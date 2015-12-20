/* This program is there to recover a psoc with a broken clock config



*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
// #include <math.h>


//#define readflash
//#define eraseflash
//#define fillflash

#include "usbprog_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "Error returned from ioctl call while port acquire",
  "IOCTL error in SWD_read call",
  "Some error in read-from-address call",
  "IOCTL error in SWD_write call", /* 5 */
  "Multibyte read failed",
  "Reset failed",
  "",
  "",
  "Error opening ihx file",   /* 10 */
  "Source file endend before EOF entry",
  "ihx format error: Source line too short",
  "ihx format error: Line does not start with colon",
  "ihx format error: Cannot convert hex into byte",
  "ihx format error: unrecognized record type", /* 15 */
  "ihx format error: Checksum mismatch",

};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/usbprog0"

/* helper code to transfer int to mem adress */
void int2data(int a, char *data) {
  int i;
  int b=a;
  for (i=0; i<4; i++) {
    data[i] = b & 0xff;
    b>>=8;
  };
}
/* careful - data is a char[5] thing */
int data2int(unsigned char *d2) {
  return d2[1] + (d2[2]<<8) + (d2[3]<<16) + (d2[4]<<24);
}

/* code to retreive the device ID word via SWD. On Error, -1 is returned */
int Get_Device_ID(int handle) {
  unsigned char d2[5];
  int ev;
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare address select to IDACCESS in DP space */
  d2[0]=0xa5; /* address bits = 00, DP access, read, odd parity */
  ev=ioctl(handle, SWD_Read, &d2);
  if (ev) return -1; /* not nice but what can you do... */
  if ((d2[0]&7) != 1) {
    printf("Warning: Device ID read attempt did not get proper ack: %02x\n",d2[0]);
  }
  retval=data2int(d2);
  //printf("ID req Ack status: %02x; data: %08x; ioctl returns: %08x\n",d2[0],retval,ev);
  return retval;
}
/* write data to PSOC space ; uses a 24 bit address, and 32 bit data.
   returns -1 on io error. */
int Write_To_Address(int handle, int address, int data) {
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare writing of address */
  d2[0]=0x8b; /* address bits = 01, AP access, write, even parity */
  int2data(address,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  //printf("Adr write ack: %02x;",d2[0]);
  /* write data */
  d2[0]=0xbb; /* address bits = 11, AP access, write, odd parity */
  int2data(data,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  //printf("data write ack: %02x\n",d2[0]);
  return 0;
}

/* reads data from PSOC space ; uses a 24 bit address. the data is
   returned in the 32 bit data pointer. returns -1 on io error, 0 on success. */
int Read_From_Address(int handle, int address, int *data) {
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare writing of address */
  d2[0]=0x8b; /* address bits = 01, AP access, write, even parity */
  int2data(address,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  //printf("Adr write ack: %02x; ",d2[0]);
  /* dummy read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  *data = data2int(d2);
  //printf("dummy read ack: %02x; data:%08x; ",d2[0], *data);
  /* real read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  //printf("real read ack: %02x; rest: %02x %02x %02x %02x\n",d2[0], d2[1], d2[2], d2[3], d2[4]);
  *data = data2int(d2);
  return 0;
}

/* reads numbytes of data from PSOC space ; uses a 24 bit address. the data is
   returned into an array of char.  returns -1 on io error, 0 on success. */
int Read_Multibyte(int handle, int address, int numbytes, char *data) {
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  int i=0;
  /* prepare writing of address */
  d2[0]=0x8b; /* address bits = 01, AP access, write, even parity */
  int2data(address,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  //printf("Adr write ack: %02x; ",d2[0]);
  /* dummy read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  //printf("dummy read ack: %02x; ",d2[0]);
  for (i=0; i<numbytes; i++) {
    /* real read */
    d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
    if (ioctl(handle, SWD_Read, &d2)) return -1;
    //printf("real read #%i ack status: %02x\n",i,d2[0]);
    data[i]=d2[1]; /* rescue data byte */
  } 
  return 0;
}

/* helper code to read from DBGPRT_CFG */
int Read_dbg(int handle){
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */

  /* prepare writing of address */
  d2[0]=0x8d; /* address bits = 01, dP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("dummy read ack: %02x; ",d2[0]);

  d2[0]=0x8d; /* address bits = 01, dP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("real read  ack: %02x; ",d2[0]);


  return data2int(d2);
}


/*--------------------------------------------------------------------*/
/* ihx reading related stuff */
#define flash_rowsize 256
#define flash_size 0x10000
#define flash_tagsize (flash_size/flash_rowsize)

/* structure which holds the data array */
char flashdata[flash_size];
char flashtag[flash_tagsize];

/* ihx parsing code */
int getbyte(char *src) {
  int c=0, k=0;
  char u;
  for (k=0; k<2; k++) {
    c *= 16;
    u=src[k];
    if ((u<'0') || (u>'9')) {
      u &=0xdf; /* uppercase character */
      if ((u<'A') || (u>'F')) {
	return -1; /* no proper character */
      } else {
	c += u-'A'+10;
      }
    } else {
      c += u-'0';
    }
  }
  return c;
}



#define linelength 256
/* parser code */
int parse_ihx(FILE *src) {
  char instring[linelength];
  char endfile = 0;
  char *readidx; /* points to current position */
  int length, adr, chksum, tmp, type, i;
  
  while (fgets(instring, linelength, src)) {
    //printf("%s",instring);
    /* consistency checks */
    if (strlen(instring)<11) return 12;
    readidx=instring; /* reset working pointer */
    if (readidx[0]!=':') return 13;
    readidx++; /* point to first hex char */

    length=getbyte(readidx);
    if (length<0) return 14;
    chksum =length;
    readidx +=2; adr=getbyte(readidx); if (adr<0) return 14;
    chksum += adr;
    readidx +=2; tmp=getbyte(readidx); if (tmp<0) return 14;
    chksum += tmp;
    adr = (adr <<8) | tmp; /* this is the address */
    readidx +=2; type=getbyte(readidx); if (type<0) return 14;
    chksum += type;

    //printf("adr: %04x, type: %02x, len:%02x\n",adr, type, length);
    /* some last consistency check */
    if (strlen(instring)<(11+length*2) ) return 12;
    /* record interpretation */
    switch (type) {
    case 0: /* data record */
      for (i=0; i<length; i++) {
	readidx +=2; tmp=getbyte(readidx); if (tmp<0) return 14;
	chksum += tmp;
	flashdata[adr+i]=tmp;
	flashtag[(adr+i)/flash_rowsize] |=1;
      }
      break;
    case 1: /* EOF record */
      endfile=1;
      break;
    default:
      return 15; /* unrecognized record type */
    }
    /* do checksum test */
    readidx +=2; tmp=getbyte(readidx); if (tmp<0) return 14;

    //printf(" chksum: %04x, nominal: %02x\n",chksum, tmp);
    if ((chksum + tmp)&0xff) return 16; /* chksum mismatch */
  }
  
  if (!endfile) return 11;
  return 0;
}


/*--------------------------------------------------------------------*/
/* main code */

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval=0, retdata=0;
    int i, address, fpag;
    FILE *hexfile;
    char data[100]; /* parameter for communication with device driver */
    char targetdata[1024];
    unsigned char sign, temperature; /* for flashing */
   
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }
    /* try to acquire device */
    data[0]=5; /* 0: no programkey, 1: programkey is sent */
    retval=ioctl(handle, SWD_Acquire, data);
    if (retval) return -emsg(2);
    printf("Return value of ack: 0x%02x, rounds: %02x \n",data[0], data[1]);

    /* resend test key */
    //retval=Write_To_Address(handle, 0x050210, 0xea7e30a9); /* test key */
    //if (retval) return -emsg(5);
    /* reset swd unit */
    //if (ioctl(handle, SWD_Reset, 60)) return -emsg(7);
    //if (ioctl(handle, SWD_Sendword, 0xfffe)) return -emsg(7);

    /* try to read device ID */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("Returned device ID: 0x%08x\n",retval);

    /* reset swd unit */
    //if (ioctl(handle, SWD_Reset, 60)) return -emsg(7);
    //if (ioctl(handle, SWD_Sendword, 0x7fff)) return -emsg(7);


    /* try to read device ID */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("2nd Returned device ID: 0x%08x\n",retval);


    /* third ID read attempt */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("Run 3: Returned device ID: 0x%08x\n",retval);
 
    retval=Write_To_Address(handle, 0x050220, 0xb3); /* Halt CPU, enable DOC*/
    if (retval) return -emsg(5);
 
   
    /* Read a value from a memory location */

    address=0;
    retval=Read_From_Address(handle, 0x46ec, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("Returned silicon revision ID: 0x%08x\n",retdata);
 
    retval=Read_From_Address(handle, 0x050220, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("Readback of DOC_DBG_CTRL: 0x%08x\n",retdata);
 
   
    /* Write to memory location; info taken from AN62391, page 16 */
    //retval=Write_To_Address(handle, 0x050220, 0xb3); /* Halt CPU, enable DOC*/
    //if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x46ea, 0x01); /* Halt CPU */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x43a0, 0xbf); /* Enable subsystems */
    if (retval) return -emsg(5);
 
    retval=Write_To_Address(handle, 0x4210, 0x00); /* xtal off */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4000, 0x00); /* direct clock */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4200, 0x00); /* IMO to 12 MHz */
    if (retval) return -emsg(5);

    /* ------------------------------------------------------------ */
    /*fixing area */


    /* read back */
    retval=Read_From_Address(handle, 0x46ea, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("at 46ea : 0x%08x, retval: %08x\n",retdata,retval);

    /* read PC */
    retval=Read_From_Address(handle, 0x05014e, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("PC : 0x%08x, retval: %08x\n",retdata,retval);

    /* ------------------------------------------------------------ */

    /* Read a value from a memory location */
    retval=Read_From_Address(handle, 0x4722, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("SPC_status: 0x%08x, retval: %08x\n",retdata,retval);

    /* reset SPC engine and set to low bus speed */
    retval=Write_To_Address(handle, 0x4723, 0x03); /* Manual reset, slow clk */
    if (retval) return -emsg(5);

    /* Read a value from a memory location */
    retval=Read_From_Address(handle, 0x4722, &retdata);
    if (retval) return -emsg(4); /* read call failed */
    printf("Second SPC_status: 0x%08x, retval: %08x\n",retdata,retval);


#define readnvl
#ifdef readnvl

    /* do port configuration to fix NVL read bug in silicon ES1 and ES2 */
    retval=Write_To_Address(handle, 0x5112, 0x0); /* Port reg 0 */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x5113, 0x0); /* Port reg 1 */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x5114, 0x0); /* Port reg 2 */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x5110, 0x4); /* data output, P[1].2 */
    if (retval) return -emsg(5);

    /* The read sequence for each NVL byte */
    for (address=0; address<4; address++) {
      retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, 0xd6); /* d3 + readbyte */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, 0x03); /* multibyte rd */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, 0x80); /* array ID */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, address & 0xff); /* adr */
 
      /* wait until done */
      do {
	usleep(500000);
	retval=Read_From_Address(handle, 0x4722, &retdata);
	if (retval) return -emsg(4); /* read call failed */
      } while (retdata != 1); /* wait for data ready */

      /* Read back byte */
      retval=Read_From_Address(handle, 0x4720, &retdata);
      if (retval) return -emsg(4); /* read call failed */
      data[address]=retdata & 0xff;
      
    }
    printf("NVL content:\n  %02x %02x %02x %02x\n",
	   data[0] & 0xff, data[1] & 0xff, data[2] & 0xff, data[3] & 0xff);
    
#endif

    

#ifdef readflash
    /* read first flash row */
    for (address=0; address<2048; address +=256) {
    
    retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, 0xd7); /* d3 + multibyte rd */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, 0x04); /* multibyte rd */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, 0x00); /* array ID */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, (address>>16)& 0xff); /* adr msb */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, (address>>8)& 0xff); /* adr */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, address& 0xff); /* adr lsb */
    if (retval) return -emsg(5);
    retval=Write_To_Address(handle, 0x4720, 0xff); /* number of bytes */
    if (retval) return -emsg(5);

    /* wait until done */
    do {
      usleep(500000);
      retval=Read_From_Address(handle, 0x4722, &retdata);
      if (retval) return -emsg(4); /* read call failed */
    } while (retdata != 1); /* wait for data to be readt */

    /* readback loop */
    retval=Read_Multibyte(handle, 0x4720, 256, targetdata);
    if (retval) return -emsg(6); /* read failed */

    /* display stuff */
    for (i=0; i<256; i++) {
      if ((i&0xf)==0) printf("%04x: ",i+address);
      printf("%02x ",targetdata[i]&0xff);
      if ((i&0xf)==0xf) printf("\n");
    }
    }
#endif
    

#ifdef eraseflash
    printf("Erasing flash....");
    /* send erase flash command */
    retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, 0xdc); /* d3 + erase */
      if (retval) return -emsg(5);
      retval=Write_To_Address(handle, 0x4720, 0x09); /* erase */
      if (retval) return -emsg(5);
      
      /* wait until done */
      do {
	usleep(500000);
	retval=Read_From_Address(handle, 0x4722, &retdata);
	if (retval) return -emsg(4); /* read call failed */
      } while (retdata  != 2); /* wait for idle */
     printf("done\n");
     
#endif


    
#ifdef fillflash

     printf("Getting die temperature for flashing....");
     for (i=0; i<2; i++) {
       retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0xe1); /* d3 + get temp */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x0e); /* get temp */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x03); /* number of samples */
       if (retval) return -emsg(5);
       /* wait until data ready */
       do {
	 usleep(500000);
	 retval=Read_From_Address(handle, 0x4722, &retdata);
	 if (retval) return -emsg(4); /* read call failed */
       } while (retdata != 1); /* wait for data ready */
       /* readback loop */
       retval=Read_Multibyte(handle, 0x4720, 2, targetdata);
       if (retval) return -emsg(6); /* read failed */
       sign=(unsigned char)targetdata[0];
       temperature=(unsigned char)targetdata[1];
       printf("\n Read number %d: Sign: %02x, Temperature: %d units\n",
	      i,sign, temperature);
     }
     
     printf("Parsing ihx file named %s.....",argv[1]);
     
     hexfile=fopen(argv[1],"r");
     if (!hexfile) return -emsg(10);
     
     /* prepare target data */
     for (i=0; i<flash_size; i++) flashdata[i]=0;
     for (i=0; i<flash_tagsize; i++) flashtag[i]=0;
     
     /* call parser. Should return 0 on success or error code. Flash data and
       tags are kept as global variables for later extension to other fields. */
     retval=parse_ihx(hexfile);
     if (retval) return -emsg(retval);
     fclose(hexfile);
     printf("done\n");
     printf("Programming flash now.");
      
     /* flash data is now in buffer. Now transfer to processor. */
     for (fpag=0; fpag<256; fpag++) { /* loop through all populated pages */
       if (flashtag[fpag] == 0) continue; /* nothing to write */
       printf("transferring page %02x.....",fpag);
       
       /* load row */
       retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0xd5); /* d3 + load row */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x02); /* ld row */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x00); /* array ID */
       if (retval) return -emsg(5);
       
       /* send data */
       for (i=0; i<256; i++) {
	 //printf("i=%03x: %02x\n; ",i,flashdata[fpag*256+i]&0xff);
	 retval=Write_To_Address(handle, 0x4720, flashdata[fpag*256+i]&0xff); /* data */
	 if (retval) return -emsg(5);
       }
       /* wait until done */
       
       do {
	 usleep(500000);
	 retval=Read_From_Address(handle, 0x4722, &retdata);
	 if (retval) return -emsg(4); /* read call failed */
       } while ((retdata & 2) != 2);
       
       if (retdata>>2) {
	 printf("load row return status :%02x\n",retdata>>2);
	 return -1;
       }


       printf("flashing.....");
       
       /* send write command - this assumes an erased flash */
       retval=Write_To_Address(handle, 0x4720, 0xb6); /* init key */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0xda); /* d3 + pgm row */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x07); /* pgm row */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x00); /* array ID */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, 0x00); /* adr msb */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, fpag); /* adr lsb */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, sign); /* sign */
       if (retval) return -emsg(5);
       retval=Write_To_Address(handle, 0x4720, temperature); /* temperature */
       if (retval) return -emsg(5);

       
       /* wait until done */
       do {
	 usleep(500000);
	 retval=Read_From_Address(handle, 0x4722, &retdata);
	 if (retval) return -emsg(4); /* read call failed */
       } while ((retdata &2)!= 2);
       printf("done\n");
       if (retdata>>2) {
	 printf("flash return status :%02x\n",retdata>>2);
	 return -1;
       }

       
     }
     
#endif
     
    //retval=Read_dbg(handle);
    //printf("Return value: 0x%08x\n",retval);

    close(handle);
    
    return 0;

}

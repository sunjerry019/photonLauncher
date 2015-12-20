/* This program is there to transfer code into the PSOC3 processor with the
   combined JTAG/SWD protocol.

   Intent is to acquire the device, and do a device ID check. Currently, there
   is no transfer of data into the chip, but it will use a Intel hex file as a
   source.

   first code      7.12.2010

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
    printf("Warning: Device ID read attempt did not get proper ack.\n");
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
  printf("Adr write ack: %02x;",d2[0]);
  /* write data */
  d2[0]=0xbb; /* address bits = 11, AP access, write, odd parity */
  int2data(data,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  printf("data write ack: %02x\n",d2[0]);
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
  printf("Adr write ack: %02x; ",d2[0]);
  /* dummy read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  *data = data2int(d2);
  printf("dummy read ack: %02x; data:%08x; ",d2[0], *data);
  /* real read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("real read ack: %02x; rest: %02x %02x %02x %02x\n",d2[0], d2[1], d2[2], d2[3], d2[4]);
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

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval=0, retdata=0;
    int i, address;
    FILE *inhandle = stdin; /* temporary version */
    char data[100]; /* parameter for communication with device driver */
    char targetdata[1024];
   
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }
    /* try to acquire device */
    data[0]=1; /* 0: no programkey, 1: programkey is sent */
    retval=ioctl(handle, SWD_Acquire, data);
    if (retval) return -emsg(2);
    printf("Return value of ack: 0x%02x, rounds: %02x \n",data[0], data[1]);

    /* resend test key */
    //retval=Write_To_Address(handle, 0x050210, 0xea7e30a9); /* test key */
    //if (retval) return -emsg(5);

    /* try to read device ID */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("Returned device ID: 0x%08x\n",retval);



    /* reset swd unit */
    //if (ioctl(handle, SWD_Reset, 60)) return -emsg(7);
    //if (ioctl(handle, SWD_Sendword, 0xfffe)) return -emsg(7);

 
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
    retval=Write_To_Address(handle, 0x4200, 0x00); /* IMO to 12 MHz */
    if (retval) return -emsg(5);

    /* second ID read attempt */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("Run 2: Returned device ID: 0x%08x\n",retval);


  

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


    
#define readflash
#ifdef readflash
    /* read first flash row */

    address=0;
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
    } while (retdata != 1);

    /* readback loop */
    retval=Read_Multibyte(handle, 0x4720, 256, targetdata);
    if (retval) return -emsg(6); /* read failed */

    /* display stuff */
    for (i=0; i<256; i++) {
      if ((i&0xf)==0) printf("%04x: ",i);
      printf("%02x ",targetdata[i]&0xff);
      if ((i&0xf)==0xf) printf("\n");
    }
#endif

    //retval=Read_dbg(handle);
    //printf("Return value: 0x%08x\n",retval);

    close(handle);
    
    return 0;

}

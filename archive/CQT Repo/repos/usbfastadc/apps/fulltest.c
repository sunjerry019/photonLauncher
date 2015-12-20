/* program that tests the combined features of the card+firmware+host driver */

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/mman.h>

#include "usbfastadc_io.h"

/* get a reasonably large buffer */
#define SIZE_DMA 1<<24

/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot open device.", /* 1 */
  "Cannot parse device file name",
  "Error setting up clock configuration",
  "Error setting CPLD mode",
  "Error setting ADC configuration ", /* 5 */
  "Mmap failed",
  "error starting USB engine on driver side",
  "error starting limited acquisition",
  "error stopping USB engine",
  "error reading byte count",  /* 10 */
  "error resetting the device",

};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbfastadc0"

/* read back status registers located in 0x22c, 0x22d. parameter is handle,
   return is 0x22c in its 0..7, 0x22D in bits 8..15 */
int getstatusbits(int handle) {
  char buffer[10];
  int retval;
  buffer[0]=2; /* read back two bytes */
  buffer[1]=0x02; buffer[2]=0x2d; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  return ((buffer[3]<<8)& 0xff) + (buffer[4] & 0xff);
}
/* read back some registers */
void readregister(int handle, int adr, int num) {
  char buffer[256];
  int retval, i;
  buffer[0]=num; /* read back some bytes */
  buffer[1]=(adr >>8)&0x1f; buffer[2]=adr & 0xff; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  for (i=0; i<num; i++) printf("%03x: 0x%02x\n",adr-i,buffer[3+i]&0xff);

}

/* generic SPI configuration, eats a data stream and a command */
int SPI_configure(int handle, char *configdata, int command) {
  int i, l, retval;
  i=0; /* initial index */
  while ((l=configdata[i])) { /* length is non-zero */
    retval=ioctl(handle, command, &configdata[i]); /* copy data */
    printf("length: %d, retval: %d\n",l,retval);
    usleep(10000);
    if (retval) return retval; /* an error has occured */
    i+=l+3; /* move to next sequence in data field */
  }
  return 0; /* everything went fine */
}

/* generic clock configuration. Data is stored in an array that could reside
   in the firmware at some point. Format is SPI data format, with a first byte
   describing payload size, followed by an address, then followed by the
   payload. A payload size of 0 terminates the configuration chain. */
char clock_data[] = {
  /* reset device */
  1, 0x00, 0x00,
  0x24,

  /*  PLL2 configuration: A=0, B=48 (total N: 192), pump 56uC 
      VCO2 frequency: 3840 MHz , VCOdiv=4, */
  7, 0x00, 0xf6,
  0x00, 0x00, 0x00, 0x08, 0x03, 0x30, 0x10,

  /* Output configuration channels 3..0 */
  12, 0x01, 0xa1,
  0x00, 0x1f, 0x20, /* ch 3: */
  0x00, 0x2f, 0x02, /* ch 2: div by 48 ->20 MHz, LVDS3.5mA */
  0x00, 0x2f, 0x08, /* ch 1: div by 48 -> 20 MHz ,CMOS true phase */
  0x00, 0x1f, 0x20, /* ch 0: */

  /* Output configuration channels 5, 4 */
  6, 0x01, 0xb3,
  0x00, 0x2f, 0x08, /* ch 5: /48, CMOS output at OUT5, true phase */
  0x00, 0x1f, 0x20, /* ch4: */

  /* PLL1 parameter set */
  13, 0x00, 0x1c,
  0x48, /* select refa, Vcc/2 when no signal */
  0x30, /* 0x1b: OSC_in is feedb ref, ZD is off, REFA in CMOS mode */
  0x28, /* 0x1a: REFA is enabled, REFA, OSCinREFB in cmos mode */
  0x03, /* 0x19: normal operation, minimum antibacklash */
  0x0c, /* 6 uA charge pump current */
  0x00, 20, /* 0x17/0x16: PLL1 feedback divider ->20 */
  0, 1, /* reserved, rev_test divider ->1 */
  0, 1, /* REFB R divider ->1 */
  0, 10, /* REFA R divider ->10 */

  /* PLL1 ouput control */
  2, 0x01, 0xbb,
  0x80, /* PLL1 output driver off, no routing to outputs 0,1 */
  0x00, /* 0x1ba: PLL1 output divider=0, output strenght= */
  
  /* power down control of PLLs */
  1, 0x02, 0x33,
  0x0,

  /* update registers */
  1, 0x02, 0x34,
  0x01, /* reset */
  
  /* initiate calibration & update registers */
  1, 0x00, 0xf3,
  0x0a,
  1, 0x02, 0x34, 0x01,  

  /* issue a synchronize command */
  1, 0x02, 0x32, 0x01, 1, 0x02, 0x32, 0,

  /* end of sequence */
  0
}; 

int clock_configure(int handle) {
  return SPI_configure(handle, clock_data, CLOCKCHIP_WRITE);
}

/* generic ADC configuration. */
char adc_data[] = {
  1, 0x00, 0x00,
  0x18, /* reset */
  /* user test pattern: 0x1234, 0x5678 alternating*/
  4, 0x00, 0x1c,
  0x12, 0x34, 0x56, 0x78,
  /* choose test mode -> user defined, alternate is 0x48. 00 is normal */
  1, 0x00, 0x0d,
  0x00,
  /* set transfer */
  1, 0x00, 0xff, 1,
  
  0     /* end of pattern */
};

int adc_configure(int handle) {
  return SPI_configure(handle, adc_data, ADCCHIP_WRITE);
}


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int i, retval, v;
    unsigned char *startad=NULL;
    //uint16_t *intarray;
    char bla[30];


    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       }
    }

    /* open device */
    handle=open(devicefilename,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }

    /* send device in a clean state */
    retval=ioctl(handle, RESET_TRANSFER);
    if (retval) return -emsg(11);
    
    
    /* Basic CPLD configuration to turn on power */
    retval=ioctl(handle, WRITE_CPLD, 0x010c);
    if (retval) return -emsg(4);
    
    /* Configuration of clock chip to provide 20 MHz to ADC and IFCLK */
    if (clock_configure(handle)) return -emsg(3);


    for (i=0; i<2; i++) {
      printf("status bits: %04x\n",getstatusbits(handle));
      usleep(500000);
    }


    /* configure ADC with something reasonable */
    if (adc_configure(handle)) return -emsg(5);
   
    /* start mmap */
    startad=mmap(NULL,SIZE_DMA,PROT_READ|PROT_WRITE, MAP_SHARED,handle,0);
    if (startad==MAP_FAILED) {
      printf("erno of fail: %d\n",errno);
      return -emsg(6);
    }
   
    /* start acquisition */
    retval=ioctl(handle, Start_USB_machine);
    if (retval) return -emsg(7);

    /* try to get 2000 entries from fx2 */
    retval=ioctl(handle, START_LIMITED,20000);
    if (retval) return -emsg(8);
    
    /* check running status */
    for (i=0; i<4; i++) {
      retval=ioctl(handle, Get_transferredbytes);
      printf("transferred bytes: %d\n",retval);
      usleep(100000); /* wait 100ms */
      if (i==2) {
	//retval=ioctl(handle, FLUSH_FIFO);
	//printf("retval from flush: %d\n",retval);
      }
      retval=ioctl(handle, GETRDYLINESTAT, bla);
      printf("readyline stat: 0x%02x, retval: %d\n",bla[0],retval);
    }

    
    /* output stuff */
    for (i=0; i<256; i++) {
      if ((i&15)==0) printf("%04x:",i);
      printf(" %02x",startad[i]);
      if ((i&15)==15) printf("\n");
    }

#ifdef bla    

    /* output as integers */
    intarray = (uint16_t *) startad;
    for (i=1; i<10; i++) {
      v=intarray[i]-0x8000;
      printf("%d: %d\n",i,v);
    }

#endif
    /* see residual byte count */
    retval=ioctl(handle, GETBYTECOUNT, &v);
    if (retval) return -emsg(9);
    printf("Residual byte count: %d (=0x%x)\n",v,v);
    
    retval=ioctl(handle, GETRDYLINESTAT, bla);
    printf("readyline stat: 0x%02x, retval: %d\n",bla[0],retval);

    retval=ioctl(handle, GET_TCB, &v);
    if (retval) return -emsg(9);
    printf("TCB content: %d (=0x%x)\n",v,v);


    /* do the test */
    //printf("Press enter to flush the memory:");
    //scanf("%s", bla);
    retval=ioctl(handle, FLUSH_FIFO);
    printf("retval from flush: %d\n",retval);

    usleep(100000);
    retval=ioctl(handle, Get_transferredbytes);
    printf("transferred bytes: %d\n",retval);

    retval=ioctl(handle, GET_TCB, &v);
    if (retval) return -emsg(9);
    printf("TCB content: %d (=0x%x)\n",v,v);

  
    
    /* stop engine */
    retval=ioctl(handle, Stop_USB_machine);
    if (retval) {
      printf("return code: %d, erro: %d\n",retval, errno);
      return -emsg(9);
      }
    usleep(100000);
    
    /* see residual byte count */
    retval=ioctl(handle, Get_transferredbytes);
    printf("transferred bytes: %d\n",retval);
  
    
    close(handle);
    
    return 0;

}

/* program to program the clock/ADC chips on the board via the SPI interface.
   preliminary to test out the board
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "timestampcontrol.h"


/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot open device.", /* 1 */
  "Cannot parse device file name",
  "error switching device on",
  "error configuring clock chip",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbtmst0"

/* read back status registers located in 0x22c, 0x22d. parameter is handle,
   return is 0x22c in its 0..7, 0x22D in bits 8..15 */
int getstatusbits(int handle) {
  char buffer[10];
  int retval;
  buffer[0]=2; /* read back two bytes */
  buffer[1]=0x02; buffer[2]=0x2d; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  //for (i=0; i<6; i++) printf("  %d:0x%02x\n",i,buffer[i]&0xff);
  return ( (buffer[3]<<8) & 0xff00 ) + (buffer[4] & 0xff);
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
    //printf("length: %d, retval: %d\n",l,retval);
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

  /*  PLL2 configuration: A=0, B=50 (total N: 200), pump 56uC 
      VCO2 frequency: 4000 MHz , VCOdiv=4, */
  7, 0x00, 0xf6,
  0x00, 0x00, 0x00, 0x08, 0x03, 0x32, 0x10,

  /* Output configuration channels 1,2 */
  6, 0x01, 0x9e,
  0x00, 0x09, 0x02, /* ch 2: div by 10 ->100 MHz, LVDS3.5mA */
  0x00, 0x13, 0x01, /* ch 1: div by 20 ->50 MHz, LVPECL */

  /* Output configuration channels 5*/
  3, 0x01, 0xb3,
  0x00, 0x18, 0x09, /* ch 5: /25 ->40MHz, CMOS, true phase to - (IFCLK)*/

  /* PLL1 parameter set */
  13, 0x00, 0x1c,
  0x48, /* select refa, Vcc/2 when no signal */
  0x30, /* 0x1b: OSC_in is feedb ref, ZD is off, REFA in CMOS mode */
  0x28, /* 0x1a: REFA is enabled, REFA differential, OSCin/REFB in cmos mode */
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

  /* FS output */
  2, 0x02, 0x31,
  0x01, /* FS1: PLL1 and 2 are locked */
  0x01, /* FS0: VCXO is ok */
  
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
  1, 0x02, 0x32, 0x01, 1, 0x02, 0x34, 0x01,
  1, 0x02, 0x32, 0,    1, 0x02, 0x34, 0x01,

  /* end of sequence */
  0
}; 


/* configure clock, eventually reconfigure dividers for alternate sig */
int clock_configure(int handle) {
  int retval;
  retval=SPI_configure(handle, clock_data, CLOCKCHIP_WRITE);
  return retval;
}


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int retval;

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

    /* switch on power */
    retval=ioctl(handle, SET_POWER_STATE, 1);
    if (retval) return -emsg(3);

    usleep(1000000); /* wait some time */

    /* configure clock */
    retval=clock_configure(handle);
    if (retval) return -emsg(4);

    /* readback */
    readregister(handle, 0x22d,2);

    close(handle);
    
    return 0;

}

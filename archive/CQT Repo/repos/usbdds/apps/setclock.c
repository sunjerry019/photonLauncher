/* program to program the clock chip on the dds board - this is temporary 
   code to test if the AD9524 chip can be programmed and is working properly
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>

#include "usbdds_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "Error sending clock commands",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/dds0"


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

  /*  PLL2 configuration: A=2, B=47 (total N: 190), pump 56uC 
      VCO2 frequency: 3800 MHz , VCOdiv=4, */
  7, 0x00, 0xf6,
  0x00, 0x00, 0x00, 0x08, 0x03, 0xaf, 0x10,

  /* Output configuration channel 1*/
  3, 0x01, 0x9b,
  0x00, 0x12, 0x02, /* ch 1: div by 19 ->50 MHz, LVDS3.5mA */


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
  
  /* power down control of PLLs */
  1, 0x02, 0x33,
  0x0,

  /* set status monitor 0 to reflect PLL1 lock status */
  1, 0x02, 0x30,
  0x02,

  /* update registers */
  1, 0x02, 0x34,
  0x01, /* reset */
  
  /* update registers - is this for double happyness? */
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


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval;

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }
    
    /* configure clock */
    retval = SPI_configure(handle, clock_data, WriteClockchip);
    if (retval) {
	fprintf(stderr, "error no: %d\n",retval);
	return -emsg(2);
    }

    
    //retval=ioctl(handle, Full_DDS_Reset);
    //printf("reset retval: %d\n",retval);

    close(handle);
    
    return 0;

}

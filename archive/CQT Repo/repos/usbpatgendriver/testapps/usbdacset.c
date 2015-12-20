/* program to set a voltage on the various DAC outputs on the USB pattern
   generator device. 

   usage: usbdacset [-d devicefile] [-m] [channel] voltage
          usbdacset [-d devicefile]

   Options:
   -d devicefile: Use the specified device instead of the default device (which
                  is /dev/ioboards/pattgen_generic0 ).
   -m             With this option set, the voltage argument is in millivolt
                  rather than volts. This is to replace the
		  usbdacsetmillivolt program
   
   In the first syntax, the optional channel argument ranges from 0 to 23 
   (0 if unspecified), and the voltage ranges from -10.0 to +10.0V. The device
   is an AD7841 DAC with a resolution of 14bit, therefore the resolution is
   about 1.3mV.

   In the second syntax, without any arguments, all DACS are initialized
   reset to 0 volt.

   This program assumes that there is only one device connected to the host.

   fixed level conversion 23.11.09chk

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "usbpattgen_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "wrong number of arguments.", /* 1 */
  "Unable to open USB device. Check /dev/ioboards/ for the device",
  "Voltage out of range.",
  "unexpected return when sumbmitting a USB packet.",
  "Error parsing voltage argument.",   /* 5 */
  "Error parsing channel argument",
  "Channel number out of range (must be between 0 and 23)",
  "Cannot parse device file name",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};


#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"
#define OPEN_ATTEMPTS 5
#define OPEN_RETRYWAIT 10000

int main(int argc, char *argv[]) {
    int dacch;
    int handle; /* file handle for usb device */
    char devicefilename[200] = DEFAULT_DEVICENAME; /* holds device */
    int opt;
    float voltage;
    int v2;
    int retval;
    int opentry = OPEN_ATTEMPTS; /* try a few times to open in 
				    case someone else hogs device */
    int foundoptions=0;
    int millivoltoption=0;
    
    /* check for optional device argument */
    opterr=0;
    while ((opt=getopt(argc, argv, "+d:m")) != EOF) {
      switch (opt) {
      case 'd': /* device file option */
	if (1!=sscanf(optarg, "%199s", devicefilename)) return -emsg(8);
	foundoptions+=2; /* this is an option with two entries */
	break;
      case 'm': /* millivolt option */
	millivoltoption=1;
	foundoptions+=1;
	break;
      }
    }

    while (opentry) {
      handle=open(devicefilename,O_RDWR);
      if (handle != -1) break;
      usleep(OPEN_RETRYWAIT); /* wait for some time until retry */
      opentry--;
    }
    if (handle==-1) return -emsg(2);
    
    switch (argc-foundoptions) {
	case 1: /* no additional argument: reset DACS */
	    ioctl(handle,InitDac);
	    break;
	case 2: /* only voltage argument */
	    if (1!=sscanf(argv[1+foundoptions],"%f",&voltage)) return -emsg(5);
	    if (millivoltoption) {
	      voltage = voltage / 1000.0;
	    }
	    if ((voltage<-10.0) || (voltage>10.0)) return -emsg(3);
	    v2=(int)((voltage+10.0)*819.2); /* conversion to integer pattern */

	    dacch = 0;
	    if (v2<0) v2=0;if (v2>0x3fff) v2=0x3fff; /* boundary check */

	    if (ioctl(handle,SendDac,(v2 & 0xffff) | ((dacch & 0xff)<<16))) {
		return -emsg(4);
	    }
	    break;
	case 3: /* voltage and channel argument */
	    if (1!=sscanf(argv[2+foundoptions],"%f",&voltage)) return -emsg(5);
	    if (millivoltoption) {
	      voltage = voltage / 1000.0;
	    }
	    if ((voltage<-10.0) || (voltage>10.0)) return -emsg(3);

	    if (1!=sscanf(argv[1+foundoptions],"%d",&dacch)) return -emsg(6);
	    if ((dacch<0) || (dacch>23)) return -emsg(7);

	    v2=(int)((voltage+10.0)*819.2); /* conversion to integer pattern */
	    if (v2<0) v2=0;if (v2>0x3fff) v2=0x3fff; /* boundary check */
	    
	    retval=ioctl(handle,SendDac,(v2 & 0xffff) | ((dacch & 0xff)<<16));
	    if (retval) {
	      printf("return value: %d\n",retval);
		return -emsg(4);
	    }
	    break;
	default: 
	  //printf("options: argc=%d, foundoptions=%d\n",argc, foundoptions);
	    return -emsg(1);
    };

    return 0;
}

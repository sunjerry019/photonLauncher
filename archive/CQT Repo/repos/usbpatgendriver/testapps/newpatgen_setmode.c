/* simple code that sets the new pattern generator into one of several modes.

   usage: newpatgen_setmode [-d devicefile]
                            [-r routemode ]  
                            [-D divider]
			    [-R | -I | -A]
   
   Options:
   -d devname Communicate with the device specified in devname rather than
              the default device /dev/ioboards/pattgen_generic_0
	      
   -r route   sets the routing mode register. Defaults to 0.

   -D value   selects divider value (default: 100)


   -R         switches into run mode after eventual modeset
   -A         switches into alternate run mode after modeset
   -I         switches into idle mode after modeset

   


*/
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include "usbpattgen_io.h"
#include <unistd.h>
#include <sys/ioctl.h>

/* error handling */
char *errormessage[] = {
  "No error.",
  "Unable to open USB device.", /* 1 */
  "cannot parse device file name",
  "cannot parse route mode (integer 0..255 or hex value)",
  "missing source file name (or - for stdin)",
  "cannot open source file", /* 5 */
  "cannot parse divider value",
  "divider out of range (0..255)",
  "ioctl error writing parameters to CPLD)",
  "error setting run mode",
  
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"
#define DEFAULT_CARDMODE 1
#define DEFAULT_DIVIDER 100

int main(int argc, char *argv[]) {
  int handle; /* file handle for usb device */
  char devicefilename[200]=DEFAULT_DEVICENAME; /* name of device */
  int opt;
  int cardmode = DEFAULT_CARDMODE; /* mode in which card is left
				     0: idle, 1: run, 2: alternate run */
  int routemode = 0; /* what to fill into route register */
  int loadmode=0; /* indicates if a mode register should be loaded first */
  unsigned char cplddata[6]; /* holds data for CPLD upload */
  int runcommand[3]={IdleMode, RunMode, AltRunMode};
  int divider = DEFAULT_DIVIDER;
  int retval;
        
  /* parse arguments */
  opterr=0; /* be quiet when there are no options */
  while ((opt=getopt(argc, argv, "d:r:RAID:")) != EOF) {
    switch (opt) {
    case 'd': /* select device name */
      if (1!=sscanf(optarg,"%199s",devicefilename)) return -emsg(2);
      devicefilename[199]=0; /* safety termination */
      break;
    case 'r': /* set route mode */
      if (1!=sscanf(optarg,"%i",&routemode)) return -emsg(3);
      routemode &= 0xff;
      loadmode=1;
      break;
    case 'R': /* switch into runmode after upload */
      cardmode=1;
      break;
    case 'A': /* switch into alt run mode after upload */
      cardmode=2;
      break;
    case 'I': /* switch into idle mode after upload */
      cardmode=0;
      break;
    case 'D': /* select divider value */
      if(1!=sscanf(optarg,"%d",&divider)) return -emsg(6);
      if ((divider<0) || (divider>255)) return -emsg(7);
      loadmode=1;
      break;
    }
  }
 
  /* open device file */
  handle=open(devicefilename,O_RDONLY);
  if (handle==-1) return -emsg(1);

  /* reset device */
  ioctl(handle, ResetCPLD);
  /* switch to desired mode */
  if (loadmode) { /* we need to program the CPLD mode regs */
    cplddata[0]=0; /* main mode, not yet used */
    cplddata[1]=routemode;
    cplddata[2]=divider;
    cplddata[3]=0; cplddata[4]=0; cplddata[5]=0; /* address */
    retval=ioctl(handle, WriteParameters, cplddata);
    if (retval) {
      printf("retval: %d, errno:%d\n",retval,errno);
      return -emsg(8);
    }
  }
  /* switch to desired run mode */
  if (ioctl(handle, runcommand[cardmode])) return -emsg(9);
  
  /* close device */
  close(handle);

  return 0;
}




   

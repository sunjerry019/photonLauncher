/* program to set a value to the digital output of the usb pattern generator
   device. This is a very simple app. 

   (DOES NOT WORK BECAUSE HARDWARE HAS ISSUES) 

   usage: usbdigiout <value>
   
   The integer value is copied into the digital outputs. If no argument is
   given, all outputs are set to zero.



*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include "usbpattgen_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "wrong number of arguments.", /* 1 */
  "Unable to open USB device. Check /dev/ioboards/ for pattgen_generic0",
  "Error parsing  argument.",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};


#define DEVICENAME "/dev/ioboards/pattgen_generic0"
int main(int argc, char *argv[]) {
    int dacch;
    int handle; /* file handle for usb device */
    float voltage;
    int v2;
    
    handle=open(DEVICENAME,O_RDWR);
    if (handle==-1) return -emsg(2);
    
    switch (argc) {
	case 1: /* no additional argument: set al lto zero */
	    ioctl(handle, SetDigitalOutput, 0); 
	    break;
	case 2: /* only value  argument */
	    if (1!=sscanf(argv[1],"%d",&value)) return -emsg(3);
	    ioctl(handle, SetDigitalOutput, value); 
	    break;
	default: 
	    return -emsg(1);
    };

    return 0;
}

/* program to set the internal timer of the digital output card. 

     usage:settimer value
   
   Therein, value is the periode in microsecnds. The timer can be set with a
   resolution of 2 microsecond, the maximal periode is 2^17 microsec, the 
   minimal periode fixed to 20 microseconds. If the periode exceeds a 
   sensible limit, the program returns with an error message and leaves the 
   card unchanged. 
 
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>

#include "usbdigiout_io.h"


/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "timing out of range",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/digiout0"

/* definition in periodes in multiples of a microsecond */
#define MIN_TIMING 20
#define MAX_TIMING 131072

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int timing;

    handle=open(DEVICENAME,O_RDWR);
    if (handle==-1) return -emsg(1);

    sscanf(argv[1],"%d",&timing);
    if (timing<MIN_TIMING || timing >= MAX_TIMING) return -emsg(2);
    
    ioctl(handle,Set_Timer,0xffff-(timing/2));
        
    return 0;

}

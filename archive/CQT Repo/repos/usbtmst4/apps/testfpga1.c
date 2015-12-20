/* program to program the clock/ADC chips on the board via the SPI interface.
   preliminary to test out the board

   usage:
   testfpga1 [-d devicenode] [-v value]
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
  "error from setting value",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbtmst0"


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int retval;
    int sendvalue=0;

    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:v:")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       case 'v': /* send integer value to config register */
	 if (sscanf(optarg,"%d", &sendvalue)!=1 ) return -emsg(2);
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

    
    /* send some stuff to config register */
    retval=ioctl(handle, WRITE_CPLD, sendvalue);
    if (retval) return -emsg(4);

    close(handle);
    
    return 0;

}

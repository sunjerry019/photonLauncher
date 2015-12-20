/* program to program the CPLD register

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "usbfastadc_io.h"


/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot open device.", /* 1 */
  "Cannot parse device file name",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbfastadc0"


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int retval;
    int value;

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

    /* eventually abort a GPIF transaction */
    retval=ioctl(handle,RESET_TRANSFER);
    printf("return value from abort : %d = 0x%x\n", retval, retval);
    
    /* update registers */
    do {
      printf("Enter number or -1 for exit: ");
      scanf("%i",&value);
      if (value<0) break;
      retval=ioctl(handle, WRITE_CPLD, value);
      printf("return value from write : %d = 0x%x\n",retval, retval);
    } while (1);

    close(handle);
    
    return 0;

}

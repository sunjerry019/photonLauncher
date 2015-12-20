/* program to test the power bit

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
  "Cannot parse device fila name",
  "cannot parse power status",
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
    int powerstatus = 0;

    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:v:")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       case 'v': /* set power status */
	   if (sscanf(optarg,"%d", &powerstatus)!=1 ) return -emsg(3);
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


    retval=ioctl(handle, SET_POWER_STATE, powerstatus);
    printf("sent value: %d, return value: %d\n", powerstatus, retval);

    close(handle);
    
    return 0;

}

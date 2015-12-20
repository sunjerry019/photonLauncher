/* program to send a pattern to the digital output card */

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>

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


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int i, retval;
    int timing=(1<<16)-50;
    uint8_t data[100000];
    int totransfer;
    int transferred, thistransfer;

    printf("Byte number to transfer: ");
    scanf("%d",&totransfer);

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) return -emsg(1);

    for (i=0;i<50000;i++) { 
	data[2*i]=(i>600)?((i&64)?1:0):(i&1);
	data[2*i+1]=0;
    }

    ioctl(handle,Set_Timer,timing);

    ioctl(handle,Start_Transfer);
    
    transferred=0;
    do {thistransfer=totransfer-transferred;
	retval=write(handle,&data[transferred],thistransfer);
	printf("return value: %d\n",retval);
	if (retval<0) break;
	transferred+=retval; 
        usleep(50000); /* wait 50 msec */
    } while (transferred < totransfer);
    return 0;

}

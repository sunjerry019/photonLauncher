/* program to talk to the USB pattern generator device. This version (tpg1.c)
   should only be able to use a few ioctls.


*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include "usbpattgen_io.h"


#define DEVICENAME "/dev/ioboards/pattgen_generic0"
int main(int argc, char *argv[]) {
    int opcode, p1;
    int handle; /* file handle for usb device */


    handle=open(DEVICENAME,O_RDWR);
    if (handle==-1) {
	perror("usbtester tpg1");
	return -1;
    }
    
    do {
	/* ask for argument */
	printf("0: exit 4: initialize_rfsrc 5: RF_reference, 6: RF parameter");
	scanf("%d",&opcode);
	switch (opcode) {
	    case 0: break;
	    case 4:
		printf("initialize RF\n");
		ioctl(handle,InitializeRFSRC);
		break;

	    case 5:
		printf("RF source parameter: ");scanf("%i",&p1);
		ioctl(handle,Rf_Reference,p1);
		break;
	    case 6:
		printf("RF value parameter: ");scanf("%i",&p1);
		ioctl(handle,Send_RF_parameter,p1);
		break;

 
	}
    } while (opcode);
    
    close(handle);
    return 0;
}

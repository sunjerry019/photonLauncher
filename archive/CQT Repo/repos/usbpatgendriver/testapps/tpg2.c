/* program to talk to the USB pattern generator device. This version (tpg2.c)
   should also allow to talk to the DAC.


*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <unistd.h>
#include "usbpattgen_io.h"


#define DEVICENAME "/dev/ioboards/pattgen_generic0"
int main(int argc, char *argv[]) {
    int opcode, p1;
    int handle; /* file handle for usb device */
    int retval;
    int dacval, dacch;
    char *dummymem;

    handle=open(DEVICENAME,O_RDWR);
    if (handle==-1) {
	perror("usbtester tpg1");
	return -1;
    }
    
    dummymem = (char *)malloc(1000000);
    do {
	/* ask for argument */
	printf("0: exit 2: SendDac 3: InitDac 4: initialize_rfsrc\n 5: RF_reference, 6: RF parameter 9: Lseek 7: runmode 8: idlemode 10: loadmode\n99: request status 50: write stuff->");
	scanf("%d",&opcode);
	switch (opcode) {
	    case 0: break;
	    case 2: /* senddac */
		printf("DAC value: ");scanf("%i",&dacval);
		printf("DAC channel: ");scanf("%i",&dacch);
		ioctl(handle,SendDac,(dacval & 0xffff) | ((dacch & 0xff)<<16));
		break;
	    case 3: /* init DAC */
		printf("initialize DAC\n");
		ioctl(handle,InitDac);
		break;
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
	    case 9: /* lseek */
		printf("Lseek parameter ");scanf("%i",&p1);
		ioctl(handle, PatternRAM_lseek,p1);
		break;

	    case 7: /* run mode */
		printf("switch to run mode\n");
		ioctl(handle,ForceRun);
		break;
	    case 8: /* idle mode */
		printf("switch to idle mode\n");
		ioctl(handle,ForceIdle);
		break;
	    case 10: /* load mode */
		printf("switch to prog mode\n");
		ioctl(handle,ProgMode); 
		break;
	    case 50: /* write stuff to device */
		printf("number of bytes to write: ");scanf("%i",&p1);
		retval=ioctl(handle,2005,p1);
		printf("written %d bytes, retval: %d.\n",p1, retval);
		break;
	    case 70: /* do real write */
		printf("number of bytes to write: ");scanf("%i",&p1);
		retval=write(handle,dummymem,p1);
		printf("write returned: %i\n",retval);
		break;
	    case 99: /* request status */
		printf("status variable -> ");scanf("%i",&p1);
		ioctl(handle,RequestStatus,p1);
		printf("returnvalue: %x\n",ioctl(handle,2004));
		break;
  	    case 91: /* request status */
		printf("status variable -> ");scanf("%i",&p1);
		ioctl(handle,RequestStatus,p1);
		printf("returnvalue: %x\n",ioctl(handle,2000));
		break;
 
	}
    } while (opcode);
    
    close(handle);
    return 0;
}

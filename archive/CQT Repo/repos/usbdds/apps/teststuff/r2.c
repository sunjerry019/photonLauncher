/* program to send a pattern to the digital output card */

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>

#include "usbdds_io.h"

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

#define DEVICENAME "/dev/ioboards/dds0"

/* code which dies the EP1 send sequence. it generates the framework for the
   EP1 command correctly, and should return the number of transfered bytes
   as reported by the ioctl thing. */
int send_sequence(int handle, int number, uint8_t *buffer) {
    int i; uint8_t chksum;
    int length; /* transmitted length */
    length=number; if (length>60) length=60; if (length<0) length=0;
    
    /* generate overall length info for EP1 command */
    ioctl(handle, 3000, (0<<8) + length+3);  chksum = length+3;
    ioctl(handle, 3000, (1<<8) + SendDirectStream);
    chksum += SendDirectStream; /* cmd */
    for (i=0; i<length; i++) {
	ioctl(handle, 3000, ((i+2)<<8) + (uint8_t)buffer[i]);
	chksum += (uint8_t)buffer[i];
    }
    ioctl(handle, 3000, ((length+2)<<8) + chksum); /* add checksum */
    
    return ioctl(handle, 3002, length+3);
}
int send_sequence2(int handle, int code) {
    uint8_t chksum;
    int length=0; /* transmitted length */
    
    /* generate overall length info for EP1 command */
    ioctl(handle, 3000, (0<<8) + length+3);  chksum = length+3;
    ioctl(handle, 3000, (1<<8) + (code & 0xff));
    chksum += (code & 0xff); /* cmd */
    ioctl(handle, 3000, ((length+2)<<8) + chksum); /* add checksum */
    
    return ioctl(handle, 3002, length+3);
}


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval,i;

    /* this enables all channels, and sets the transfer method to
       4-serial-bits, MSB first */
     uint8_t reset_sequence[8]={0,0,0,0, 0x11, 0x11, 0x01 ,0x10};
    //uint8_t reset_sequence[8]={0x00,0x00,0,0x0, 0x00, 0x0, 0x00 ,0x11};
     uint8_t reseq2[4]={0, 0xf6,0,0xf6};

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    retval=ioctl(handle, Reset_DDS_unit);
    printf("reset retval: %d\n",retval);

    retval=ioctl(handle, IOupdate_on);
    printf("ioupdate retval: %d\n",retval);

    retval=ioctl(handle, Start_Transfer);
    printf("start retval: %d\n",retval);

    /* copy DDS reset code into data field */
    //retval=send_sequence(handle, 8, reset_sequence);
    //retval=send_sequence2(handle, Reset_DDS_unit);

    ioctl(handle,RequestStatus,2);
    retval=ioctl(handle, 2000);
    printf("transaction cnt: %d  ",retval);
    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("GPIFTRIG retval: %d\n",retval);

    retval=write(handle, reset_sequence, 8);
    printf("return value from write: %d\n", retval);

    ioctl(handle,RequestStatus,2);
    retval=ioctl(handle, 2000);
    printf(" transact ct retval: %d  ",retval);
    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("EP2CS retval: %d\n",retval);

	printf("continue >0, stop 0:");scanf("%i",&i);

    retval=write(handle, reseq2,4);
    printf("return value from write: %d\n", retval);
    
    ioctl(handle,RequestStatus,2);
    retval=ioctl(handle, 2000);
    printf(" transact ct retval first repeat: %d",retval);
    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("EP2CS retval: %d\n",retval);


    do {
	printf("continue >0, stop 0:");scanf("%i",&i);
	if (i) break;
	
	retval=write(handle, reseq2,2);
	//retval=send_sequence(handle, 2, reseq2);
	printf("return value from write: %d\n", retval);


	ioctl(handle,RequestStatus,2);
	retval=ioctl(handle, 2000);
	printf(" transact ct retval: %d  ",retval);
    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("EP2CS retval: %d\n",retval);


    } while (1);

    retval=ioctl(handle, Stop_Transfer);
    printf("stop stat: %d\n",retval);

    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("EP2CS retval: %d\n",retval);


    retval=ioctl(handle, Start_Transfer);
    printf("start stat: %d\n",retval);

    ioctl(handle,RequestStatus,1);
    retval=ioctl(handle, 2000);
    printf("EP2CS retval: %d\n",retval);


    retval=ioctl(handle, Stop_Transfer);
    printf("stop stat: %d\n",retval);


    close(handle);
    
    return 0;

}

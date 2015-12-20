/* Demo program to test the IOUpdate_regular mode for a continuous sweep
   of the the DDS with a long parameter file.
   
   This program handles the EP1 commands with ioctl() calls, and the larger
   data transfer to EP2 with a write command, following the linux  device
   driver structure. The program can just be called and needs no parameters.
   It currently generates a frequency sweep from 5 MHz to 55 MHz in about 4
   seconds on both channels.

 */

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>

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


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval,k,i;				
    double f0;
    unsigned int f;
    unsigned char *message;

    message = (unsigned char *)malloc(2500000);
    /* this enables all channels, and sets the transfer method to
       4-serial-bits, MSB first */
    uint8_t primary_setup[23] = {
	0x01, 0xa8, 0x00, 0x20, 0x00, 0xf6, 0x03, 0x00,
	0x03, 0x00, 0x00, 0xf6, 0x04, 0x05, 0x1e, 0xb8,
	0x51, 0x00, 0xf6, 0x06, 0x00, 0x13, 0xff };
    uint8_t sec_setup[10] = {0x04, 0x04, 0x04, 0x04, 0x04};


    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    retval=ioctl(handle, Full_DDS_Reset );
    retval=ioctl(handle, Stop_Transfer );
    retval=ioctl(handle, IOupdate_on);
    retval=ioctl(handle, Start_Transfer );

    /* prepare singletone mode  */
    retval=write(handle, primary_setup, 23);
    printf("return value from write: %d\n", retval);
    retval=write(handle, sec_setup, 5);

    // switch mode
    ioctl(handle, Stop_Transfer);
    /* This is to indicate ioupdate after each 5 bytes plus some wait
       total duration: 5*2 + 2 + 228 = 240 clock cycles @30 MHz = 8 usec */
    ioctl(handle, IOUpdate_regular, 5+256*228);
    ioctl(handle, Start_Transfer);


    /* generate a list of frequencies from 5 MHz to 55 MHz,
       should last 4 sec. needs about 500k steps. */
    for (i=0; i<500000; i++) { /* loop through all steps */
	k=5*i; 
	message[k]=0x04; /* freq tuning address */
	f0=((1ll<<32)/500000000.*(5e6+100*i));
	f=(unsigned int) f0;
	message[k+4]=f & 0xff;
	message[k+3]=(f>>8) & 0xff;
	message[k+2]=(f>>16) & 0xff;
	message[k+1]=(f>>24) & 0xff;
    }
    
    /* send it out */
    for (i=0;i<1;)  retval=write(handle, &message[0], 2500000);
    printf("return value from write: %d\n", retval);

    close(handle);
    
    return 0;

}

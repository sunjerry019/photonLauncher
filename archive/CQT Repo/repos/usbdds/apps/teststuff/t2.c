/* program to send a pattern to the digital output card - 
   cleanup stage for dirty commands
 */

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

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval,i;

    /* this enables all channels, and sets the transfer method to
       4-serial-bits, MSB first */
    uint8_t reset_sequence[8]={0,0,0,0, 0x11, 0x11, 0x01 ,0x10};
    uint8_t config_string[19]={ /* single tone version, both outputs
				   at 23.45 MHz */
	0x00, 0xf6, /* CSR to both channels */
	//0x01, 0xa8, 0x00, 0x20, /* FR1; standard config singele tone */
	0x01, 0xa8, 0x23, 0x20, /* FR1; standard config 16 level modulation */
	0x04, 0x0c, 0x01, 0xa3, 0x6e, /* CTW0 corresp 23,450 kHz */
	0x06, 0x00, 0x11, 0xff, /* ACR, corresp to half amplitude */
	0x03, 0x80, 0x00, 0x00, /* CFR; FM modulation */

    };
    
    uint8_t freqset[7] = { /* set frequency of channel 0 */
	//0x00, 0x76, /* CSR only channel 0 */
	 0x04, 0,0,0,0
     };
    unsigned long long f3; /* for doing the frequency - index conversion */

    /* which frequency is stored where */
    int register_list[16] = {4,10,11,12, 13,14,15,16, 17,18,19,20, 21,22,23,24};
    int reg;
 
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    retval=ioctl(handle, Get_Firmware_Version);
    printf("firmware version: %x\n",retval);

    //retval=ioctl(handle, Reset_DDS_unit);
    //retval=ioctl(handle, Full_DDS_Reset );
    //printf("reset retval: %d\n",retval);

    retval=ioctl(handle, Start_Transfer);
    //printf("start retval: %d\n",retval);
    
 
    /* copy DDS reset code into data field */
    //retval=write(handle, reset_sequence, 8);

    /* send basic configuration string to device */
    retval=write(handle, config_string, 15);
    printf("write config retval retval: %d\n",retval);

    /* now an attempt to write in the cfg register */
    retval=write(handle, &config_string[15], 4);
    printf("write config retval retval: %d\n",retval);
   
 
    do {
	printf("Enter a register (0-15) and freqency in MHz >0, or  stop with  0:");
	scanf("%i %i",&reg, &i);
	if (reg<0 || reg>15) continue; /* try again */
	
	if (i==0) break;
	f3=((unsigned long long)i<<32)/500;
	i=f3;
	freqset[0]=register_list[reg]; /* specify register address */
	freqset[1]=(i>>24)&0xff;
	freqset[2]=(i>>16)&0xff;
	freqset[3]=(i>>8)&0xff;
	freqset[4]=(i>>0)&0xff;

	retval=write(handle, freqset, 5);
	
    } while (1);

    retval=ioctl(handle, Stop_Transfer);

    close(handle);
    
    return 0;

}

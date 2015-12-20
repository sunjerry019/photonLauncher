/* program to send a pattern to the digital output card - 
   by now, this version only uses the EP2 send commands via the write method.
   You can set frequencies, modulation methods, and all kind of stuff just by
   sending the correct configuration bytes to the DDS device node in correct
   binary.
   Usually after each write section (once the FIFO falls empty), a IOUPDATE is
   issued and the changes take effect.

   The only thing to keep in mind when modifying the CSR register for addressing
   different channel registers is to keep the last nibble to 0x06. This
   keeps the DDS unit in the mode the USB chip is programmed for.

   if things go south, there should be a cleanup program which brings the
   unit back into a clean state via ioctl() commands; a reset of the DDS unit
   should work as well, but that's a bit brutal....


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

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval,i;

    /* this enables all channels, and sets the transfer method to
       4-serial-bits, MSB first */
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


    close(handle);
    
    return 0;

}

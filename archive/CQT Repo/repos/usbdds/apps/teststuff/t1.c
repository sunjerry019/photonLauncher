/* program to send a pattern to the digital output card - first testings */

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
    uint8_t reset_sequence[16]={0,0,0,0, 0x11, 0x11, 0x01 ,0x10};
     uint8_t config_string[15]={ /* single tone version, both outputs
				    at 23.45 MHz */
	 0x00, 0xf6, /* CSR to both channels */
	 0x01, 0xa8, 0x00, 0x20, /* FR1; standard config singele tone */
	 0x04, 0x0c, 0x01, 0xa3, 0x6e, /* CTW0 corresp 23,450 kHz */
	 0x06, 0x00, 0x13, 0xff /* ACR, corresp to full amplitude */
     };
     uint8_t cfg2[17] = {//0x88,
			 0,0,0,0x01, 0x10,0x10,0x10,0,
			 0,0,0,0, 0x0,0x00,0,0,
     };
     uint8_t cfg3[17] = {//0x88,
			 0,0,0,0x01, 0x10,0x01,0x01,0,
			 0,0,0,0, 0x0,0x00,0,0,
     };

 
    uint8_t freqset[7] = { /* set frequency of channel 0 */
	//0x00, 0x76, /* CSR only channel 0 */
	 0x04, 0,0,0,0
     };
    unsigned long long f3;
     uint8_t resetseq2[2] = {0x00, 0xf6};

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    retval=ioctl(handle, Get_Firmware_Version);
    printf("firmware version: %x\n",retval);

    //retval=ioctl(handle, Get_Board_Version);
    //printf("board version: %x\n",retval);

    //retval=ioctl(handle, Get_Base_Chip);
    //printf("base chip: %d\n",retval);  

    //retval=ioctl(handle, Get_Reference_Freq);
    //printf("reference freq: %d Hz\n",retval);

    //retval=ioctl(handle, Get_Serial_Number);
    //printf("Serial number of card: %d\n",retval);


    retval=ioctl(handle, Reset_DDS_unit);
    printf("reset retval: %d\n",retval);

    printf("waiting until next sequence...");scanf("%d",&retval);

    //retval=ioctl(handle, IOupdate_on);
    //printf("ioupdate on retval: %d\n",retval);

    retval=ioctl(handle, Start_Transfer);
    printf("start retval: %d\n",retval);
    
 
    /* copy DDS reset code into data field */
    retval=write(handle, reset_sequence, 8);
    //retval=send_sequence(handle, 16, cfg3);
    printf("return value from write: %d\n", retval);

    printf("waiting until next sequence...");scanf("%d",&retval);

    /* send basic configuration string to device */
    retval=write(handle, config_string, 15);
    //retval=send_sequence(handle, 16, cfg2);
    printf("return value from config write: %d\n", retval);
    
    do {
	printf("freq >0, stop 0:");scanf("%i",&i);
	if (i==0) break;
	f3=((unsigned long long)i<<32)/500000000;
	i=f3;
	freqset[1]=(i>>24)&0xff;
	freqset[2]=(i>>16)&0xff;
	freqset[3]=(i>>8)&0xff;
	freqset[4]=(i>>0)&0xff;
	//retval=write(handle, config_string,6);
	retval=write(handle, freqset, 5);

	
	printf("return value from write: %d\n", retval);
	
    } while (1);

    retval=ioctl(handle, Stop_Transfer);
    printf("stop stat: %d\n",retval);

    close(handle);
    
    return 0;

}

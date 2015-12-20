/* 
  program to test elements of the listplay mode; prepares the F2 into a state
  that directs EP2 messages into the internal buffer. For initial testing 


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

/* this code fills the buffer with a control word for a tuning info */
void maketuningword(unsigned char *buffer, int frequency) {
  unsigned long long tempbuf;
  tempbuf=0x100000000ll*frequency;
  tempbuf = tempbuf / 500000000;
  buffer[0]=0; buffer[1]=0xf6; /* both channels */
  buffer[2]=0x04; /* frequency tuning word */
  buffer[3]=(tempbuf>>24) & 0xff;
  buffer[4]=(tempbuf>>16) & 0xff;
  buffer[5]=(tempbuf>>8) & 0xff;
  buffer[6]=tempbuf & 0xff;

}

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval, i;

    unsigned char configtable[10000]={
      0x12, 0x34, 0x56, 0x78, 0x90,0xab, 0xcd, 0xef,
      0xa1, 0xb1, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    };

    
 
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    /* send basic configuration string to device */
    // retval=ioctl(handle, Full_DDS_Reset);
    //printf("device was reset; retval: %d\n",retval);

    /* now an attempt to set device in listplay mode  10 entries per click */
    retval=ioctl(handle,Stop_Transfer ); 
    //printf("transfer stopped. retval: %d\n",retval);
    retval=ioctl(handle,ListplayMode, 7 +10*256); /* 10 entries */
    //retval=ioctl(handle,IOUpdate_regular, 7+10*256 ); /* 10 entries */
    //printf("set in listplay mode; retval: %d\n",retval);

    retval=ioctl(handle,StartListplayMode);
    //retval=ioctl(handle,Start_Transfer);
    //printf("start mode; retval: %d\n",retval);


    /* transfer of some stuff into the device */

    for (i=0; i<1000; i++) {
      maketuningword(&configtable[i*7], 2000*(i+1));
    }
    retval=write(handle, configtable, 7*1000);
    //printf("index:: %d, write stuff to EP2; retval: %d\n",i,retval);


    /* read back various settings */
    //retval=ioctl(handle,Get_Buffer_bytecount ); 
    //printf("bytecount:. retval: %d\n",retval);
    //retval=ioctl(handle,Get_Buffer_writeindex ); 
    //printf("writeindex:. retval: %d\n",retval);
    //retval=ioctl(handle,Get_Buffer_readindex ); 
    //printf("Get_Buffer_readindex retval: %d\n",retval);

    /*for (j=0; j<128;j+=16) {
      for (i=0; i<16; i++) {
	retval=ioctl(handle, ListplayLseek, i+j ); 
	retval=ioctl(handle,Get_Buffer_content);   
	printf("%02x ",retval);
      }
      printf("\n");
    }
    */
    //retval=ioctl(handle,Get_Buffer_bytecount ); 
    //printf("bytecount:. retval: %d\n",retval);
    //retval=ioctl(handle,Get_Buffer_writeindex ); 
    //printf("writeindex:. retval: %d\n",retval);
    //retval=ioctl(handle,Get_Buffer_readindex ); 
    //printf("Get_Buffer_readindex retval: %d\n",retval);
    

    //retval=ioctl(handle,Get_Buffer_content);   
    //printf("calls: %d\n",retval);

    /* for (i=0;i<5;i++) {
      ioctl(handle,RequestStatus,1);
      retval=ioctl(handle,Read_EP1_8bit); 
      printf("GPIFTRIG: %d; ",retval);

      ioctl(handle,RequestStatus,2);
      retval=ioctl(handle,Read_EP1_8bit); 
      printf("TCB0: %d;",retval);

      ioctl(handle,RequestStatus,0);
      retval=ioctl(handle,Read_EP1_8bit); 
      printf("EP6CS: %d\n",retval);

      sleep(1);
    }
    */

    retval=ioctl(handle,Get_Buffer_content);   
    printf("2nd round: calls: %d\n",retval);
   
    //retval=ioctl(handle,StopListplayMode);
    //retval=ioctl(handle,Stop_Transfer);
    //printf("start mode; retval: %d\n",retval);

    //retval=ioctl(handle,IOupdate_on);
    //retval=ioctl(handle,Start_Transfer);

    //retval=ioctl(handle, Full_DDS_Reset);
    //printf("device was reset; retval: %d\n",retval);


    close(handle);
    
    return 0;

}

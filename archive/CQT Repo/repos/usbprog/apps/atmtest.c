/* This program tests the Atmel programmer. First, there will only be a few
   initial tests.

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "usbprog_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "Error returned from ioctl call",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/usbprog0"

/* this is some silly byte order thing when transmitting stuff via int */
int reversebytes(int x) {
  return ((x>>24) & 0xff) | ((x>>8) & 0xff00) | 
    ((x<<8) & 0xff0000) | ((x<<24) & 0xff000000);
}
/* some code snippets that conform to the atmel programming routines.
   they return zero on success or an error code > 0 . */
int programming_enable(int handle) {
  int retval;
  retval = reversebytes(ioctl(handle, reversebytes(0xac530000)));
  retval = (retval >>16)&0xff; /* isolate second return byte */
  if (retval != 0x53) { /* test if echo is correct */
    fprintf(stderr,"return byte is: %02x.",retval);
    return 3; /* wrong response */
  }
  return 0;
}
int chip_erase(int handle) { /* This is supposed to clear the flash */
  int retval;
  retval=ioctl(handle, reversebytes(0xac800000));
  return retval?4:0; /* test if some error occured */
}
/* this reads a single byte; the address is a byte address */
int read_prog_memory(int handle, int address) {
  int wordadr,hilo,retval;
  wordadr = (address & 0x1ffe )<< 7; /* shift it at correct place already */
  hilo = (address & 1)?0x08000000:0; /* hi/low byte selection */
  retval=ioctl(handle, reversebytes(0x20000000 | hilo | wordadr));
  return reversebytes(retval) & 0xff;
}
/* this preloads a single byte; pageoffset is a byte address within a page */
int load_prog_memory(int handle, int pageoffset, int value) {
  int adr, hilo;
  adr = (pageoffset & 0x3e )<< 7; /* shift it at correct place already */
  hilo = (pageoffset & 1)?0x08000000:0; /* hi/low byte selection */
  ioctl(handle, reversebytes(0x40000000 | hilo | adr | (value & 0xff)));
  return 0; /* test if some error occured */  
}
/* send page into flash; address is byte adr */
int write_mem_page(int handle, int address){
  int wordadr;
  wordadr = (address & 0x1ffe )<< 7; /* shift it into correct place already */
  ioctl(handle, reversebytes(0xc0000000 | wordadr));
  return 0;
}
/* this reads a single byte; the address is a byte address */
int read_eeprom(int handle, int address) {
  int adr, retval;
  adr = (address & 0x1f )<< 8; /* shift it at correct place already */
  retval=ioctl(handle, reversebytes(0xa0000000 | adr));
  return reversebytes(retval) & 0xff;
}
/* this writes a single byte; the address is a byte address */
int write_eeprom(int handle, int address, int value) {
  int adr;
  adr = (address & 0x1f )<< 8; /* shift it at correct place already */
  ioctl(handle, reversebytes(0xc0000000 | adr | (value & 0xff)));
  return 0;
}
/* this reads the lockbits */
int read_lockbits(int handle) {
  int retval;
  retval=ioctl(handle, reversebytes(0x58000000 ));
  return reversebytes(retval) & 0xff;
}
/* this writes the lockbits */
int write_lockbits(int handle, int value) {
  ioctl(handle, reversebytes(0xace000c0 | (value & 0x3f)));
  return 0;
}
/* this reads a signature byte; the address is 0..3 */
int read_signature(int handle, int address) {
  int adr, retval;
  adr = (address & 0x3 )<< 8; /* shift it at correct place already */
  retval=ioctl(handle, reversebytes(0x30000000 | adr));
  return reversebytes(retval) & 0xff;
}
/* this reads the fusebits */
int read_fusebits(int handle) {
  int retval;
  retval=ioctl(handle, reversebytes(0x50000000 ));
  return reversebytes(retval) & 0xff;
}
/* this writes the fuse bits */
int write_fusebits(int handle, int value) {
  ioctl(handle, reversebytes(0xaca00000 | (value & 0xff)));
  return 0;
}
/* this reads the high fusebits */
int read_fusebits_high(int handle) {
  int retval;
  retval=ioctl(handle, reversebytes(0x58080000 ));
  return reversebytes(retval) & 0xff;
}
/* this writes the high fuse bits */
int write_fusebits_high(int handle, int value) {
  ioctl(handle, reversebytes(0xaca80000 | (value & 0xff)));
  return 0;
}
/* reads one calibration byte, adr; 0..3 */
int read_calibration(int handle, int address) {
  int adr, retval;
  adr = (address & 0x3 )<< 8; /* shift it into correct place already */
  retval=ioctl(handle, reversebytes(0x38000000 | adr));
  return reversebytes(retval) & 0xff;
}

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval=0;
    int option, parameter;

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d; ",errno);
	return -emsg(1);
	}

    /* here comes test stuff. We have a simple parser loop */
    do {
      printf("actions:\n0: exit, 1: Reset Target, 2: Unreset target, 3: send word, 4: set delay >");
      scanf("%d",&option);
      switch(option) {
      case 0: /* end */
	break;
      case 1: /* reset target */
	retval=ioctl(handle,Reset_Target);
	printf(" return value: %d\n:",retval);
	if (retval) return -emsg(2);
	break;
      case 2: /* unreset target */
	retval=ioctl(handle,Unreset_Target);
	printf(" return value: %d\n:",retval);
	if (retval) return -emsg(2);
	break;
      case 3: /* send data */
	printf("Enter data to send (in hex): ");scanf("%i",&parameter);
	retval=ioctl(handle,Send_Word,parameter);
        printf("Sent: %08x, return value: %08x\n",parameter,retval);
	break;
      case 4: /* Set delay */
	printf("Enter delay value: ");scanf("%i",&parameter);
	retval=ioctl(handle,Set_Delay,parameter);
	printf(" return value: %d\n:",retval);
	if (retval) return -emsg(2);
	break;
      default:
	printf("Option not implemented. Use 0 to exit.\n");
	break;
      }
    } while (option);
    
    close(handle);
    
    return 0;

}

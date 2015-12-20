/* This program sends acquires the debug port of the PSOC in the SWD mode, and 
   switches the interface over to JTAG mode.

   Seems the SWD programming is a bit stuck, thus this little helper app.

   Intent is to acquire the device, and do a device ID check.

   first code      7.12.2010

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
// #include <math.h>

#include "usbprog_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "Error returned from ioctl call while port acquire",
  "IOCTL error in SWD_read call",
  "Some error in read-from-address call",

};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/usbprog0"

/* helper code to transfer int to mem adress */
void int2data(int a, char *data) {
  int i;
  int b=a;
  for (i=0; i<4; i++) {
    data[i] = b & 0xff;
    b>>=8;
  };
}
/* careful - data is a char[5] thing */
int data2int(unsigned char *d2) {
  return d2[1] + (d2[2]<<8) + (d2[3]<<16) + (d2[4]<<24);
}

/* code to retreive the device ID word via SWD. On Error, -1 is returned */
int Get_Device_ID(int handle) {
  unsigned char d2[5];
  int ev;
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare address select to IDACCESS in DP space */
  d2[0]=0xa5; /* address bits = 00, DP access, read, odd parity */
  ev=ioctl(handle, SWD_Read, &d2);
  if (ev) return -1; /* not nice but what can you do... */
  if ((d2[0]&7) != 1) {
    printf("Warning: Device ID read attempt did not get proper ack.\n");
  }
  retval=data2int(d2);
  //printf("ID req Ack status: %02x; data: %08x; ioctl returns: %08x\n",d2[0],retval,ev);
  return retval;
}
/* write data to PSOC space ; uses a 24 bit address, and 32 bit data.
   returns -1 on io error. */
int Write_To_Address(int handle, int address, int data) {
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare writing of address */
  d2[0]=0x8b; /* address bits = 01, AP access, write, even parity */
  int2data(address,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  printf("Adr write ack: %02x;",d2[0]);
  /* write data */
  d2[0]=0xbb; /* address bits = 11, AP access, write, odd parity */
  int2data(data,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  printf("data write ack: %02x;",d2[0]);
  return 0;
}

/* reads data from PSOC space ; uses a 24 bit address. the data is
   returned in the 32 bit data pointer. returns -1 on io error, 0 on success. */
int Read_From_Address(int handle, int address, int *data) {
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare writing of address */
  d2[0]=0x8b; /* address bits = 01, AP access, write, even parity */
  int2data(address,&d2[1]);
  if (ioctl(handle, SWD_Write, &d2)) return -1;
  printf("Adr write ack: %02x; ",d2[0]);
  /* dummy read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("dummy read ack: %02x; ",d2[0]);
  /* real read */
  d2[0]=0x9f; /* address bits = 11, AP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("real read ack: %02x; rest: %02x %02x %02x %02x\n",d2[0], d2[1], d2[2], d2[3], d2[4]);
  *data = data2int(d2);
  return 0;
}

/* helper code to read from DBGPRT_CFG */
int Read_dbg(int handle){
  unsigned char d2[5]; /* for usb transfer */
  unsigned int retval; /* hope ths gets msb right? */
  /* prepare writing of address */
  d2[0]=0x8d; /* address bits = 01, dP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("dummy read ack: %02x; ",d2[0]);

  d2[0]=0x8d; /* address bits = 01, dP access, read, even parity */
  if (ioctl(handle, SWD_Read, &d2)) return -1;
  printf("real read  ack: %02x; ",d2[0]);


  return data2int(d2);
}

int main(int argc, char *argv[]){
  int handle; /* file handle for usb device */
  int retval=0, retdata=0;
    FILE *inhandle = stdin; /* temporary version */
    char data[100]; /* parameter for communication with device driver */
   
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }
    /* try to acquire device */
    data[0]=1;
    retval=ioctl(handle, SWD_Acquire, data);
    if (retval) return -emsg(2);
    printf("Return value of ack: 0x%02x\n",data[0]);

    /* try to read device ID */
    retval=Get_Device_ID(handle);
    if (retval==-1) return -emsg(3); /* read call failed */
    printf("Reproted device ID in SWD mode:: 0x%08x\n",retval);


    /* Issue the SWD reset sequence */
    ioctl(handle, SWD_Reset, 60);
    /* Issue the switchover command from SWD to JTAG */

    ioctl(handle, SWD_Sendword, 0xe73c);


    printf("Device should now be in JTAG mode.\n");


    close(handle);
    
    return 0;

}

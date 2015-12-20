/* This program can be used to issue a "clear EEPROM" command - such a command
   clears the first 10 bytes of the firmware flash, and should allow to
   reprogram it later on. Make sure that the write protection is disabled on
   the serial EEPROM. 
   
   This is sort of an emergency program, one step before soldering out an
   EEPROM which cannot be restarted in diag mode. You are completely on your
   own when using it.

   Call it once, and see if the card comes up in the development kit identity
   after a cold reboot of the target device.

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
  "timing out of range",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/usbprog"

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval=0;
    char responsestring[100];

    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d; ",errno);
	return -emsg(1);
	}

    printf("Are you really, really, really sure you want to clear the firs ten bytes of the EEPROM (yes/no) ?");
    scanf("%100s",responsestring);
    if (strncmp(responsestring,"yes",3)) {
      printf("clearing procedure aborted.\"");
      return 0;
    }

    retval=ioctl(handle, 254);
    printf("Clear EEPROM command issued.\nReturn value from driver: retval: %d\n",retval);

    close(handle);
    
    return 0;

}

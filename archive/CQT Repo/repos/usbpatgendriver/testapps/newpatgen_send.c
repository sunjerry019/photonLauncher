/* program to send a pattern to the new pattern generator. Takes a file name,
   and transfers its content into the pattern generator. this is transient
   code, should be replaced by a simpler serial interface. 


   usage: newpatgen_send [-d devicename] [-r routemode] [-R |-A |-I] srcfile
   
   Options:
   -d devname Communicate with the device specified in devname rather than
              the default device /dev/ioboards/pattgen_generic_0

   -r route   sets the routing mode register. Defaults to 0.

   -R         switches into run mode after the upload. This is the default.
   -A         switches into alternate run mode after upload.
   -I         switches into idle mode after upload.

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include "usbpattgen_io.h"
#include <unistd.h>
#include <sys/ioctl.h>

/* error handling */
char *errormessage[] = {
  "No error.",
  "Unable to open USB device.", /* 1 */
  "cannot parse device file name",
  "cannot parse route mode (integer 0..255 or hex value)",
  "missing source file name (or - for stdin)",
  "cannot open source file", /* 5 */
  
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"
#define DEFAULT_CARDMODE 1

int main(int argc, char *argv[]) {
  int handle; /* file handle for usb device */
  char devicefilename[200]=DEFAULT_DEVICENAME; /* name of device */
  char sourcefilename[200]=DEFAULT_DEVICENAME; /* name of device */
  int opt;
  int cardmode = DEFAULT_CARDMODE; /* mode in which card is left after upload.
				     0: idle, 1: run, 2: alternate run */
  int routemode = 0; /* what to fill into route register */
  int inhandle=0; /* stdin as default */
        
  /* parse arguments */
  opterr=0; /* be quiet when there are no options */
  while ((opt=getopt(argc, argv, "d:r:RAI")) != EOF) {
    switch (opt) {
    case 'd': /* select device name */
      if (1!=sscanf(optarg,"%199s",devicefilename)) return -emsg(2);
      devicefilename[199]=0; /* safety termination */
      break;
    case 'r': /* set route mode */
      if (1!=sscanf(optarg,"%i",&routemode)) return -emsg(3);
      routemode &= 0xff;
      break;
    case 'R': /* switch into runmode after upload */
      cardmode=1;
      break;
    case 'A': /* switch into alt run mode after upload */
      cardmode=2;
      break;
    case 'I': /* switch into idle mode after upload */
      cardmode=0;
      break;
    }
  }
  
  /* take file name */
  if (optind>=argc) return -emsg(4);
  if (strcmp("-",argv[optind])) {
    inhandle=open(argv[optind],O_RDONLY);
    if (inhandle==-1) return -emsg(5);
  } 
  
  /* open device file */
  handle=open(devicefilename,O_RDWR);
  if (handle==-1) return -emsg(1);

  /* reset device */
  /* switch to upload mode */
  /* copy file into RAM */
  /* switch to desired mode */
  /* close file handle if non stdin */
  
  return 0;
}



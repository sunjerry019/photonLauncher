/* program to set the frequency of the clock generator on the new boards. 
   This is to provide a clock source to the pattern generator. 

   The frequency can range form xxx to yyy MHz, with a resolution of zzz.
   The same code can be used to set the frequency of the aux output.

   usage: usbrfgenset [-d devicename] [-e | -i] [-f frequency] [ -q]
   
   Options:
   -e         use external 10 MHz frequency reference.
              Legacy option for compatibility, ignored

   -i         use internal 10 MHz crystal. Legacy option for
              compatibility, ignored

   -f freq    choose a given output frequency (in MHz). The default is 
              100.0 MHz, corresponding to a fast clock step of 20 ns for
	      the pattern generator.

   -q         quiet option. If this option is NOT used, the program returns
              the exact frequency it is using in approximation to the 
	      specified frequency, as the PLL can only provide certain
	      frequency steps.
   -d devname Communicate with the device specified in devname rather than
              the default device /dev/ioboards/pattgen_generic_0
   -p phase   sets relative phase for the main or aux channel.
              default is 0.
   -A         selects aux frequency channel instead of main channel.
   -R         do a reset of the clock chip before settingfrfequency. Keep
              in mind that this resets the frequency of both channels to
	      the firmware defaults.

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
  "error parsing frequency argument.",
  "error sending USB command for RF initialize",
  "error sending USB command for clock source selection",
  "Frequency out fo range", /* 5 */
  "Frequency below VCO capability",
  "Frequency above VCO capability",
  "Main PLL divider out of range",
  "Error submitting RFsource config over USB",
  "Cannot parse device file name",  /* 10 */
  "Cannot parse phase value",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};




#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"
int main(int argc, char *argv[]) {
    int handle; /* file handle for usb device */
    char devicefilename[200]=DEFAULT_DEVICENAME; /* name of device */
    int opt;
    int Resetoption=0; /* by default, no reset before setting frequency */

    float inputfreq = 10.0; /* target frequency in MHz */
    int quietoption=0;
    int RFtarget = 0 ; /* 0: main 1: aux */
    int phasevalue = 0; /* phase setting for clock chip */
    int divider = 1;  /* for PLL setting */
    int retval;
        
    /* parse arguments */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "ieqf:p:AR")) != EOF) {
      switch (opt) {
      case 'i': case 'e': /* legacy */
	break;
      case 'q':
	quietoption=1; /* no reply */
	break;
      case 'f': /* read frequency */
	if (1!=sscanf(optarg, "%f",&inputfreq)) return -emsg(2);
	break;
      case 'd': /* device name */
	if (1!=sscanf(optarg,"%199s", devicefilename)) return -emsg(10);
	devicefilename[199]=0; /* safety measure */
	break;
      case 'A': /* choose aux channel */
	RFtarget=1;
	break; 
      case 'R': /* reset option */
	Resetoption=1;
	break;
      case 'p': /* set phase value */
	if (1!=sscanf(optarg, "%i",&phasevalue)) return -emsg(11);
	break;
      }
    }
    
    handle=open(devicefilename,O_RDONLY);
    if (handle==-1) return -emsg(1);
    
    
    /* initialize RF source */
    if (Resetoption) 
      if (ioctl(handle, InitializeRFSRC)) return -emsg(3);

    /* check frequency range and convert it into divider rate. The main
       clock frequency is 400 MHz */
    if ((inputfreq>400.) || (inputfreq<0.390625)) return -emsg(5);
    divider = 400./inputfreq - 1;
    if (divider<0) divider=0;
    if (divider>1023) divider=1023;
    retval=ioctl(handle,
		 RFtarget?Send_AUXRF_parameter:Send_RF_parameter,
		 (((phasevalue & 0x3f)<<10) | (divider & 1023)));
    if (retval) {
      printf("error code: %d\n",retval);
      return -emsg(9);
    }
    
    /* return true frequency */
    if (!quietoption) printf("%f\n",400./(divider+1));
    
    return 0;
}

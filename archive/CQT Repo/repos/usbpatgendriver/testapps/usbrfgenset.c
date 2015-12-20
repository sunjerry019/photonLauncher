/* program to set the frequency of the onboard PLL generator. This is to 
   provide a clock source to the pattern generator. 

   The frequency can range form xxx to yyy MHz, with a resolution of zzz.
   The PLL can be referenced either to an internal crystal oscillator or an
   external reference input

   usage: usbrfgenset [-d devicename] [-e | -i] [-f frequency] [ -q]
   
   Options:
   -e         use external 10 MHz frequency reference for the PLL

   -i         use internal 10 MHz crystal oscillator for PLL

   -f freq    choose a given output frequency (in MHz). The default is 
              100.0 MHz, corresponding to a fast clock step of 20 ns for
	      the pattern generator.

   -q         quiet option. If this option is NOT used, the program returns
              the exact frequency it is using in approximation to the 
	      specified frequency, as the PLL can only provide certain
	      frequency steps.
   -d devname Communicate with the device specified in devname rather than
              the default device /dev/ioboards/pattgen_generic_0

  This program assumes that there is only one device connected to the host.

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
  "Reference frequency out fo range", /* 5 */
  "Frequency below VCO capability",
  "Frequency above VCO capability",
  "Main PLL divider out of range",
  "Error submitting RFsource config over USB",
  "Cannot parse device file name",  /* 10 */
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};


/* transmit testregister t, output divider n, main divider m bits to the
   rf source chip; returns 0 on success */
int _rfsource_set_registers(int handle, int t, int n, int m){
    int u, retval;
    if (t & ~7) return -1; /* t range overflow */
    if (n & ~3) return -1; /* output divider overflow */
    if (m & ~0x1ff) return -1; /* main divider overflow */
    
    /* assemble data word and transmit the 14 bits to the usb device */
    u=((t & 7)<<11) | ((n & 3)<<9) | (m & 0x1ff);
    retval=ioctl(handle, Send_RF_parameter, u); /* error treatment?? */
    return retval;
}

/* optimize frequency assuming a reference freq. returns exact freq or <0
   on error. All Frequencies are given in kilohertz. */
int adjust_rfsource(int handle, int ftarget, int fref){
  int np; /* out_divider power; division ratio 2,4,8,1 for np=0,1,2,3 finally*/
  int m; /* main divsion ratio */
  int tmp;
  if (fref<10000 || fref>20000) return -5; /* reference out of range */
  if (ftarget <50000) return -6;/* frequency below VCO capability */
  if (ftarget>800000) return -7; /* frequency exceeds VCO capability */

  /* calculate raw division power to keep VCO between 400 and 800 MHz */
  tmp = (800000/ftarget);
  if (tmp>16) return -6; /* frequency below VCO capability */
  for (np=1;tmp>>np;np++); /* np = 1,2,3,4 for ratios 1,2,4,8*/

  //fprintf(stderr,"np:%d\n",np);

  /* calculate main divider setting */
  m=(ftarget <<(np-1))/(fref>>3); /* should give right main divider ratio */
  //fprintf(stderr,"m:%d\n",m);

  if (m<1 || m>0x1ff) return -8; /* main divider out of range */
  /* send this to the chip, test mode switched off;
     correction to np in the chip; ratio 2,4,8,1 for n_value=0,1,2,3 */
  if (_rfsource_set_registers(handle, 0,(np+2)&3,m)) return -9; /* some err */
  /* calculate generated frequency in kilohertz; true frequency may be off
   up to a kHz due to rounding */
  return fref*m/8/(1<<(np-1));
}


#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"
int main(int argc, char *argv[]) {
    int handle; /* file handle for usb device */
    char devicefilename[200]=DEFAULT_DEVICENAME; /* name of device */
    int opt;
    int retval;

    float inputfreq = 10.0; /* target frequency in MHz */
    int quietoption=0;
    int RFsource = 0 ; /* 0: internal 1: external reference */
    
        
    /* parse arguments */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "ieqf:d:")) != EOF) {
	switch (opt) {
	    case 'i': /* select internal clock reference */
		RFsource = 0;
		break;
	    case 'e': /* select external clock reference */
		RFsource = 1;
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
	}
    }

    handle=open(devicefilename,O_RDWR);
    if (handle==-1) return -emsg(1);


    /* initialize RF source */
    //not implemented? if (ioctl(handle, InitializeRFSRC)) return -emsg(3);

    /* make RF source selection */
    if (ioctl(handle, Rf_Reference, RFsource?0:1)) return -emsg(4);

    /* check frequency range and  generate PLL settings; recycle code from
       timestamp cards */
    retval = adjust_rfsource(handle, (int)(inputfreq*1000.+10), 10000);
    if (retval<0) return -emsg(-retval);


    /* return true frequency */
    if (!quietoption) printf("%f\n",retval/1000.);
    
    return 0;
}

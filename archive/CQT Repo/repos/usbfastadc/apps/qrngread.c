/* This code is a modified version of the oscilloscope code that outputs
   data processed by the scrambler. Works with 60 MHZ sample rate on the input.


   current options: 
   qrngread   [-d <devicefile>]
              [-n <numberofsamples>]
	      [-m <inputmode>]
	      [-O ]
	      [-p <prescaler>]
              [-f filename]

  data is written to the specified target file or stdout without any
  processing, directly as it comes from the acquisition device.

  OPTIONS:
   -d <devicefile>   Specify different device file. Default is currently
                     dev/ioboards/usbfastadc0.

   -n <numsamples>   Specify the number of samples to be taken. Default is
                     2000.
   -m <inputmode>    Selects input mode. following options are available:
                     0: Sample channel A with 16 bit width
		     1: Sample channel B with 16 bit width
   -O                ignore an overflow in the transfer FIFO of FX2
   -p <prescaler>    programms the prescaler in the CPLD, which tells how many
                     samples per cycle are to be skipped. default is 0. the
		     value of prescaler is an integer between 0 and 4095
		     USE WITH CARE... not every value works... to divide
		     the rate by two, you need to insert 3 wait states, to
		     divide it by k, you need to insert 2k-1 states (I think).

 
  OUTPUT OPTIONS:
   -f <filename>     output file. If this is not specificed, stdout is used.

  LOGGING OPTIONS:
   -q                quiet output. If set, no text will be sent in the main
                     loop.


  SIGNALS:
  SIGTERM, SIGPIPE,
  SIGINT:            When the process receives any of these signals, it
                     terminates data acquisition.

  History:
  22.1.2015        first version, taken from stable streamread.
		    
  ToDo: Try to make initial urb size longer so it does not run into a
         reading problem.

  
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/mman.h>
#include <signal.h>

#include "usbfastadc_io.h"

/* get a reasonably large buffer */
#define SIZE_DMA (1<<24)
#define DEFAULT_INPUTMODE 0
#define INITIAL_TRANSFERLENGTH (1<<16)

/* polling time in microseconds */
#define POLLTIME 10000
#define MBPS 40
#define GRACEBUFFER 256000

/* conversion constants */
#define conversion_offset (0x8000)
#define CONVERSION_SPAN 1.0

/* other default definitions */
#define FILENAMLEN 200
#define DEFAULT_AUTOTRIGFACTOR 50
#define DEFAULTDEVICENAME "/dev/ioboards/usbfastadc0"
#define DEFAULT_PRESCALER 0

/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot open device.", /* 1 */
  "Cannot parse device file name",
  "Error setting up clock configuration",
  "Error setting CPLD mode",
  "Error setting ADC configuration ", /* 5 */
  "Mmap failed",
  "error starting USB engine on driver side",
  "error starting limited acquisition",
  "error stopping USB engine",
  "error reading byte count",  /* 10 */
  "error resetting the device",
  "cannot parse sample number",
  "samples exceed current capability",
  "cannot parse input mode",
  "invalid input mode", /* 15 */
  "error reading transferred bytes",
  "Timeout reading in buffer",
  "Error stopping stream",
  "Cannot set overflow policy",
  "Cannot parse prescaler value", /* 20 */
  "Prescaler value not in range 0..4095",
  "Wrong trigger mode (must be 0, 1 or 2)",
  "Trigger channel out of range (0 or 1)",
  "Trigger level out of range",
  "Hysteresis makes trigger impossible", /* 25 */
  "Cannot open output file",
  
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

/* read back status registers located in 0x22c, 0x22d. parameter is handle,
   return is 0x22c in its 0..7, 0x22D in bits 8..15 */
int getstatusbits(int handle) {
  char buffer[10];
  int retval;
  buffer[0]=2; /* read back two bytes */
  buffer[1]=0x02; buffer[2]=0x2d; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  //usleep(10000);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  return (buffer[3]<<8)+buffer[4];
}
/* read back some registers */
void readregister(int handle, int adr, int num) {
  char buffer[256];
  int retval, i;
  buffer[0]=num; /* read back some bytes */
  buffer[1]=(adr >>8)&0x1f; buffer[2]=adr & 0xff; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  //usleep(10000);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  for (i=0; i<num; i++) printf("%03x: 0x%02x\n",adr-i,buffer[3+i]&0xff);

}

/* generic SPI configuration, eats a data stream and a command */
int SPI_configure(int handle, char *configdata, int command) {
  int i, l, retval;
  i=0; /* initial index */
  while ((l=configdata[i])) { /* length is non-zero */
    retval=ioctl(handle, command, &configdata[i]); /* copy data */
    //printf("length: %d, retval: %d\n",l,retval);
    usleep(10000);
    if (retval) return retval; /* an error has occured */
    i+=l+3; /* move to next sequence in data field */
  }
  return 0; /* everything went fine */
}

/* generic clock configuration. Data is stored in an array that could reside
   in the firmware at some point. Format is SPI data format, with a first byte
   describing payload size, followed by an address, then followed by the
   payload. A payload size of 0 terminates the configuration chain. */
char clock_data[] = {
  /* reset device */
  1, 0x00, 0x00,
  0x24,

  /*  PLL2 configuration: A=0, B=48 (total N: 192), pump 56uC 
      VCO2 frequency: 3840 MHz , VCOdiv=4, */
  7, 0x00, 0xf6,
  0x00, 0x00, 0x00, 0x08, 0x03, 0x30, 0x10,

  /* Output configuration channels 3..0 */
  12, 0x01, 0xa1,
  0x00, 0x1f, 0x20, /* ch 3: */
  0x00, 0x13, 0x02, /* ch 2: div by 20 ->48 MHz, LVDS3.5mA */
  0x00, 0x13, 0x08, /* ch 1: div by 20 ->48 MHz ,CMOS true phase */
  0x00, 0x1f, 0x20, /* ch 0: */

  /* Output configuration channels 5, 4 */
  6, 0x01, 0xb3,
  0x00, 0x27, 0x08, /* ch 5: /40 ->24 MHz, CMOS, true phase (IFCLK)*/
  0x00, 0x13, 0x08, /* ch 4: /20 ->48 MHz, CMOS, true phase (aux clk)*/

  /* PLL1 parameter set */
  13, 0x00, 0x1c,
  0x48, /* select refa, Vcc/2 when no signal */
  0x30, /* 0x1b: OSC_in is feedb ref, ZD is off, REFA in CMOS mode */
  0x28, /* 0x1a: REFA is enabled, REFA differential, OSCin/REFB in cmos mode */
  0x03, /* 0x19: normal operation, minimum antibacklash */
  0x0c, /* 6 uA charge pump current */
  0x00, 20, /* 0x17/0x16: PLL1 feedback divider ->20 */
  0, 1, /* reserved, rev_test divider ->1 */
  0, 1, /* REFB R divider ->1 */
  0, 10, /* REFA R divider ->10 */

  /* PLL1 ouput control */
  2, 0x01, 0xbb,
  0x80, /* PLL1 output driver off, no routing to outputs 0,1 */
  0x00, /* 0x1ba: PLL1 output divider=0, output strenght= */
  
  /* power down control of PLLs */
  1, 0x02, 0x33,
  0x0,

  /* update registers */
  1, 0x02, 0x34,
  0x01, /* reset */
  
  /* initiate calibration & update registers */
  1, 0x00, 0xf3,
  0x0a,
  1, 0x02, 0x34, 0x01,  

  /* issue a synchronize command */
  1, 0x02, 0x32, 0x01, 1, 0x02, 0x34, 0x01,
  1, 0x02, 0x32, 0,    1, 0x02, 0x34, 0x01,

  /* end of sequence */
  0
}; 


/* configure clock, eventually reconfigure dividers for alternate sig */
int clock_configure(int handle) {
  int retval;
  retval=SPI_configure(handle, clock_data, CLOCKCHIP_WRITE);
  return retval;
}

/* generic ADC configuration. */
char adc_data[] = {
  1, 0x00, 0x00,
  0x18, /* reset */
  /* user test pattern: 0x1234, 0x5678 alternating*/
  4, 0x00, 0x1c,
  0x12, 0x34, 0x56, 0x78,
  /* choose test mode -> user defined, alternate is 0x48. 00 is normal */
  1, 0x00, 0x0d,
  0x00,
  /* set transfer */
  1, 0x00, 0xff, 1,
  
  0     /* end of pattern */
};

int adc_configure(int handle) {
  return SPI_configure(handle, adc_data, ADCCHIP_WRITE);
}

/* input mode configuration */
int modeword[2]= {
  0x140,   /* channel A */
  0x180    /* channel B */
};

/* Signal handler that deal with a kill signal */
volatile int running=0;
void termsig_handler(int sig) {
    switch (sig) {
	case SIGTERM: case SIGKILL:
	    fprintf(stderr,"got hit by a term signal!\n");
	    break;
	case SIGPIPE: 
	    /* stop acquisition */
	    fprintf(stderr,"readevents:got sigpipe\n");
    }
    running=0;
}


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    FILE *outhandle = stdout;
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int i, retval, v,vold,ovlidx;
    unsigned char *startad=NULL;
    int commandedsamples=0;
    int inputmode=DEFAULT_INPUTMODE; /* different input modes.
					0: only A channel
					1: only B channel
				     */
    int term_on_overflow=1; /* by default, respect overflows */
    int prescaler=DEFAULT_PRESCALER; /* how many samples to skip per cycle */
    char outfilename[200]="";
    int looperror, oldidx, newidx, cbytes, overflowerror;
    int quietoption=0;
    //unsigned int reason; 
    //unsigned int tcb_content;
    
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:n:m:Op:f:q")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       case 'n': /* number of samples */
	 if (sscanf(optarg,"%d",&commandedsamples)!=1) return -emsg(12);
	 if (commandedsamples<1)
	   return -emsg(13); /* too many samples */
	 break;
       case 'm': /* input mode */
	 if (sscanf(optarg,"%d",&inputmode)!=1) return -emsg(14);
	 if ((inputmode<0) || (inputmode >1)) return -emsg(15);
	 break;
       case 'O': /* ignore overflow */
	 term_on_overflow=0;
	 break;
       case 'p': /* prescaler setting */
	 if (sscanf(optarg,"%d",&prescaler)!=1) return -emsg(20);
	 if ((prescaler<0) || (prescaler >4095)) return -emsg(21);	 
	 break;
       case 'f': /* output file name */
	 sscanf(optarg, "%199s",outfilename);
	 outfilename[199]=0; /* safety termination */
	 break;
       case 'q': /* quiet option */
	 quietoption=1;
	 break;
       }
    }

    vold=0;ovlidx=0;overflowerror=0;

    /* open device */
    handle=open(devicefilename,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }

    /* open output file */
    if (outfilename[0]) {
	outhandle= fopen(outfilename,"w");
	if (!outhandle) return -emsg(26);
    }

    /* send device in a clean state */
    retval=ioctl(handle, RESET_TRANSFER);
    if (retval) return -emsg(11);
    //usleep(100000);
    
    /* Basic CPLD configuration to turn on power and LED */
    retval=ioctl(handle, WRITE_CPLD_LONG,
		 0x0c | modeword[inputmode] | (prescaler<<16) );
    if (retval) return -emsg(4);
 
    /* Configuration of clock chip to provide 20 MHz to ADC and IFCLK */
    if (clock_configure(handle)) return -emsg(3);      

    //usleep(10000);
    /* set overflow policy */
    if (ioctl(handle,SET_OVERFLOWFLAG,term_on_overflow)) return -emsg(19);      

    //usleep(10000);
    /* configure ADC with something reasonable */
    if (adc_configure(handle)) return -emsg(5);
    //usleep(10000);
   
    /* Buffer preparation, start mmap and collateral */
    startad=mmap(NULL,SIZE_DMA,PROT_READ|PROT_WRITE, MAP_SHARED,handle,0);
    if (startad==MAP_FAILED) {
      printf("erno of fail: %d\n",errno);
      return -emsg(6);
    }
    for (i=0; i<SIZE_DMA; i+=4096) retval=retval+startad[i];

    /* install termination signal handlers */
    signal(SIGTERM, &termsig_handler);
    signal(SIGINT, &termsig_handler);
    signal(SIGPIPE, &termsig_handler);

    /* set initial transfer length */
    retval=ioctl(handle, Set_transferlength, INITIAL_TRANSFERLENGTH);
    if (!quietoption) {
	fprintf(stderr, "return from transferlengh: %d (0x%x)\n",
		retval, retval);
    }


    /* start acquisition */
    retval=ioctl(handle, Start_USB_machine);
    if (retval) return -emsg(7);

    /* try to get a number of entries from fx2 */
    retval=ioctl(handle, START_QSTREAM);
    if (retval) return -emsg(8);
    
    
    /* run  status */
    running=1; looperror=0; oldidx=0;
    cbytes=commandedsamples*sizeof(uint16_t);

    do { /* polling until number has been reached */
	usleep(10000); /* wait 10 msec */
	v=ioctl(handle, Get_transferredbytes);
	if (v<0) {
	    looperror=16;
	    break;
	}
	
	if (!quietoption) {
	    //  fprintf(stderr, "poll v=%d (0x%x) running: %d, cbytes: %d\n",
	    //	    v, v, running, cbytes);
	    if (v==vold) {
		fprintf(stderr, 
			"poll v=%d (0x%x) running: %d, cbytes: %d\n",
			v, v, running, cbytes);
		//running=0; overflowerror=1;
	    }
	    if (v<vold) {
		ovlidx++;
		fprintf(stderr, "2GB overflow; index: %d\n",
			ovlidx);
	    }	 
	    vold=v;

	}
	
	/* this shouldhandle a limited number of events */
	if (cbytes) {
	    if (v>cbytes) {
		v=cbytes; running=0;
	    }
	}
	
	newidx=v % SIZE_DMA;
	/* send stuff to output */
	if (newidx<oldidx) {
	    fwrite(&startad[oldidx], sizeof(char),
		   SIZE_DMA-oldidx, outhandle);
	    oldidx=0;
	}
	fwrite(&startad[oldidx], sizeof(char),(newidx-oldidx), outhandle);
	oldidx=newidx;

    } while (running && !looperror);
    
    if (looperror) return -emsg(looperror);

    /* overflow error treatment */
    if (overflowerror) {
	fprintf(stderr,"overflow error\n");
    }

    
    /* recover the irq reason thing - for debugging */
    //reason=0x12345678;
    //retval=ioctl(handle, GETRDYLINESTAT, &reason);
    //fprintf(stderr,"Returned IRQ reason: 0x%08x, return from ioctl:%d\n",
    //	    reason, retval);
    
    /* recover the terminal count register - for debugging */
    //tcb_content=0x12345678;
    //retval=ioctl(handle, GET_TCB, &tcb_content);
    //fprintf(stderr,"Returned TCB: 0x%08x, return from ioctl:%d\n",
    //	    tcb_content, retval);
 
    
    retval=ioctl(handle, STOP_STREAM);

    /* stop engine */
    retval=ioctl(handle, Stop_USB_machine);
    if (retval) {
	return -emsg(9);
    }
    
    /* switch off external IFclock */
    retval=ioctl(handle, RESET_TRANSFER);
    if (retval) return -emsg(11);

    /* switch off light  */
    retval=ioctl(handle, WRITE_CPLD_LONG,
		 0x02 | modeword[inputmode] | (prescaler<<16));
    if (retval) return -emsg(4);
 
    close(handle);
    
    return 0;

}

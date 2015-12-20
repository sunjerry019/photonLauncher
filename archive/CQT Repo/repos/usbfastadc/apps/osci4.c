/* program that tests the usage as oscilloscope. This version uses the 
   circular buffer to implement very long runs (still ToDo) cleanup, sigint
   trapping to switch off device. 
   Also: more benign error behaviour.

   current options: 
   osci1 [-d <devicefile>]
         [-n <numberofsamples>]
	 [-m <inputmode>]
	 [-O ]
	 [-q ]
	 [-p <prescaler>]
	 [-T <trigmode>]
	 [-L <triglevel>]
	 [-P <polarity>]
	 [-C <channel>]
	 [-H <hysteresis>]
	 [-D <delaytime>]


  OPTIONS:
   -d <devicefile>   Specify different device file. Default is currently
                     dev/ioboards/usbfastadc0.

   -n <numsamples>   Specify the number of samples to be taken. Default is
                     2000.
   -m <inputmode>    Selects input mode. following options are available:
                     0: Sample channel A with 16 bit width
		     1: Sample channel B with 16 bit width
		     2: Sample both A and B with 16 bit
		     3: Sample A and B with 8 bit each (take MSB)
   -O                ignore an overflow in the transfer FIFO of FX2
   -q                Quiet mode. If set, no output data will be generated,
                     only the comments in the header line.
   -p <prescaler>    programms the prescaler in the CPLD, which tells how many
                     samples per cycle are to be skipped. default is 0. the
		     value of prescaler is an integer between 0 and 4095

  TRIGGER OPTIONS:
   -T <mode>         Defines trigger mode
                     0: no content-related trigger, starts immediately. This
		        is the default trigger mode.
		     1: 'normal' trigger; waits until specified trig condition
		     2: 'auto' trigger: autotrig after delay of ....
		
   -L <level>        Specifies trigger level in volt. Default is 0.0 V
   -P <polarity>     Specifies trigger polarity. If <polarity> is a negative 
                     number, a negative trigger polarity is chosen. Default
		     is positive trigger polarity.
   -C <channel>      selects the channel in cases both channels are sampled.
                     Can be 0 or 1, default is 0.
   -H <hysteresis>   Specify how far below/above the trigger level has to be
                     before the system is armed to consider a trigger event.
		     This is to suppress triggering on noise. Dafault is 50mV.
   -D <time>         Time from trig to start_acquisition to in seconds. 
                     A positive value of <time> corresponds to a wait from
		     trigger time until acquisition starts. Default is 0.0s.

  OUTPUT OPTIONS:
   -S                scaled; output is given in seconds/volts rather than ints
   -B                bare; no timing information is given
   
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

#include "usbfastadc_io.h"

/* get a reasonably large buffer */
#define SIZE_DMA (1<<24)
#define DEFAULT_COMMANDEDSAMPLES 2000
#define DEFAULT_INPUTMODE 0

/* polling time in microseconds */
#define POLLTIME 10000
#define MBPS 40
#define GRACEBUFFER 256000

/* conversion constants */
#define conversion_offset (0x8000)
#define CONVERSION_SPAN 1.0
#define maxADCvalue (0xffff)
#define MAX_VOLTAGE 0.5
#define MIN_VOLTAGE -0.5

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
    //usleep(10000);
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
  0x00, 0x2f, 0x02, /* ch 2: div by 48 ->20 MHz, LVDS3.5mA */
  0x00, 0x2f, 0x08, /* ch 1: div by 48 ->20 MHz ,CMOS true phase */
  0x00, 0x1f, 0x20, /* ch 0: */

  /* Output configuration channels 5, 4 */
  6, 0x01, 0xb3,
  0x00, 0x17, 0x08, /* ch 5: /24 ->40MHz, CMOS, true phase (IFCLK)*/
  0x00, 0x2f, 0x08, /* ch 4: /48 ->20MHz, CMOS, true phase (aux clk)*/

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

/* clock data to reconfigure clock registers for interleaved operation */
char clock_data_interleaved[] = {
  
  /* Output configuration channels 3..0 */
  12, 0x01, 0xa1,
  0x00, 0x1f, 0x20, /* ch 3: */
  0x00, 0x5f, 0x02, /* ch 2: div by 96 -> 10 MHz, LVDS3.5mA */
  0x00, 0x5f, 0x08, /* ch 1: div by 96 -> 10 MHz, CMOS true phase */
  0x00, 0x1f, 0x20, /* ch 0: */

  /* Output configuration channels 5, 4 */
  6, 0x01, 0xb3,
  0x00, 0x17, 0x08, /* ch 5: /24 -> 40MHz, CMOS true phase (IFCLK)*/
  0x00, 0x5f, 0x08, /* ch 4: /96 -> 10MHz, CMOS true phase (aux clk)*/
  
  /* set sync bit */
  1, 0x02, 0x32,
  1,
  
  /* update registers */
  1, 0x02, 0x34, 1,

  /* execute sync */
  1, 0x02, 0x32, 0, 1, 0x02, 0x34, 1,

  /* end of sequence */
  0
};


/* configure clock, eventually reconfigure dividers for alternate sig */

int clock_configure(int handle, int mode) {
  int retval;
  retval=SPI_configure(handle, clock_data, CLOCKCHIP_WRITE);
  if (retval) return retval; /* some error */
  if (mode==2) { /* we need to reconfigure dividers */
    retval=SPI_configure(handle, clock_data_interleaved, CLOCKCHIP_WRITE);
  }
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
int modeword[4]= {
  0,    /* channel A */
  0x40, /* channel B */
  0x100, /* both channels interleaved */
  0x80  /* A and B in 8 bit versions */
};


int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opterr, opt; /* for parsing options */
    int i, retval, v;
    int v1, v2;
    unsigned char *startad=NULL;
    uint16_t *intarray;
    uint16_t *testindex;
    int numsamples;
    int commandedsamples=DEFAULT_COMMANDEDSAMPLES;
    int inputmode=DEFAULT_INPUTMODE; /* different input modes.
					0: only A channel
					1: only B channel
					2: both A and B interleaved 16 bit
					3  both A and B interleaved 8 bit
				     */
    int term_on_overflow=1; /* by default, respect overflows */
    int quietoption=0;
    int prescaler=DEFAULT_PRESCALER; /* how many samples to skip per cycle */
    int wordspersample; /* 1 word or 2 words */
    int samplenum; /* size of DMA buffer in samples */
    int samples, visited_already; /* already read in samples */
    int goodpoints; /* points ready for output */
    float basetime; /* base time step between samples in microseconds */
    int totalmilliseconds;
    int totalacquisitiontime;
    int bytespermillisecond; /* for estimating data flow/timeout condition */
    int allowedbytelag, expectedbytes, timeoutflag;
    int baremode=0;
    int scalemode=0;
    int autotrigstatus=0; /* do indicate if an autotrig event was used */

    /* the following is for the trigger status */
#define TRIG_PREACQ 0           /* buffer is empty */
#define TRIG_WAITING_FOR_ARM 1  /* waiting for hysteresis criterium */
#define TRIG_ARMED 2            /* pre-trig ok, waiting for trig */ 
#define TRIG_TRIGGERED 3        /* acq active */
#define TRIG_DONE 4             /* we have everything */
    int trigstatus = TRIG_PREACQ;
    int trigmode = 0; /* default: start right away */
    int trigchan = 0;   /* channel */
    int trigpol = 0;
    float TriggerDelay = 0.0; 
    float TriggerLevel = 0.0;
    float TriggerHysteresis = 0.05;
    float conversion;
    uint16_t triglev1, triglev2; /* for direct comparison */
    int trigdel;   /* integer version of delay */
    int trigidx ;    /* contains index of trigger */
    uint16_t trigmask;    /* used to include 2x8bit modes */
    int autotrigdelay = -1;  /* keeps autotrig delay. neg means work */
    
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:n:m:Oqp:T:C:P:D:L:H:SB")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       case 'n': /* number of samples */
	 if (sscanf(optarg,"%d",&commandedsamples)!=1) return -emsg(12);
	 //printf("commanded samples: %d, limit: %d\n",commandedsamples, SIZE_DMA/2);
	 if ((commandedsamples<1) /*|| (commandedsamples >(SIZE_DMA/2))*/)
	   return -emsg(13); /* too many samples */
	 break;
       case 'm': /* input mode */
	 if (sscanf(optarg,"%d",&inputmode)!=1) return -emsg(14);
	 if ((inputmode<0) || (inputmode >3)) return -emsg(15);
	 break;
       case 'O': /* ignore overflow */
	 term_on_overflow=0;
	 break;
       case 'q': /* quiet option */
	 quietoption=1;
	 break;
       case 'p': /* prescaler setting */
	 if (sscanf(optarg,"%d",&prescaler)!=1) return -emsg(20);
	 if ((prescaler<0) || (prescaler >4095)) return -emsg(21);	 
	 break;
       case 'T': /* Trigger mode*/
	 sscanf(optarg, "%d", &trigmode);
	 if (trigmode<0 || trigmode>2) return -emsg(22);
	 break;
       case 'C': /* trig channel */
	 sscanf(optarg, "%d", &trigchan);
	 if (trigchan<0 || trigchan>1) return -emsg(23);
	 break;
       case 'P': /* trig polarity */
	 sscanf(optarg, "%d", &trigpol);
	 trigpol = (trigpol<0)?-1:1;
	 break;
       case 'D': /* Trigger delay */
	 sscanf(optarg, "%f", &TriggerDelay);
	 break;
       case 'L': /* Trigger level */
	 sscanf(optarg, "%f", &TriggerLevel);
	 break;
       case 'H': /* Trigger hysteresis */
	 sscanf(optarg, "%f", &TriggerHysteresis);
	 break;
       case 'S': /* scaled mode (output in sec/volt) */
	 scalemode=1;
	 break;
       case 'B': /* bare mode (only voltage is given, no time) */
	 baremode=1;
	 break;
       }
    }

    /* some basic timing parameters */
    wordspersample = inputmode==2?2:1;
    basetime=50e-3*wordspersample*(prescaler+1); /* in microseconds */

    totalmilliseconds = basetime*commandedsamples/1000.;
    bytespermillisecond = 1000.*wordspersample*2/basetime+0.5;
    allowedbytelag = GRACEBUFFER+3*POLLTIME*bytespermillisecond/1000;
    printf("# totalmillisec: %d, bytespermillisec: %d, allowedbytelag: %d\n",
	   totalmilliseconds, bytespermillisecond, allowedbytelag);
    
    samplenum = SIZE_DMA/sizeof(uint16_t); /* at the moment ok for modes 0,1 */

    conversion = CONVERSION_SPAN/(maxADCvalue+1);

    /* adjust trigger channel variable for meaningful choice */
    if ((trigchan+inputmode) == 1) trigchan=0;
    trigmask=0xffff; /* for 16 bit modes */
    if (inputmode==3) {
      trigmask = trigchan ? 0xff : 0xff00;
      trigchan=0;
    }

    /* Do discrete versions from Trigger data */
    /* delay from trig to start-of-acq in samplesteps, truncated to first entry */
    trigdel = (int)(TriggerDelay/basetime*1000000.);
    if (trigmode == 0) trigdel=0; /* for consistent buffer readout */

    if ((TriggerLevel > MAX_VOLTAGE) || (TriggerLevel < MIN_VOLTAGE))
      return -emsg(24);
    triglev1 = (int)(TriggerLevel/conversion + conversion_offset);
    triglev2 = triglev1 - (trigpol<0?-1:1) *
      (int)(TriggerHysteresis/conversion); 
    printf("# triglev1: %d, triglev2: %d\n",triglev1, triglev2);
    printf("# trigger mode: %d\n",trigmode);
    printf("# input mode: %d\n",inputmode);
    if ((triglev2<0) || (triglev2>maxADCvalue)) return -emsg(25);

    /* adjust trigger levels and conversion factor */
    if (inputmode==3) {
      if (trigmask & 0xff) { /* we have channel 1 */
	triglev1 = triglev1 >> 8; triglev2 = triglev2 >> 8;
      } else {
	triglev1 = triglev1 & 0xff00; triglev2 = triglev2 & 0xff00;
      }
    }

    /* some random autotrig stuff */
    if (autotrigdelay<0)
      autotrigdelay = commandedsamples * DEFAULT_AUTOTRIGFACTOR;
    
    /* open device */
    handle=open(devicefilename,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }

    /* send device in a clean state */
    retval=ioctl(handle, RESET_TRANSFER);
    if (retval) return -emsg(11);
    //usleep(10000);
    
    /* Basic CPLD configuration to turn on power and LED */
    retval=ioctl(handle, WRITE_CPLD_LONG,
		 0x0c | modeword[inputmode] | (prescaler<<16) );
    if (retval) return -emsg(4);
   
    /* Configuration of clock chip to provide 20 MHz to ADC and IFCLK */
    if (clock_configure(handle, inputmode)) return -emsg(3);      

    /* set overflow policy */
    if (ioctl(handle,SET_OVERFLOWFLAG,term_on_overflow)) return -emsg(19);      

    /* configure ADC with something reasonable */
    if (adc_configure(handle)) return -emsg(5);
   
    /* Buffer preparation, start mmap and collateral */
    startad=mmap(NULL,SIZE_DMA,PROT_READ|PROT_WRITE, MAP_SHARED,handle,0);
    if (startad==MAP_FAILED) {
      printf("erno of fail: %d\n",errno);
      return -emsg(6);
    }
    for (i=0; i<SIZE_DMA; i+=4096) retval=retval+startad[i];
    intarray = (uint16_t *) startad;   /* for reading out as integers */


    /* start acquisition */
    retval=ioctl(handle, Start_USB_machine);
    if (retval) return -emsg(7);

    /* try to get a number of entries from fx2 */
    retval=ioctl(handle, START_STREAM);
    if (retval) return -emsg(8);
    
    /* prepare trigger status */
    if (trigmode == 0) {
      trigidx = 0;
      trigstatus=TRIG_TRIGGERED; /* go into acquisition mode directly */
    } else {
      if (trigdel>0) {
	trigstatus=TRIG_WAITING_FOR_ARM; /* skip preacq */
      }
    }
    visited_already=0; /* no pretrig points */
    
    /* check running status */
    totalacquisitiontime=0; /* polling timer */
    do { /* polling until number has been reached */
      usleep(POLLTIME);
      v=ioctl(handle, Get_transferredbytes);
      if (v<0) return -emsg(16);
      totalacquisitiontime += POLLTIME;
      expectedbytes = totalacquisitiontime*bytespermillisecond/1000;
      /* do timeout check */
      timeoutflag = v+allowedbytelag < expectedbytes;
      
      //printf("polling: totaltime: %d, bytes: %d, expected: %d\n",
      //     totalacquisitiontime, v, expectedbytes);

      /* now we do the content processing */
      samples = v/sizeof(int); /* for now, we assume single16bit mode */
      switch (trigstatus) {
      case TRIG_PREACQ:          /*  check if sth happened */
	if (samples < -trigdel) break; /* pre-trigger acquisition */
	trigstatus = TRIG_WAITING_FOR_ARM;
	/* make sure that we have enough in buffer */
	if (trigdel < 0)  visited_already = -trigdel;

      case TRIG_WAITING_FOR_ARM: /* do a search for arm condition */
	if (trigpol<0) { /* we need to be above triglev2 */
	  for (i=visited_already; i<samples; i++)
	    if ((intarray[(wordspersample*i+trigchan) % samplenum] & trigmask)
		>= triglev2) break;
	} else {/* we need to be below triglev2 */
	  for (i=visited_already; i<samples; i++) 
	    if ((intarray[(wordspersample*i+trigchan) % samplenum] & trigmask)
		<= triglev2) break;
	}
	/* check if pretrig was found, and leave loop if not */
	if (i>=samples) break;
	trigstatus = TRIG_ARMED;
	visited_already = i;
	printf("# armed at: %d\n",i);
	
      case TRIG_ARMED:	         /* do a search for trigger condition */
	if (trigpol<0) { /* we need to be below triglev1 */
	  for (i=visited_already; i<samples; i++)
	    if ((intarray[(wordspersample*i+trigchan) % samplenum] & trigmask)
		<= triglev1) break;
	} else {/* we need to be above triglev1 */
	  for (i=visited_already; i<samples; i++) 
	    if ((intarray[(wordspersample*i+trigchan) % samplenum] & trigmask)
		 >= triglev1) break;
	}
	/* check if pretrig was found, and leave loop if not */
	if (i>=samples) break;
	trigidx = i; /* this is our trigger time */
	trigstatus = TRIG_TRIGGERED;
	visited_already = i;
	printf("# triggered at: %d, samples: %d\n",i, samples);
	
      case TRIG_TRIGGERED: /* check if we have enough samples */
	goodpoints = samples - trigidx - trigdel;
	if (goodpoints < 0) { /* we are still in pretrig */
	  goodpoints = 0; /* is this used as an error indication? */ 
	  break;
	}
	if (goodpoints < commandedsamples) break; /* no status change */
	trigstatus = TRIG_DONE;

      case TRIG_DONE:     /* nothing to do here - should never be reached? */
	break;
      }
      visited_already = samples;
      /* do autotrig mechanism */
      if (trigmode==2) {
	if ((trigstatus == TRIG_WAITING_FOR_ARM) ||
	    (trigstatus == TRIG_ARMED)) {
	  if ( samples > autotrigdelay) {
	    trigidx=autotrigdelay;
	    trigstatus = TRIG_TRIGGERED;
	    autotrigstatus=1;
	    goodpoints = samples - trigidx - trigdel;
	    if (goodpoints >= commandedsamples) trigstatus = TRIG_DONE;
	  }
	}
      }
    } while ( (!timeoutflag) & 
	      (trigstatus < TRIG_DONE )
	      );
    
    retval=ioctl(handle, STOP_STREAM);
    if (timeoutflag) {
      fprintf(stderr,
	      " number of bytes: %d, time: %d\n",
	      v,totalacquisitiontime);
      return -emsg(17);
    }

    retval=ioctl(handle, FLUSH_FIFO);
    usleep(10000);

    //printf("retval from flush: %d\n",retval);
    v=ioctl(handle, Get_transferredbytes);
    //if (retval) return -emsg(9);
    printf("# bytecount: %d\n",v);
    
    numsamples=v/sizeof(uint16_t)/wordspersample;
    printf("# total acquired samples: %d\n",numsamples);
   
    printf("# autotrig status: %d\n",autotrigstatus);

    printf("# skipped cycles: %d\n",prescaler);
    printf("# timestep per line: %e seconds\n",basetime/1000000.);
    //printf("# total time: %d millisec\n",totalmilliseconds);

    if (!quietoption) {
      /* output as integers */
      switch (inputmode) {
      case 0: case 1: /* each sample is a single 16 bit value */
	for (i=0; i<commandedsamples; i++) {
	  v=intarray[(i+trigidx+trigdel) % samplenum]-0x8000;
	  switch (baremode+2*scalemode) {
      	  case 0:                                              /*output stuff*/
	    printf("%d %d\n",i+trigdel,v); break;
	  case 1:
	    printf("%d\n",v); break;
	  case 2:
	    printf("%g %g\n",(i+trigdel)*basetime/1000000.,v*conversion);
	    break;
	  case 3:
	    printf("%g\n",v*conversion); break;
	  }
	}
	break;
      case 2: /* interleaved mode */
	for (i=0; i<commandedsamples; i++) {
	  v1=intarray[(2*(i+trigidx+trigdel)) % samplenum]-0x8000;
	  v2=intarray[(2*(i+trigidx+trigdel)+1) % samplenum]-0x8000;
	  switch(baremode+2*scalemode) {
	  case 0:
	    printf("%d %d %d\n",i+trigdel,v1, v2); break;
	  case 1:
	    printf("%d %d\n", v1, v2); break;
	  case 2:
	    printf("%g %g %g\n",
		   (i+trigdel)*basetime/1000000.,
		   v1*conversion, v2*conversion);
	    break;
	  case 3:
	    printf("%g %g\n",v1*conversion, v2*conversion); break;
	  }
	}
	break;
      case 3: /* 8 bit interleaved */
	conversion = conversion*256.;
	for (i=0; i<commandedsamples; i++) {	
	  v=intarray[(i+trigidx+trigdel) % samplenum];
	  v1=((v>>8)& 0xff) - 0x80;
	  v2=(v & 0xff) - 0x80;
	  switch(baremode+2*scalemode) {
	  case 0:
	    printf("%d %d %d\n",i,v1, v2); break;
	  case 1:
	    printf("%d %d\n",v1, v2); break;
	  case 2:
	    printf("%g %g %g\n",
		   (i+trigdel)*basetime/1000000.,
		   v1*conversion, v2*conversion);
	    break;
	  case 3:
	    printf("%g %g\n",v1*conversion, v2*conversion); break;
	  }
	}
	break;
      }
    }
    

    printf("# trigdel: %d\n",trigdel);

    /* stop engine */
    retval=ioctl(handle, Stop_USB_machine);
    if (retval) {
      //printf("return code: %d, erro: %d\n",retval, errno);
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

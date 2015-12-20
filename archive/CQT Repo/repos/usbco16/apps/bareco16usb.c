/* program to talk to & use the 16-fold coincidence unit - bare events

   first round - needs to be tested 3.8.2014chk
   major bugfix 6.9.2014chk
   temporary fix for 10ms bug at end of sequence

   Usage:
   
   bareco16 [-t time]
            [-w | -b | -B]
	    [-i | -x | -r]
	    [-C <coincidacvalue>] [-D <deadtimedacvalue>] [-N]
	    [-f filename]

   program to run the 16-fold coincidence counter, connected to a USB
   adapter, for a given amount of time and deliver the results in
   various ways to stdout. API is similar to the counter programs for
   the simple counter cards, so it can be used in the usuial scripts.
   
   Options:
   
   -t <time>  Looks for detector events during <time>, given in
              milliseconds. Default is 1000 milliseconds, maximum
	      currrently 10^6 msec. Be aware that the histogramming buffer
	      is made up by unsigned integers, which limits the maximum
	      number of events to approx. 4x10^9.
   -w         output 16 bit variables.
   -b         output only lower 8 bits. This is the default.
   -B         output only upper 8 bits.

   -i         output in decimal text form
   -x         output in hex text form (default)
   -r         output raw binary 


   -h         output short helptext and stop then.

   -C <nnn>   send value nnn to coincidence time DAC. nnn has to be
              in range 0..4095. default is 2048
   -D <nnn>   set value for deadtime DAC. value has to be in range 0..4095
              default is 512.

   -N         no DAC setup. the DAC values are not explicitely set.
              this option is supposed to save time since DAC has not be
	      upoaded each consecutive call. not default.

   -U <device> use the specified file node <device> as the default device.
              If not set, it uses the default /dev/iobards/usbco16_0
   -f <file>  defines name of target file. If not specified, stdout is used.	
    
   (based on co16usb.c)

   ToDo:
     -check missing events (about 1% missing??)
*/
#include <inttypes.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>
/* definitions for IOCTLs of the device driver */
#include "usbco16_io.h"


/* default values and such */
#define default_device "/dev/ioboards/usbco16_0"
#define DEFAULT_integtime 1000 /* integration time in milliseconds */
#define DEFAULT_OUTPUT_OPTION 8     /* lower 8 bit, hex text */
#define DEFAULT_coincidac_value 2048 /* corresponds to xxx for a bby40 varactor
					a 330 ohm resistor and a short cable */
#define DEFAULT_deaddac_value 512 /* coresponds to xx ns for  BBY40/1kohm */
#define DEFAULT_DACsetupmode 1 /* default is to set up DAC */

/* internal constants - tweeking disrecommended */
/* This is a safety margin of 419kevents per polling interval. At a rate
   of 2.8 Mevents/sec (hw limit?) this corresponds to a latency time of
   150 msec - should be ok for excessive swap parties....110307chk */
#define size_dma  (1<<21) /* kernel buffer size, should be multiple of 4k */
#define dmasize_in_words (size_dma / sizeof(uint16_t))
#define dmabuf_complainwatermark (dmasize_in_words * 4 / 5)
#define hard_timer_boundary 1000000 /* maximum integration time */
#define POLLING_INTERVAL 40 /* in milliseconds */
#define TIMING_GRATITUDE 500 /* before timeout, in milliseconds */
#define ONESHOT_DELAY_TWEEK 0 /* fine adjustment to integration time in ms */
#define INTEGTIME_LOOP 60000 /* max integration window size, must be <64k */


/* ----------------------------------------------------------------*/
/* error handling */
char *errormessage[] = {
  "No error.",
  "Integration time out of range.",
  "",
  "IO device busy.",
  "Error opening IO device.",
  "Error getting histogram buffer", /* 5 */
  "Error getting DMA buffer or mmap failed",
  "DMA Buffer overflow during histogramming.",
  "No hardware timer within software timeout.",
  "Problems determining DMA count transfer 8-(",
  "Cannot open target file", /* 10 */
  "Error mallocing correction array.",
  "", 
  "Error finding histogram index in output routine.",
  "",
  "Coincidence DAC value out of range (0..4095).", /* 15 */
  "Deadtime DAC value out of range (0..4095).", 
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

/* file handle for co16 device */
int fh;

/* DAC code; all bitbang stuff is now done in firmware */
void send_DAC_word(int dataword) {
  ioctl(fh, SendDac, dataword);
  return;
}
void initialize_DAC(void) {
   ioctl(fh, InitDac);
   return;
}
void set_DAC(int channel, int value){
    send_DAC_word(((channel & 7)<<12) + (value & 0xfff));
    return;
}

/* structures for timer interrupts */
struct itimerval newtimer = {{0,0},{0,POLLING_INTERVAL*1000}};
struct itimerval stoptime = {{0,0},{0,0}}; 

/* handler for itimer signal SIGALRM */
int alarmcount,maxalarms;
int hardwaretimerflag;
void timer_handler(int sig) {
    if (sig==SIGALRM) {
	setitimer(ITIMER_REAL, &newtimer,NULL); /* restart timer */
	alarmcount++;
    }
    /* ToDo: test for end-of-timer */
}



/* process data. Arguments are:
   sourcebuffer: DMA buffer start address,
   startword: index of first word in DMA buffer to process,
   numwords: total number of words read in DMA buffer,
   buffer: Some scratch buffer, same size as DMA buffer
   outoption: encodes output mode,
   handle: indicates output file.
   the code returns the number of processed elements, which may be not all
   elements that were entered, or a negative number in case of an error.
   Less than numwords may be processed if there is a DMA buffer rollover
*/
int prepare_output(void * sourcebuffer, int startword, int numwords, 
		   void * buffer, int outoption, FILE* handle) {
    uint16_t *events; /* pointer into in buffer */
    unsigned char * cbuffer = (unsigned char *)buffer; /* for access as byte buffer */
    uint16_t *wbuffer = (uint16_t *) buffer; /* for access as uint16_t */
    int startindex, endindex,i;
    int oi; 
    int nw2; /* holds number of really processed words */
    char format[10]="%d\n"; /* default is decimal format */
    uint16_t w; /* for storing events */
    
    events = (uint16_t *) sourcebuffer;
    
    nw2 = numwords-startword;
    if (nw2 <= 0) return 0; /* also accounts for errors */

    /* complain if buffer is too filled */
    if ( nw2 > dmabuf_complainwatermark ) {
	return -1;
    }
    
    startindex = startword % dmasize_in_words;
    /* the following points to the last word */
    endindex   = ((numwords-1) % dmasize_in_words);
    
    /* first, handle eventual buffer wrap-around */
    if (endindex < startindex) {
	nw2 = dmasize_in_words - startindex;
	endindex = dmasize_in_words-1;
    }


    /* now we can process without wrapping */

    if (outoption & 2) { /* we have a 16 bit data taking */
	oi=0; /* output index */
	for (i=startindex; i<=endindex; i++) {
	    w=events[i];
	    if (w) wbuffer[oi++]=w;
	}
	/* now we have oi entries */
	if (outoption & 8) { /* we have a binary output */
	    fwrite(wbuffer, sizeof(uint16_t), oi, handle);
	} else { /* we have formattedd output */
	    if ((outoption & 0xc)==4) { /* we have hex text output */
		strcpy(format,"%04x\n");
	    }
	    /* send out the stuff event by event */
	    for (i=0; i<oi; i++) {
		fprintf(handle, format, wbuffer[i]);
	    }
	}
    } else { /* we have 8 bit data taking */
	oi=0;
	if (outoption & 1) { /* we take the upper 8 bits */
	    for (i=startindex; i<=endindex; i++) {
		w=(events[i]>>8)&0xff;
		if (w) cbuffer[oi++] = w;
	    }
	} else {
	    for (i=startindex; i<=endindex; i++) {
		w=events[i]&0xff;
		if (w) cbuffer[oi++] = w;
	    }
	}
	/* now output stuff */
	if (outoption & 8) { /* we have a binary output */
	    fwrite(cbuffer, sizeof(char), oi, handle);
	} else { 
	    /* now choose output format */
	    if ((outoption & 0xc)==4) { /* we have hex text output */
		strcpy(format,"%02x\n");
	    }
	    /* send out the stuff event by event */
	    for (i=0; i<oi; i++) {
		fprintf(handle, format, cbuffer[i]);
	    }
	}
    }
    return nw2; 
}


int main(int argc, char * argv[]){
  int retval, value;
    /* stuff for dma buffer */
    unsigned char *startad=NULL;
    int overflowflag;
    int wordsread,oldwordsread,wordsprocessed;
    uint16_t *outbuffer; /* for target reformatting */
    int integrationtime = DEFAULT_integtime; /* in milliseconds */
    int integtime_last,integ_loopcount; /* for multiple integration windows */
    int opt; /* for parsing command line options */
    int outoption = DEFAULT_OUTPUT_OPTION; /* determines style of output;
					      bit 0:1 
					         0: lower 8 bit, 1: upper 8 bit
						 2/3: 16 bit
					      bit 2:3
						 0: decimal, 1: hex, 
						 2/3: binary option
					       */
						 
    int coincidac_value = DEFAULT_coincidac_value;
    int dacsetupmode = DEFAULT_DACsetupmode; /* 0: no setup, 1: setup */
    int deaddac_value = DEFAULT_deaddac_value;
    char devicename[200]=default_device; /* name of device node */
    char outfilename[200] = ""; /* holds eventually outfilename */
    FILE *outhandle;
    int i;


    /* --------parsing arguments ---------------------------------- */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "t:wbBixrhC:D:NU:f:")) != EOF) {
	switch (opt) {
	case 't':
	    sscanf(optarg,"%d",&integrationtime);
	    /* integration time ok? */
	    if (integrationtime > hard_timer_boundary ||
		integrationtime < 3) return -emsg(1);
	    break;
	case 'b': /* lower 8 bits only mode */
	    outoption = outoption & 0xc;
	    break;
	case 'B': /* upper 8 bit */
	    outoption = (outoption & 0xc)+1;
	    break;
	case 'w': /* 16 bit output */ 
	    outoption = (outoption & 0xc)+2;
	    break;
	case 'i': /* send integer */
	    outoption = outoption & 3;
	    break;
	case 'x': /* hex text */
	    outoption = (outoption & 3) + 4;
	    break;
	case 'r': /* output raw binary */
	    outoption = (outoption & 3) + 8;
	    break;
	case 'C': /* set coincidence DAC */
	    sscanf(optarg,"%d",&coincidac_value);
	    if ((coincidac_value<0 ) || (coincidac_value>4095)) 
		return -emsg(15);
	    break;
	case 'D': /* set deadtime DAC */
	    sscanf(optarg,"%d",&deaddac_value);
	    if ((deaddac_value<0 ) || (deaddac_value>4095)) 
		return -emsg(16);
	    break;
	case 'N':
	    dacsetupmode= 0; /* no DAC setup */
	    break;
	case 'U': /* specify new device file */
	    sscanf(optarg,"%200s",devicename);
	    devicename[199]=0; /* safety termination*/
	    break;
	case 'f': /* specify outfile name */
	    sscanf(optarg, "%200s", outfilename);
	    outfilename[199]=0; /* safety termination */
	    break;
	case 'h':
	default:
	    printf("usage: %s [-t time] [-b | -B | -w] [-i | -x | -r] [-h] [-f filename]\nRefer to extensive description in the beginning of the source code for details.\n",argv[0]);
	    return 0;
	    break;
	};
    };



    /* prepare integration time windows */
    integ_loopcount=integrationtime/INTEGTIME_LOOP;
    integtime_last=integrationtime-INTEGTIME_LOOP*integ_loopcount;
    if (integtime_last==0) {
	integtime_last=INTEGTIME_LOOP; 
	integ_loopcount--;
    }
  
    /* start stuff */
    maxalarms = ((integrationtime+TIMING_GRATITUDE) / POLLING_INTERVAL); 
    
    /* prepare output buffer for cleaning up*/
    if (!(outbuffer=(uint16_t *)calloc(size_dma, sizeof(char))))  
	return -emsg(5);
    
    /* try to open outfile if specified */
    outhandle=stdout;
    if (outfilename[0]) {
	outhandle = fopen(outfilename, "w");
	if (!outhandle) return -emsg(10);
    }

    /* open adapter device driver with coincidence unit attached to it */
    if ((fh=open(devicename,O_RDWR))==-1) return -emsg(4);
    
    /* try to reserve memory for DMA transfer */
    startad=mmap(NULL,size_dma,PROT_READ|PROT_WRITE, MAP_SHARED,fh,0);
    if (startad==MAP_FAILED) return -emsg(6);
    /* try to speed up the nopage game */
    for (i=0;i<size_dma;i+=0x400) startad[i]=0;
    
    /* install signal handler for polling timer clicks */
    signal(SIGALRM, &timer_handler);
    
    /* eventually load DAC values */
    if (dacsetupmode) {
	initialize_DAC();
	set_DAC(0,coincidac_value);
	set_DAC(1,deaddac_value);
    }

    /* prepare coincidence unit */
    ioctl(fh, Reset_Hardware); /* disallow events to be registered */
    ioctl(fh, Initialize_FIFO); /* reset FIFO in EZusb */
  
    /* arm transfer engines */
    //ioctl(fh, Autoflush, 5 ); /* allow autoflush after 50 msec */
    ioctl(fh, StartTransfer); /* GPIF engine in EZusb */
    ioctl(fh, Start_USB_machine); /* kernel driver engine */


    /* preparation of timer signals */
    setitimer(ITIMER_REAL, &newtimer, NULL);
    
    alarmcount=0;
    overflowflag=0;
    wordsprocessed=0;
    
    /* multiple integration time window loop */
    do {
        hardwaretimerflag=0;
	/* start a hardware timer and start sampling data */
	value = (integ_loopcount?INTEGTIME_LOOP:integtime_last
		 -ONESHOT_DELAY_TWEEK)/10; /* internal time is 10ms granular */
	retval=ioctl(fh, Timed_Inhibit, value);  /* start actual accquisition */
	//printf("sent as timer argument: %d, retval: %d\n",value, retval);
	
        /*--------------------------------------------------------
	  here, the waiting for data & histogramming should happen */
	
	do {
	    pause();
	    retval=ioctl(fh, TimeToGo);
	    value=ioctl(fh, RequestStatus,100); /* query IOA register of FX2 */
	    if ((retval==0) &&((value&2)==0)) hardwaretimerflag=1;
	    //printf("came back from pause1; retval from timetogo: %d\n",retval);

	    wordsread=ioctl(fh,Get_transferredbytes)/sizeof(uint16_t);
	    if (wordsread<0) {
	      //printf("overflowpoint 1; wordsread: %d\n",wordsread);
		overflowflag=1;break;
	    }
	  
	    retval=prepare_output(startad, wordsprocessed, wordsread,
				  outbuffer, outoption, outhandle);
	    if (retval<0) {
		overflowflag=2;
	    } else {
		wordsprocessed+=retval;
	    };
	    
	} while ((!hardwaretimerflag) && (alarmcount < maxalarms) &&
		 (!overflowflag));
    } while (integ_loopcount--); /* loop through integration time windows */

    /* do cleanup of FIFO content after shutdown */
    ioctl(fh, ManualFlush);
    ioctl(fh, Stop_nicely);

    if (!overflowflag){ 
      do {
	pause();
	retval=ioctl(fh, TimeToGo);
	if (retval==0) hardwaretimerflag=1;

	oldwordsread=wordsread;
	wordsread=ioctl(fh,Get_transferredbytes)/sizeof(uint16_t);
	if (wordsread<0) {
	  overflowflag=1;break;
	}
	retval=prepare_output(startad, wordsprocessed, wordsread,
			      outbuffer, outoption, outhandle);
	if (retval<0) {
	  overflowflag=1;
	} else {
	  wordsprocessed+=retval;
	};
      } while ((oldwordsread<wordsread) && (!overflowflag)
	       && (alarmcount < maxalarms));
    } 

    /* ----------- here, readin & processing should end */

    //ioctl(fh, Stop_nicely);
    ioctl(fh, Stop_USB_machine);

    /* switch off polling  timer */
    setitimer(ITIMER_REAL, &stoptime, NULL);

    /* de-register signal handler */
    signal(SIGALRM,SIG_DFL);


    /* debug: print out buffer: */

    fclose(outhandle);
    
    close(fh);

    /* ----------- check for errors during acquisition  */
    if (wordsprocessed<0) return -emsg(9); /* error determining DMA cnt */
    if (overflowflag) {
	if (overflowflag==1) printf("overflow during readbytes.\n");
	/* printf("overflow: %d\n",overflowflag); */
	return -emsg(7); /* DMA buffeer overflow */
    }
    if (alarmcount >=maxalarms) return -emsg(8); /* timeout */

    free(outbuffer);
    return 0;
}














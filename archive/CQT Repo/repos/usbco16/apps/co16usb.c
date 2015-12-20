/* in transition to work with the USB interface version. seems to work

ToDo:
- add -u option to allow for different USB devices - ok
- update mmap structure to suit new interface - ok??
- migrate other communication/setup codes - verify!!
- move from quad to denser coding schemes in the USB version. look how these
  things are done in the readevents code - ok

- update timer granularity to 10ms
- check GPIF operation


program to talk to & use the 16-fold coincidence unit.

   Usage:
   
   co16 [-t time] [-a <mask> ] [-c] [-n] [-v] 
       [-d <nnnn> | -b <bitcnt> | -p <order> | -f]
       [-C <coincidacvalue>] [-D <deadtimedacvalue>] [-N]

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

   -n         If this option is given, no newline is sent after the results.
              Seems to be helpful for newer scanning scripts.
	      
   -a <mask>  sets a mask for which detectors should be considered in
              generating the histogram. The mask argument acts as a bitmask
	      for and-ing registered events before histogramming. For example,
	      a <mask> argument of 0x3f only considers the six detectors 0...5,
	      and <mask>= 0x11 only consideres detectors 0 and 4. Defaults
	      to a value of 0xffff (all sixteen detectors are on).

   -c         Correction for multiple coincidences to lower events. If
              switched on, a coincidence event like e.g. between detetectors
	      0,1 (pattern 0x0003) also is added to the single events in
	      patterns 0x0002 and 0x0001, similarly to higher order
	      coincidences.  Switched off per default.

   -d <nnnn>  Returns only the single events in inputs specified in the
              string nnnn. Each character of <nnnn> may be one of the digits
	      from 0 to f, in an arbitrary sequence. Switching on of correction
	      with option -c is recommended but not performed automatically.
	      This is the default out option, with <nnnn>="0123456789abcdef".

   -f         Output option, specifies to return all histogram entries
              compatible with detectors enabled in the detector mask (which
	      can be set by the -a option). The output sequence is monotonic
              in the detector pattern index. The first output, which would
	      correspond to pattern 0x0 and therefore be 0 by definition,
	      contains the total number of registered events.

   -b <bitcnt>Output option, specifies to return all histogram entries
              compatible with the detectors enabled like in the -f option,
	      but restricts output only to histogram entries corresponding
	      to at most <bitcnt> detectors having fired. Again, the first
	      number output corresponds to the number of total recorded events.

   -p <order> Output option similar to the -b option, but sorted differently.
              After the first output of the total event count, all single
	      count rates compatible with the bitmask specified in option -a
	      are output (in monotonic order of pattern index), then all
	      histogram counts corresponding to pairs are output (in an
	      "obvious" sequence, like (0-1, 0-2, 0-3, 1-2, 1-3, 2-3) for
	      mask=0xf; then all triples are output, and so on, up to
	      coincidences among <order> detectors.

   -v         Auxiliary output option to not only give the histogram entries,
              but also the corresponding index, with index and entry separated
	      by commas and individual outputs separated with newlines.
	      Intended as a debugging tool to understand what particular
	      index order is given out by one of the output options.

   -V         like option v, but gives out channel number in binary format

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


   extremely alpha version     14.05.03 christian kurtsiefer
   dma transfer and general flow control are working 16.05.03 chk
   added a user interface & prelim testing              18.5.03 chk
   documented handshake opertion mode 3 of nudaq card   9.5.05 chk
   implemented tunable timing: -C, -D, -N option        9.5.05chk
   removed integration time limit by using multiple
   integration windows   15.7.05 all&chk
   fine-tuned event buffer for large count rates; works now up 
   to 2.8 Mevents/sec 11.03.07 chk
   temporarily fixed issue with 10ms timing request for USB device 8.9.2014chk


   ToDo:
   - better separation of application-spec / kernel stuff
   - bring kernel driver definitions into a nudaq driver header file
   - use sigaction to make signalling more robust
   - do output index generation  while DMA is running instead of idle

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
#define CR_OPTION_DEFAULT 1 /* append newline to output per default */
#define CORRECT_OPTION_DEFAULT 0     /* no pair correction on as default */
#define DEFAULT_OUTPUT_OPTION 0     /* single counts only */
#define DEFAULT_SEQUENCE  "0123456789abcdef" /* for output option 0 */
#define SEQ_MAXLEN 20                        /* also for option 0 */
#define DEFAULT_VERBOSE_OPTION 0 /* do not give indices on output as default */
#define DEFAULT_histomask 0xffff
#define DEFAULT_coincidac_value 2048 /* corresponds to xxx for a bby40 varactor
					a 330 ohm resistor and a short cable */
#define DEFAULT_deaddac_value 512 /* coresponds to xx ns for  BBY40/1kohm */
#define DEFAULT_DACsetupmode 1 /* default is to set up DAC */

/* internal constants - tweeking disrecommended */
#define HISTOGRAM_SIZE 0x10000
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
  "Illegal element in single mode output specifier.",
  "IO device busy.",
  "Error opening IO device.",
  "Error getting histogram buffer", /* 5 */
  "Error getting DMA buffer or mmap failed",
  "DMA Buffer overflow during histogramming.",
  "No hardware timer within software timeout.",
  "Problems determining DMA count transfer 8-(",
  "Histogram mask not restricted to 16 bit.", /* 10 */
  "Error mallocing correction array.",
  "Error determining output option.", 
  "Error finding histogram index in output routine.",
  "Requested output order not compatible with number of detectors.",
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

/* helper routines for creating the output patterns */
/* for counting set bits in the lower 16 bits of a number: */
int bitcount(int x) {
    int m=0;
    int i;
    for (i=0x8000;i;i>>=1) if (i & x) m++;
    return m;
}

/*  recursive procedure creating a list of entries
    with a given first free bit position u, the number of v bits
    to still distribute, and the up-to-now existing bit pattern. The list
    lives in the prindex array, and the current vacant index in this list
    is stored in pnum. Apologies to everybody who reads this... */
void recursive_index_routine(int u, int v, int w, int stopmask,
		       int* prindex, int * pnum) {
    int x;
    for (x=u;x<(stopmask>>(v-1));x<<=1) {
	if (v==1) {
	    prindex[(*pnum)++] = w|x;
	} else {
	    recursive_index_routine(x<<1, v-1, w|x, stopmask, prindex, pnum);
	}
    }	 
}

/* routine to do the histogramming - returns total number of processed words */
int do_histogram(void * sourcebuffer, unsigned int * histo,
		 int startword, int endword, int hmask) {
    uint16_t *events;
    int startindex, endindex,i; 
    int numberofwords;
    
    events = (uint16_t *)sourcebuffer;
    numberofwords = endword - startword;
    /* what if startword == endword? */
    if (numberofwords <= 0) return 0; /* also accounts for errors */
    /* complain if buffer is too filled */
    if ( numberofwords > dmabuf_complainwatermark ) {
	/* printf("sq:%d eq: %dnumberofquads: %d\n",
	   startquad, endquad, numberofquads); */
	return -1;
    }
    
    startindex = startword % dmasize_in_words;
    endindex   =   endword % dmasize_in_words;
    if (startindex < endindex) {
	for (i=startindex;i<endindex;i++) histo[events[i] & hmask]++;
    } else {
	for (i=startindex;i<dmasize_in_words;i++) 
	    histo[events[i] & hmask]++;
	for (i=0;i<endindex;i++) histo[events[i] & hmask]++; 
    };
    return numberofwords;
}

/* routine to convert an integer number into a binary string representation */
void convert_to_binary(int number,char *targetstring) {
    int i;
    for (i=0;i<16;i++) 
	targetstring[i]=(number & (0x8000 >> i))?'1':'0';
    targetstring[16]=0;
}

int main(int argc, char * argv[]){
  int retval, value;
    /* stuff for dma buffer */
    unsigned char *startad=NULL;
    int oflags;
    int overflowflag;
    int wordsread,oldwordsread,wordsprocessed;
    unsigned int *histogram, *histogram2; /* for target+corrected histogram */
    int histomask = DEFAULT_histomask;
    int i,j;
    int integrationtime = DEFAULT_integtime; /* in milliseconds */
    int integtime_last,integ_loopcount; /* for multiple integration windows */
    int opt; /* for parsing command line options */
    int cr_option = CR_OPTION_DEFAULT;  /* if true append newline to output */
    int correct_option=CORRECT_OPTION_DEFAULT;  
    int output_option = DEFAULT_OUTPUT_OPTION; /* determines style of output;
						  0: like in single counters,
						  1: flat subsection of the
						     pattern array,
						  2: subset of the pattern
						     array up to order bits
						  3: cleverly ordered subset
						     of the pattern array */
    char out_sequence[SEQ_MAXLEN+1] = DEFAULT_SEQUENCE; /* for option 0 */
    int effective_hist_size;
    int indexfield[HISTOGRAM_SIZE];   /* to keep correction efficient */
    int print_n;                      /* number of entries in the print idx */
    int printindex[HISTOGRAM_SIZE];   /* to arrange for printout index */
    int verbose_option = DEFAULT_VERBOSE_OPTION; /*give indices with results */
    int out_order = 0;/* number of coincidences to be considered on output */
    int coincidac_value = DEFAULT_coincidac_value;
    int dacsetupmode = DEFAULT_DACsetupmode; /* 0: no setup, 1: setup */
    int deaddac_value = DEFAULT_deaddac_value;
    char dummystring[20];  /* for output of channels */
    char devicename[200]=default_device; /* name of device node */

    /* --------parsing arguments ---------------------------------- */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "na:t:d:cfvVb:p:hC:D:NU:")) != EOF) {
	switch (opt) {
	    case 'n': /* clear newline flag */
		cr_option=0;
		break;
	    case 't':
		sscanf(optarg,"%d",&integrationtime);
		/* integration time ok? */
		if (integrationtime > hard_timer_boundary ||
		    integrationtime < 3) return -emsg(1);
		break;
	    case 'a': /* set histogram AND mask */
		sscanf(optarg,"%i", &histomask);
		if (histomask & ~0xffff) return -emsg(10);
		break;
	    case 'c':  /* do correction for higher coincidences */
		correct_option = 1;
		break;
	    case 'd': /* set single counter output mode */
		output_option = 0;
		sscanf(optarg,"%19s",out_sequence);
		for (i=0; i<SEQ_MAXLEN && out_sequence[i] !=0; i++) 
		    if (!index("0123456789abcdef",out_sequence[i]))
			return emsg(2);
		break;
	    case 'f': /* set to all-good-histo-out mode */
		output_option = 1;
		break;
	    case 'v': /* be verbose on indices with output */
		verbose_option = 1;
		break;
	    case 'V':
		verbose_option = 2;
		break;
	    case 'b': /* give output up to order bits */
		output_option = 2;
		sscanf(optarg,"%d",&out_order);
		break;
	    case 'p': /* give output up to order bits in clever order */
		output_option = 3;
		sscanf(optarg,"%d",&out_order);
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
	        sscanf(optarg,"%s",devicename);
		devicename[199]=0; /* safety termination*/
		break;
	    case 'h':
	    default:
		printf("usage: %s [-t time] [-a <mask> ] [-c] [-n] [-v] [-d <nnnn> | -b <bitcnt> | -p <order> | -f] [-h]\nRefer to extensive description in the beginning of the source code for details.\n",argv[0]);
		return 0;
		break;
	};
    };

/* check argument consistency */
    if ((out_order < 0 ) || (out_order >bitcount(histomask)))
	return -emsg(14);

    /* prepare integration time windows */
    integ_loopcount=integrationtime/INTEGTIME_LOOP;
    integtime_last=integrationtime-INTEGTIME_LOOP*integ_loopcount;
    if (integtime_last==0) {
	integtime_last=INTEGTIME_LOOP; 
	integ_loopcount--;
    }
  
    /* start stuff */
    maxalarms = ((integrationtime+TIMING_GRATITUDE) / POLLING_INTERVAL); 
    
    /* prepare histogram buffer */
    if (!(histogram=(unsigned int *)calloc(HISTOGRAM_SIZE,sizeof(int)))) 
	return -emsg(5);
    
    /* open adapter device driver with coincidence unit attached to it */
    if ((fh=open(devicename,O_RDWR))==-1) return -emsg(4);
    
    /* try to reserve memory for DMA transfer */
    startad=mmap(NULL,size_dma,PROT_READ|PROT_WRITE, MAP_SHARED,fh,0);
    if (startad==MAP_FAILED) return -emsg(6);
    /* try to speed up the nopage game */
    //for (i=0;i<size_dma;i+=0x400) startad[i]=0;
    
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
	    /* This is a ttemporary, dirty fix to check if the residual
	       time is over. We use a debug code to see if the IOA1 register
	       that commands the inhibit line is still high. The TimeToGo
	       return may be (a) flawed by a race condition in the firmware,
	       and(b) does not capture the residual 10msec periode. */
	    value = ioctl(fh, RequestStatus,100); /* get ioa register value */
	    //if (retval==0) {
	      //printf("retval from timetogo: %d, value: 0x%x\n",
	      //     retval,value);
	    //}
	    if ((retval==0) && ((value&2)==0)) hardwaretimerflag=1;
	    wordsread=ioctl(fh,Get_transferredbytes)/sizeof(uint16_t);
	    if (wordsread<0) {
	      //printf("overflowpoint 1; wordsread: %d\n",wordsread);
		overflowflag=1;break;
	    }
	    retval=do_histogram(startad, histogram,
				wordsprocessed, wordsread, histomask);
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
	//retval=ioctl(fh, TimeToGo);
	//if (retval==0) hardwaretimerflag=1;
	//printf("came back from pause; retval from timetogo: %d\n",retval);

	oldwordsread=wordsread;
	wordsread=ioctl(fh,Get_transferredbytes)/sizeof(uint16_t);
	if (wordsread<0) {
	  overflowflag=1;break;
	}
	retval=do_histogram(startad, histogram,
			    wordsprocessed, wordsread, histomask);
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

    
    close(fh);

    /* ----------- check for errors during acquisition  */
    if (wordsprocessed<0) return -emsg(9); /* error determining DMA cnt */
    if (overflowflag) {
	if (overflowflag==1) printf("overflow during readbytes.\n");
	/* printf("overflow: %d\n",overflowflag); */
	return -emsg(7); /* DMA buffeer overflow */
    }
    if (alarmcount >=maxalarms) return -emsg(8); /* timeout */

    /* ----------- histogram data are postprocessed     */

    /* make histogram entry 0 to processed quads */
    histogram[0]=wordsprocessed;

    /* create an index field to restrict further operations only on
       unmasked detector bits.  */
    j=1;indexfield[0]=0;
    for (i=1;i<HISTOGRAM_SIZE;i++) if (!(i & ~histomask)) indexfield[j++]=i;
    effective_hist_size=1<<bitcount(histomask);

    /* eventually corrects for multiple coincidences */
    if (correct_option) {
	if (!(histogram2=(unsigned int *)calloc(HISTOGRAM_SIZE,sizeof(int)))) 
	    return -emsg(11); /* should contain zeros */
	for (i=1;i<effective_hist_size;i++) {
	    for (j=1;j<effective_hist_size;j++) 
		if ((j & i)==i)
		    histogram2[indexfield[i]]+=histogram[indexfield[j]];
	};
	for (i=1;i<effective_hist_size;i++)
	    histogram[indexfield[i]]=histogram2[indexfield[i]];
	free(histogram2);
    };
    
    /* create printout index list */
    print_n=0;
    switch (output_option) {
	case 0: /* linear output mode, only give single counts */
	    for (i=0; i<SEQ_MAXLEN && out_sequence[i] !=0; i++) { 
		j=out_sequence[i]-'0'; /* determine index */
		if (j>=0 && j<10) {j=(1<<j); } else {j=(1<<(j+'0'-'a'+10));}
		if ((j<0 || j>=HISTOGRAM_SIZE)) return -emsg(13);
		printindex[print_n++]=j;
	    }
	    break;
	case 1: /* flat output mode, prints out all meaningful histogram
		   entries compatible with the specified bit mask */
	    printindex[print_n++]=0; /* take processed quads as entry 0 */

	    for (i=1; i<effective_hist_size; i++)
		printindex[print_n++]=indexfield[i];
	    break;
	case 2: /* flat output mode, prints out all meaningful entries up
		   to a specified order of bits */
	    printindex[print_n++]=0; /* take processed quads as entry 0 */
	    for (i=1;i<effective_hist_size;i++) {
		if (bitcount(i)<=out_order) 
		    printindex[print_n++]=indexfield[i];
	    }
	    break;
	case 3: /* "clever" output mode, prints out all meaningfil entries up
		   to a specified order of bits in a sequence singles first,
		   then pairs, triples, etc.*/
	    printindex[print_n++]=0; /* take processed quads as entry 0 */
	    for (i=1;i<=out_order;i++) /* index singles, pairs, triplets... */
		 /* initial call to a recursive index generation procedure  */
		recursive_index_routine(1,i,0,effective_hist_size,
				    printindex, &print_n);
	    /* rearrange index to refer to original histogram indices */
	    for (i=1;i<print_n;i++) printindex[i]=indexfield[printindex[i]];
	    break;
	default:
	    return -emsg(12);
    }

    /* finally print out histogram entries */
    if (verbose_option) {
	switch (verbose_option) {
	    case 1:
		for (i=0;i<print_n;i++) 
		    fprintf(stdout,"%d, %d\n",printindex[i],
			    histogram[printindex[i]]);
		break;
	    case 2:
		for (i=0;i<print_n;i++) {
		    convert_to_binary(printindex[i],dummystring);
		    fprintf(stdout,"%s, %d\n",dummystring,
			    histogram[printindex[i]]);
		}
		break;
	}
    } else {
	for (i=0;i<print_n;i++) fprintf(stdout," %d",histogram[printindex[i]]);
    }
    if (cr_option) fprintf(stdout,"\n");
    
    free(histogram);
    return 0;
}














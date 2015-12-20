/* program to read in raw event files from the timestamp card for processing
   into a g(2) function. This is an attempt to reconstruct the clean g2
   extractor. 12.2.08 chk

   usage:  g2digest [-i infile] [-o oufile]

   options/parameters:

   -i infile:    source of the raw data stream from the timestamp card.
                 If not specified, stdin is chosen

   -t binwidth:  width of a time bin in 1/8 nsec

   -m maxbins:   number of timing bins. defaults to 100

   -o outfile:   target for the count result. if not chosen, stdout is used.

   OUTPUT FORMAT:
   
   The output format differs slightly from the pevious version in the sense
   that some parameters are encoded in the first two lines, but these
   start with a # to be ignored e.g. in gnuplot.

   The rest of the output is a set of lines with space-separated entries
   bin_index paircounts g2, where g2 is the normalized value, assuming a
   constant average rate on the two selected detector events.

   To be done: Selection of various output formats with a -V option, and
   definition of the selcted patterns for the g2 evaluation via options.

*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FNAMELENGTH 200  /* length of file name buffers */
#define FNAMFORMAT "%200s"   /* for sscanf of filenames */
#define DEFAULT_TIMESPAN 8 /* choose default binwidth 8 units = 1 nsec */
#define DEFAULT_BINNUM 500 /* choose 100 timebins */
#define INBUFSIZE 4096 /* choose 32kbyte large input buffer */

#define RINGBFORDER 20 /* should allow for 1e6 events between 1, 2 */
#define RINGBFNUM (1<<RINGBFORDER)
#define RINGBFMASK (RINGBFNUM-1)

/* error handling */
char *errormessage[] = {
    "No error.",
    "error parsing input file name",
    "error parsing output file name",
    "error parsing time interval",
    "timespan is not positive",
    "cannot open input file", /* 5 */
    "error reading pattern",
    "error opening output file",
    "error parsing bin number",
    "bin number must be positive.",
    "cannot malloc histogram buffer.", /* 10 */
    
};
int emsg(int code) {
    fprintf(stderr,"%s\n",errormessage[code]);
    return code;
};

typedef struct rawevent {unsigned int cv; /* most significan word */
    unsigned int dv; /* least sig word */} re;


int main (int argc, char *argv[]) {
    int opt; /* command parsing */
    char infilename[FNAMELENGTH]="";
    char outfilename[FNAMELENGTH]="";
    long long int timespan=DEFAULT_TIMESPAN;
    FILE *inhandle;
    long long int cnt;  /* all counts */
    long long int cnt12, cnt1, cnt2; /* counts in both ends */
    unsigned long long t1, pattern;
    struct rawevent inbuf[INBUFSIZE]; /* input buffer */
    FILE *outhandle;
    int timebinnumber = DEFAULT_BINNUM; /* number of bins */
    int index, retval; /* variables to handle input buffer */
    int *histo; /* pointer to g2 target array */
    int *histo2; /* pointer to g2 target array */
    int i;
    int discard;
    long long int discardcnt;

    unsigned long long *ringbf12; /* t12 events */
    unsigned int ringindex12;	
    unsigned long long *ringbf; /* t1 events */
    unsigned int ringindex;
    unsigned long long *ringbf2; /* t2 events */
    unsigned int ringindex2;
    /* These need to be set in an external option....*/
    int pattern1 = 0x1;
    int pattern2 = 0x2;
    unsigned long long diff; /* time difference wit two bins */
    int j;
    float factor; /* normalization factor for g2 */

    /* parse arguments */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "i:o:t:m:")) != EOF) {
	switch (opt) {
	    case 'i': /* set input file name */
		if(1!=sscanf(optarg,FNAMFORMAT,infilename)) return -emsg(1);
		
		break;
	    case 'o': /* set output file name */
		if(1!=sscanf(optarg,FNAMFORMAT,outfilename)) return -emsg(2);
		break;
	    case 't': /* set time bin interval in 1/8 nsec */
		if (1!=sscanf(optarg,"%lli",&timespan)) return -emsg(3);
		if (timespan<=0) return -emsg(4);
		break;
	    case 'm': /* number of time bins */
		if (1!=sscanf(optarg,"%i",&timebinnumber)) return -emsg(8);
		if (timebinnumber<=0) return -emsg(9);
	}
    }
    /* try to open input file */
    if (infilename[0]) {
	inhandle=fopen(infilename,"r");
	if (!inhandle) return -emsg(5);
    } else {inhandle=stdin; };
    
    /* allocate memory for storing the hsitogram bins */
    histo=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo) return -emsg(10);

    histo2=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo2) return -emsg(10);

    /* allocate ring buffer */
     ringbf=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf) return -emsg(10);
     ringbf2=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf2) return -emsg(10);
     ringbf12=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf12) return -emsg(10);
    ringindex=0; /* initialize ring index */
    ringindex2=0; /* initialize ring index */
    ringindex12=0; /* initialize ring index */
    discardcnt=0; /* initialize ring index */

    /* ATTENTION: THE RINGBUFER SHOULD BE INITIALIZED!!! */

    /* open out file */
    if (outfilename[0]) {
	outhandle=fopen(outfilename,"w");
	if (!outhandle) return -emsg(7);
    } else {outhandle=stdout; };
 
   /* initial reading */
    cnt=0; cnt1=0; cnt2=0; t1=0; cnt12=0;
    while (0<(retval=fread(inbuf, sizeof(struct rawevent), INBUFSIZE, inhandle))) {
	for (index=0;index<retval;index++) {
	    /* extract timing information */
	    t1=((unsigned long long)inbuf[index].cv<<17) + ((unsigned long long )inbuf[index].dv >>15);
		/* extract pattern info */
	 //   printf("sizeof(unsigned long long)=%d\n",sizeof(unsigned long long));
	 //   printf("t1=%lld",t1);
	    pattern = inbuf[index].dv & 0xf; 
	    
	    /* here should some processing going on. t1 contains the time
	       of an event in multiples of 1/8 nsec, pattern the detector
	       pattern.  The loop stops as soon as there are no more
		   events...*/
	    cnt++; /* for the moment, just an event counter */

	    /* temporary stuff: write time to stderr every 1024 events */
	    /* if ((cnt & 0x3ff) ==0) {
	       fprintf(stderr,"%lld\n",t1);
	       }
	    */
/*
	    if ((pattern==pattern1) && (pattern==pattern2))
	{
                cnt12++;
                ringindex12++;
                ringbf12[ringindex12 & RINGBFMASK]=t1;


		cnt2++;
		ringindex2++;
		ringbf2[ringindex2 & RINGBFMASK]=t1;
	}
*/
	    if (pattern==pattern1) { /* store in ring */
		cnt1++;
		ringindex++;
		ringbf[ringindex & RINGBFMASK]=t1;
	    }


	    if (pattern==pattern2) { /* store in ring */

	     	cnt2++;
                ringindex2++;
                ringbf2[ringindex2 & RINGBFMASK]=t1;
		//}
            	j=1;
		do {
		    /* time diff in histo index */
		    diff=(t1-ringbf2[(ringindex2-j) & RINGBFMASK])/timespan;
		    if (diff<timebinnumber) { /* count g1 event */
			histo2[diff]++;
		   } else {break;}
		    j++; /* incrementally go back in history */    
		} while (j<RINGBFNUM);  /* don't get buffer overflow */

            	j=0;
		do {
		    /* time diff in histo index */
		   diff=(t1-ringbf[(ringindex-j) & RINGBFMASK])/timespan;
		    if (diff<timebinnumber) { /* count g2 event */
			histo[diff]++;
		    } else {break; }
		    j++; /* incrementally go back in history */    
		} while (j<RINGBFNUM);  /* don't get buffer overflow */
	    
	}


    }

    factor=1.0/((float)cnt1 * ((float)cnt2-(float)discardcnt) * (float) timespan );
    fseek(outhandle, 0, SEEK_SET);
    fprintf(outhandle,"# cnt1: %lld cnt2: %lld, cnts: %lld, cnt12: %lld \n",cnt1,cnt2,cnt,cnt12);
    fprintf(outhandle,"# maxtime: %lld, timeinterval: %lld\n",t1,timespan);
    for (i=0;i<timebinnumber;i++) {
      fprintf(outhandle,"%.3f %d %f %d\n",(float)i*timespan*0.125,histo[i],histo2[i]);
}

    }
    fclose(inhandle);

    /* print result */


    free(histo); /* clean up buffer */
    free(ringbf);
    free(ringbf2);

   fprintf(stderr,"Counts1: %lld Counts2: %lld Discarded: %lld\n",cnt1,cnt2,discardcnt);

    fclose(outhandle);
    return 0;
}

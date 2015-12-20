/* standard g2 program, producing histograms with and without the timestamp bin length corrections.

   usage:  ./[thisfile] [-i infile] [-o outfile] [-h outfile2] [-p patt1] [-P patt2]

   options/parameters:

   -i infile:    source of the raw data stream from the timestamp card.
                 If not specified, stdin is chosen

   -t binwidth:  width of a time bin in 1/8 nsec

   -m maxbins:   number of timing bins. defaults to 2500

   -o outfile:   output file for g2 histogram between the two channels. if not chosen, stdout is used.

   -h outfile2:  outputs corrected and uncorrected histogram of the last 4 bits of the timing word from each entry.. 

   -p -P:        timestamp patterns between which to do the g2. 1 for chan0, 2 for chan1, 4 for chan2, etc.

************
INSTRUCTIONS
************
Supply the "true" bin lengths in the !!integer!! array ts_bin_lengths. Make sure the integers add up to the full 2000ps for our timestamp (or some other time interval for other devices?). You take care of the rounding errors. The rest should take care of themselves.

******************
INITIAL MOTIVATION
******************
To get the nominal 125ps resolution, the timestamp card takes in a 10MHz reference clock, multiplies it to a 500MHz clock signal, then 'subdivides' the 2ns period into 16 bins (4 bits). Ideally, each of these 16 bins are of equal length [125ps each], but in practice it's not quite exact. This will vary between devices, but on the same device it should be the same across all the channels.

This can show up in our results, eg in a g2 curve, small ripples/oscillations can occur where you might actually expect a straight line or a nice curve. This became an issue because we want to look at the g2 histograms from the timereversal expt in close detail.

To characterize the timestamp, have it measure a random source (eg APD measuring ambient light). The g2 should be totally flat if we look at the distribution of the last 4 bits of each timestamp entry. Any structure/fluctuations (above poisonnian error) we measure will be due to this unequal binning. From this, we can infer the "true" length of each of these 16 bins.
   
By using these "true" bin lengths [to be supplied in the code below], we can now correct for this. 

*********************
CORRECTION ALGORITHM
*********************
In an ideal case, the time interval of the bins are: 0-125ps for bin 0, 125-250ps for bin 1, 250-375ps for bin 2, etc. In reality we might measure 0-100ps for bin 0, 100-320ps for bin 2, nothing in bin 3, 320-500ps in bin 4, etc. By calculating the overlap of the time intervals of bin i (measured) and bin j (ideal), we determine the fraction of counts in bin i that needs to be reassigned into bin j. Each count in bin i then assigned to bin j with a probability equal to that fraction using a (pseudo-)random number generator. Not sure if generating a random number for each timestamp entry is too computationally heavy...

To test this correction, we use the standard g2 program to produce histograms, with and without the timestamp corrections. By comparing the two, we can see if the correction 'works'.

Victor L, Oct 2015
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

#define FNAMELENGTH 200  /* length of file name buffers */
#define FNAMFORMAT "%200s"   /* for sscanf of filenames */
#define DEFAULT_TIMESPAN 8 /* choose default binwidth 8 units = 1 nsec */
#define DEFAULT_BINNUM 2500 /* choose 100 timebins */
#define INBUFSIZE 4096 /* choose 32kbyte large input buffer */
#define DEFAULT_PATT1 1
#define DEFAULT_PATT2 2

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
    "timestamp correction bin lengths not consistent",
    
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
    char outfilename2[FNAMELENGTH]="";
    long long int timespan=DEFAULT_TIMESPAN;
    FILE *inhandle;
    long long int cnt;  /* all counts */
    long long int cnt12, cnt1, cnt2; /* counts in both ends */
    unsigned long long t1, t1_c, pattern;
    struct rawevent inbuf[INBUFSIZE]; /* input buffer */
    FILE *outhandle, *outhandle2;
    int timebinnumber = DEFAULT_BINNUM; /* number of bins */
    int index, retval; /* variables to handle input buffer */
    int *histo,*histo_c; /* pointer to g2 target array */
    int *histo2,*histo2_c; /* pointer to g2 target array */
    int i,j;
    long long int discardcnt;

    unsigned long long *ringbf, *ringbf_c; /* t1 events */
    unsigned int ringindex;
    unsigned long long *ringbf2, *ringbf2_c; /* t2 events */
    unsigned int ringindex2;
    /* These need to be set in an external option....*/
    int pattern1 = DEFAULT_PATT1;
    int pattern2 = DEFAULT_PATT2;
    unsigned long long diff; /* time difference wit two bins */

    /* parse arguments */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "i:o:t:m:h:p:P:")) != EOF) {
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
        case 'h': /* set output file name */
        if(1!=sscanf(optarg,FNAMFORMAT,outfilename2)) return -emsg(2);
        break;
        case 'p': //set pattern 1
        if(1!=sscanf(optarg,"%i",&pattern1)) return -emsg(6);
        break;
        case 'P': //set pattern 2
        if(1!=sscanf(optarg,"%i",&pattern2)) return -emsg(6);
        break;
	}
    }
    /* try to open input file */
    if (infilename[0]) {
	inhandle=fopen(infilename,"r");
	if (!inhandle) return -emsg(5);
    } else {inhandle=stdin; };
    /* open out file */
    if (outfilename[0]) {
    outhandle=fopen(outfilename,"w");
    if (!outhandle) return -emsg(7);
    } else {outhandle=stdout; };
    if (outfilename2[0]) {
    outhandle2=fopen(outfilename2,"w");
    if (!outhandle2) return -emsg(7);
    } else {outhandle2=stdout; };

    /* allocate memory for storing the hsitogram bins */
    histo=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo) return -emsg(10);
    histo2=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo2) return -emsg(10);
    histo_c=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo) return -emsg(10);
    histo2_c=(int*)calloc(timebinnumber,sizeof(int)); /* alocate buffer */
    if (!histo2) return -emsg(10);

    /* allocate ring buffer */
     ringbf=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf) return -emsg(10);
     ringbf2=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf2) return -emsg(10);
    ringbf_c=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf_c) return -emsg(10);
     ringbf2_c=(unsigned long long *)calloc(RINGBFNUM, sizeof(unsigned long long)); /* allocate ring buffer */
    if (!ringbf2_c) return -emsg(10);
    ringindex=0; /* initialize ring index */
    ringindex2=0; /* initialize ring index */
    discardcnt=0; /* initialize ring index */

    /* ATTENTION: THE RINGBUFER SHOULD BE INITIALIZED!!! */


    /**************************************
    TIMESTAMP BIN CORRECTION INITIALIZATION
    **************************************/
    //!!Supply timestamp bin lengths here!!
    #define TS_BIN_NUM 16  //no. of timestamp 'bins' 
    //!!These times are for QOT-0021V1-3!!
    //int ts_bin_lengths[TS_BIN_NUM]={133,97,180,157,174,120,80,95,148,155,0,307,180,163,11,0};
    //!!These times are for QOT-0021V1-11!!
    int ts_bin_lengths[TS_BIN_NUM]={68,113,163,163,197,142,85,113,155,157,0,278,128,158,80,0};
    int ideal_bin_length=125; //assuming picoseconds here
    int ts_bin_starttimes[TS_BIN_NUM];
    double ts_bin_cum_table[TS_BIN_NUM][TS_BIN_NUM];
    double overlap_fraction,cumu_prob;
    int overlap_start,overlap_end;
    unsigned int last4bits, new_last4bits=0;
    double rand_num;
    long long int *last4bitshisto, *corr_last4bitshisto;
    last4bitshisto=(long long int*)calloc(16,sizeof(long long int));
    corr_last4bitshisto=(long long int*)calloc(16,sizeof(long long int));
    if (!last4bitshisto || !corr_last4bitshisto) return -emsg(10);


    //Calculate the start time of each bin (with respect to the start of the first bin)
    ts_bin_starttimes[0]=0;
    for(i=1;i<TS_BIN_NUM;i++){
        ts_bin_starttimes[i] = ts_bin_starttimes[i-1] + ts_bin_lengths[i-1];
    }
        //Sanity check. 
        if( ts_bin_starttimes[TS_BIN_NUM-1]+ts_bin_lengths[TS_BIN_NUM-1] != ideal_bin_length*TS_BIN_NUM ){
            return emsg(11); //bin lengths don't add up!
        }

    //Table of cumulative probabilities
    //Element [i][j] is the probability that an entry in bin [i] should go into bins [j<=i]
    for(i=0;i<TS_BIN_NUM;i++){
        cumu_prob=0;
        for(j=0;j<TS_BIN_NUM;j++){
            overlap_start = ts_bin_starttimes[i] > j*ideal_bin_length ? ts_bin_starttimes[i] : j*ideal_bin_length;
            overlap_end = ts_bin_starttimes[i] + ts_bin_lengths[i] < (j+1)*ideal_bin_length ? ts_bin_starttimes[i] + ts_bin_lengths[i] : (j+1)*ideal_bin_length;
            if(overlap_end<=overlap_start) overlap_fraction=0;
            else overlap_fraction=(double)(overlap_end-overlap_start)/ts_bin_lengths[i];
            cumu_prob += overlap_fraction;
            ts_bin_cum_table[i][j]= cumu_prob;    
        }
    }

            //For debugging of the timestamp bin correction thing...
            /*printf("timestamp bin lengths:\n");
            for(i=0;i<TS_BIN_NUM;i++)printf("%d ",ts_bin_lengths[i]);
            printf("\ntimestamp bin starttimes:\n");
            for(i=0;i<TS_BIN_NUM;i++)printf("%d ",ts_bin_starttimes[i]);
            printf("\nideal timestamp bin starttimes:\n");
            for(i=0;i<TS_BIN_NUM;i++)printf("%d ",i*ideal_bin_length);
            printf("\ntable of cumulative probabilities:\n");
            for(i=0;i<TS_BIN_NUM;i++){
                for(j=0;j<TS_BIN_NUM;j++)printf("%.3f ",ts_bin_cum_table[i][j]);
                printf("\n");
            }*/

    //Initialize random number generator-> seed with current time
    srand((long)time(NULL));

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

        // Timestamp bin correction
        // !!NOTE!! If implementing a rollover correction (e.g. for files >19h in length, it should be done AFTER the bin correction!)
        rand_num=rand()/(double)RAND_MAX; //between 0 and 1
        last4bits=t1 & 0xf;
        new_last4bits=-1;
        for(j=0;j<TS_BIN_NUM;j++){
            if(rand_num<=ts_bin_cum_table[last4bits][j]){
                new_last4bits=j;
                break;
            }
        }
        if(new_last4bits==-1){   //did the correction procedure fail to assign a new bin?
            fprintf(stderr, "Timestamp bin correction failed: t1=%lld\n",t1);
            new_last4bits=last4bits;  //assign something: just use original value...
        }
        t1_c= (t1 & 0x1fffffffffff0LL) + (new_last4bits & 0xf); //timing word = 49 bits
        last4bitshisto[last4bits]++;corr_last4bitshisto[new_last4bits]++;

	    
	    /* here should some processing going on. t1 contains the time
	       of an event in multiples of 1/8 nsec, pattern the detector
	       pattern.  The loop stops as soon as there are no more
		   events...*/
	    cnt++; /* for the moment, just an event counter */

	    if (pattern==pattern1) { /* store in ring */
		cnt1++;
		ringindex++;
		ringbf[ringindex & RINGBFMASK]=t1;
        ringbf_c[ringindex & RINGBFMASK]=t1_c;
	    }


	    if (pattern==pattern2) { /* store in ring */

	     	cnt2++;
                ringindex2++;
                ringbf2[ringindex2 & RINGBFMASK]=t1;
                ringbf2_c[ringindex2 & RINGBFMASK]=t1_c;
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

            j=1;
        do {
            /* time diff in histo index */
            diff=(t1_c-ringbf2_c[(ringindex2-j) & RINGBFMASK])/timespan;
            if (diff<timebinnumber) { /* count g1 event */
            histo2_c[diff]++;
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

                j=0;
        do {
            /* time diff in histo index */
           diff=(t1_c-ringbf_c[(ringindex-j) & RINGBFMASK])/timespan;
            if (diff<timebinnumber) { /* count g2 event */
            histo_c[diff]++;
            } else {break; }
            j++; /* incrementally go back in history */    
        } while (j<RINGBFNUM);  /* don't get buffer overflow */
	    
	}


    }


    }
    fclose(inhandle);

    /* print result */
    fseek(outhandle, 0, SEEK_SET);
    fprintf(outhandle,"# cnt1: %lld cnt2: %lld, cnts: %lld, cnt12: %lld \n",cnt1,cnt2,cnt,cnt12);
    fprintf(outhandle,"# maxtime: %lld, timeinterval: %lld\n",t1,timespan);
    fprintf(outhandle,"# time, g2_counts, g1_counts, corrected_g2_counts, corrected_g1_counts\n");
    for (i=0;i<timebinnumber;i++) {
      fprintf(outhandle,"%.3f %d %d %d %d\n",(float)i*timespan*0.125,histo[i],histo2[i],histo_c[i],histo2_c[i]);
}

    free(histo); /* clean up buffer */
    free(ringbf);
    free(ringbf2);

   fprintf(stderr,"#Counts1: %lld Counts2: %lld Total: %lld Discarded: %lld\n",cnt1,cnt2,cnt,discardcnt);
  fprintf(outhandle2,"#Histogram of last 4 bits of timing info of each timestamp entry.\n");
  fprintf(outhandle2,"#Total counts: %lld \n", cnt);
  fprintf(outhandle2,"#bin no, counts, fraction, corrected counts, corrected fraction\n");
  for(i=0;i<16;i++){
    fprintf(outhandle2, "%d %lld %.5g %lld %.5g\n", i, last4bitshisto[i], (double)last4bitshisto[i]/cnt, corr_last4bitshisto[i], (double)corr_last4bitshisto[i]/cnt);
  }
    fclose(outhandle);
    fclose(outhandle2);
    return 0;
}

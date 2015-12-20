/* program to read in raw event files from the timestamp card for processing
   into a g(2) function, it normalizes the g2 for each small data chunk processed. 
   This might get rid of normalization error due to signal strength drifts.

   usage:  g2smarter [-i infile] [-o oufile] [-m maxbin] [-t binsize] [-c channels] [-s offset] [-n noiseoffset] 

   options/parameters:

   -i infile:    source of the raw data stream from the timestamp card.
                 If not specified, stdin is chosen

   -t binwidth:  width of a time bin in 1/8 nsec

   -m numbins:   number of timing bins. defaults to 4000

   -o outfile:   target for the count result. if not chosen, stdout is used.

   -c channel: 	 input channels of the g2 function (eg. 01,02,03,12,13,23)

   -s offset:    input the count rate of 1st and 2nd channel above which g2 function is calculated

   -n offset:    input the count rate of 1st and 2nd channel below which a bin is considered to contain only noise 
   
   -g pattern: select events with give phase pattern
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FNAMELENGTH 200  /* length of file name buffers */
#define FNAMFORMAT "%200s"   /* for sscanf of filenames */
#define DEFAULT_TIMESPAN 1 /* choose default binwidth 8 units = 1 nsec */
#define DEFAULT_BINNUM 4000 /* choose 4000 timebins */
#define INBUFSIZE 4096 /* choose 32kbyte large input buffer */
#define DEFAULTCHANNEL1 1
#define DEFAULTCHANNEL2 2
#define COUNTINGTIMESPAN 40000000 /* the count monitor duration in 125psec */
#define DEFAULT_EXTRAPHASE 0
#define RECORDLIMIT 370000000000000 /* data in a timestamp file longer than 6 hours are corrupted*/ 

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
    "error parsing input channels ",
    "g2 channel input must be either 01,02,03,12,13,23 ",
    "error parsing offset",
    "offset must not be negative.",
    "error converting extra phase or phase out of 0..0x1ff",
    "extra phase out of limits",
};
int emsg(int code) {
    fprintf(stderr,"%s\n",errormessage[code]);
    return code;
};

typedef struct rawevent {unsigned int cv; /* most significan word */
    unsigned int dv; /* least sig word */} re;

/* pattern list of allowed phase patterns (other are very rare...)
   In this list, the pattern 375 with the 2ns issue is excluded and can be corrected 
   later on...
*/

int pli[] = {6, 7, 12, 14, 39, 136, 140, 142,
             152, 156, 216, 295, 359, 371, 472,
             497, 499, 504, 505, 507, -1};

/* mask for identifying the 13 most significant bits in a 49 bit timing word */
#define UPPERMASK 0x1fff000000000LL

int main (int argc, char *argv[]) {
    int opt; /* command parsing */
    char infilename[FNAMELENGTH]="";
    char outfilename[FNAMELENGTH]="";
    long long int timespan=DEFAULT_TIMESPAN;
    unsigned long long bincnt=0; /*record the no. of counts within countingtimespan*/
    unsigned long long t1, pattern;
    struct rawevent inbuf[INBUFSIZE]; /* input buffer */
    FILE *inhandle;
    FILE *outhandle;
    int timebinnumber = DEFAULT_BINNUM; /* number of bins */
    int index=0, retval; /* variables to handle input buffer, initialize index to avoid segmentation fault */
    int *histo; /* pointer to g2 target array */
    int *temphisto; /* pointer to temporary g2 target array (if the count rate is smaller than offset, this data is removed*/
    double *histoN; /*pointer to g2 array which add up all normalized g2 from each processed data chunk*/
    double N; /*Normalization constant*/
    int i,ip;
    int extraphase = DEFAULT_EXTRAPHASE; /* phase pattern to sort */
    int ppat, oldppat; /* for storing phase pattern */
    float center;
    int patcheck=0, thrownaway1=0, thrownaway2=0; /* a parameter used to check the if an event is thrown away by because of bad pattern */
    unsigned long long rollovercorrection=0;
    unsigned long long totalnoise1,totalnoise2;
    unsigned long long totalsignal1,totalsignal2;
    unsigned long long bincnt1, bincnt2;
    unsigned long long signalbins, noisebins;
    unsigned long long offset=0; /*count rate above which g2 is considered*/
    unsigned long long noiseoffset=0; /*count rate below which a bin is considered to contain only noise*/
    unsigned long long countingtimespan=COUNTINGTIMESPAN;
    unsigned long long oldbintime=0; /*record the starting time of current 10ms bin*/
    unsigned long long timezero=0; /*record the time of the first event*/
    unsigned long long oldpattern, oldt1, delay, maxdelay,realoldpattern;
    unsigned long long channel1 = DEFAULTCHANNEL1;
    unsigned long long channel2 = DEFAULTCHANNEL2;
    unsigned long long channelopt = 01;

    double offsetd=0; 
    double noiseoffsetd=0;
    double countingtimespand=0;
    double signalbinsd=0, noisebinsd=0; /* create double copies to avoid silly integer/integer problems */
    double bgg2=0, bgg2N=0; /*background contribution to the g2*/

    /* parse arguments */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "i:o:t:m:c:s:n:g:")) != EOF) {
	switch (opt) {
	    case 'i': /* set input file name */
		if(1!=sscanf(optarg,FNAMFORMAT,infilename)) return -emsg(1);
		break;
	    case 'o': /* set output file name */
		if(1!=sscanf(optarg,FNAMFORMAT, outfilename)) return -emsg(2);
		break;
	    case 't': /* set time bin interval in 1/8 nsec */
		if (1!=sscanf(optarg,"%lli",&timespan)) return -emsg(3);
		if (timespan<=0) return -emsg(4);
		break;
	    case 'm': /* number of time bins */
		if (1!=sscanf(optarg,"%i",&timebinnumber)) return -emsg(8);
		if (timebinnumber<=0) return -emsg(9);
                break;
	    case 'c': /* input channel 1 */
		if (1!=sscanf(optarg,"%lli",&channelopt)) return -emsg(11);
		if (channelopt==1||channelopt==12||channelopt==23||channelopt==2||channelopt==3||channelopt==13) 
                {channel1=1<<(channelopt/10);channel2=1<<(channelopt-10*(channelopt/10));}
                /*convert channel num to data pattern*/
                else
                { return -emsg(12);}
                break;
	    case 's': /* offset value of 1st channel and 2nd channel above which g2 is calculated */
		if (1!=sscanf(optarg,"%lli",&offset)) return -emsg(13);
		if (offset<0) return -emsg(14);
                break;
	    case 'n': /* offset value of 1st channel and 2nd channel below which the bin is considered to contain only noise */

		if (1!=sscanf(optarg,"%lli",&noiseoffset)) return -emsg(13);
		if (noiseoffset<0) return -emsg(14);
                break;
            case 'g': /* selected phase pattern */
                if (1!=sscanf(optarg,"%i",&extraphase)) return -emsg(15);
                if (extraphase & ~0x1ff) return -emsg(16);
                break;
	}
    }
    /* try to open input file */
    if (infilename[0]) {
	inhandle=fopen(infilename,"r");
	if (!inhandle) return -emsg(5);
    } else {inhandle=stdin; };
    
    /* allocate memory for storing the hsitogram bins */
    histo=(int*)calloc(timebinnumber,sizeof(int)); /* allocate buffer */
    temphisto=(int*)calloc(timebinnumber,sizeof(int)); /* allocate buffer */
    histoN=(double*)calloc(timebinnumber,sizeof(double)); /* allocate buffer */
    if (!histo||!temphisto||!histoN) return -emsg(10);

    maxdelay = timespan*timebinnumber;
    offsetd = offset*0.000000000125*countingtimespan;
    noiseoffsetd = noiseoffset*0.000000000125*countingtimespan;
    countingtimespand= countingtimespan*0.000000000125;
    printf("File: %s\n", infilename);
    printf("   signal threshold = %.1lf/ %.1lf ms\n", offsetd, countingtimespand*1000);
    printf("   noise threshold = %.1lf/ %.1lf ms\n", noiseoffsetd, countingtimespand*1000);
    printf("   time bin = %lld x 125ps\n", timespan);
    printf("   mask of channel 1 = %lld , mask of channel 2 = %lld\n\n",channel1, channel2);

    /* initialize rollover */
    rollovercorrection=0;

    /* initialize index */
    index=0;

   /* initial reading */
    retval=fread(inbuf, sizeof(struct rawevent), 10, inhandle); /*remove first 10 events */
    retval=fread(inbuf, sizeof(struct rawevent), 1, inhandle); /*read the next event and define it to be zeroth event */

    /* extract timing infomation */
    t1=((unsigned long long)inbuf[index].cv<<17) +
	((unsigned long long )inbuf[index].dv >>15)+
	rollovercorrection;
	/* extract pattern info */
    pattern = inbuf[index].dv & 0xf; 
    ppat = (inbuf[index].dv & 0x1ff0 )>>4;

    oldpattern = pattern;
    realoldpattern = pattern;
    oldt1 = t1;
    oldbintime = t1;
    timezero = t1;
    signalbins=0;
    noisebins=0;
    bincnt1=0;
    bincnt2=0;
    totalnoise1=0;
    totalnoise2=0;
    totalsignal1=0;
    totalsignal2=0;
    delay=0;
    bincnt=1;

    for (i=0;i<timebinnumber;i++) 
    {
       histo[i]=0;
       histoN[i]=0;
    }
    while (0<(retval=fread(inbuf, sizeof(struct rawevent), INBUFSIZE, inhandle))) {
	for (index=0;index<retval;index++) 
        {
	    /* extract timing information */
	    t1=((unsigned long long)inbuf[index].cv<<17) +
		((unsigned long long )inbuf[index].dv >>15)+
		rollovercorrection;
		/* extract pattern info */
	    pattern = inbuf[index].dv & 0xf; 
	    ppat = (inbuf[index].dv & 0x1ff0 )>>4;

            if(t1<oldt1) {
		if (((t1 & UPPERMASK)==0) &&
		    ((oldt1 & UPPERMASK)==UPPERMASK)) { /* correct rollover */
		    rollovercorrection += (1LL<<49);
		    t1 += (1LL<<49); /* correct also current event */
		    printf("rollover!! new rollover: 0x%016llx\n",
			   rollovercorrection);
		} else {
		    printf("time reversal!! current event t1: 0x%016llx, previous event oldt1: 0x%016llx\n",
			   t1,oldt1);
		}
	    }

            /*if(patcheck==1)
	    {
	        if(realoldpattern==channel1){thrownaway1++;}
		else if(realoldpattern==channel2){thrownaway2++;}
	    }
	    patcheck=1;
            realoldpattern=pattern;

            for (ip=0;(pli[ip]>=0) && (pli[ip]!=ppat);ip++);
            if (pli[ip]<0) continue;   /*only take good patterns */

            patcheck=0;
            /* here should some processing going on. t1 contains the time
	       of an event in multiples of 1/8 nsec, pattern the detector
	       pattern.  The loop stops as soon as there are no more
		   events...*/

            if((t1-oldbintime)/countingtimespan>0)
            {
                oldbintime+=((t1-oldbintime)/countingtimespan)*countingtimespan;
                /*record temp histogram into final histogram if count rate above offset*/
                if ((double)bincnt1>=offsetd && (double)bincnt2>=offsetd)
                {
                    N=bincnt1*bincnt2*timespan/((double)countingtimespan);
                    for (i=0;i<timebinnumber;i++) 
                    {
                        histo[i]+=temphisto[i];
                        histoN[i]+=(temphisto[i]/N);
                    }
                    signalbins++;
                    totalsignal1+=bincnt1;
                    totalsignal2+=bincnt2;
                }
                else if((double)bincnt1<=noiseoffsetd && (double)bincnt2<=noiseoffsetd)
                {
                    noisebins++;
                    totalnoise1+=bincnt1; 
                    totalnoise2+=bincnt2; 
                }

                for (i=0;i<timebinnumber;i++) 
                {
                    temphisto[i]=0; /*clear previous bin histogram*/
                }
                bincnt=0; /*clear previous bin counts*/
                bincnt1=0; /*clear previous bin counts*/
                bincnt2=0; /*clear previous bin counts*/
            }

            if(oldpattern==channel1&&pattern==channel2)
            {
                delay = t1 - oldt1;
		if (oldt1>t1)
		{
                        printf ("Time Reversal occurs. Error!\n");
		}
		else if(delay<maxdelay)
		{ 
		    temphisto[delay/timespan]++;
                }
            }

            oldpattern=pattern;
            oldt1=t1; 
            oldppat=ppat;
            bincnt++;
 
            if(pattern==channel1||pattern==channel2)
            {
                if(pattern==channel1)
                {
                    bincnt1++;
                }
                else
                {
                    bincnt2++;
                }
            }
	}
    }
    fclose(inhandle);
  
    /* open out file */
    if (outfilename[0]) {
	outhandle=fopen(outfilename,"w");
	if (!outhandle) return -emsg(7);
    } else {outhandle=stdout; };
    
    /* print result */

    /* output histogram */
    for (i=0;i<timebinnumber;i++) {
        center = ((i*timespan)+timespan/2.0f)*0.125;
	fprintf(outhandle,"%d\t%f\t%d\t%.4lf\t%.2lf\n",i,center,histo[i],histoN[i]/signalbins,histoN[i]);
    }

    printf("total number of discarded events due to bad patterns: ch1 = %d, ch2 = %d\n",thrownaway1, thrownaway2);
    printf("total number of signal bins = %lld, noise bin = %lld\n",signalbins, noisebins);
    printf("total noise counts:\n channel 1 : %lld (%.2f /s)\n channel 2 : %lld (%.2f /s)\n", totalnoise1, totalnoise1/((float)(noisebins*countingtimespand)), totalnoise2,  totalnoise2/((float)(noisebins*countingtimespand)));
    printf("total signal counts:\n channel 1 = %lld (%.2f /s)\n channel 2 = %lld (%.2f /s)\n\n",totalsignal1, totalsignal1/((float)(signalbins*countingtimespand)), totalsignal2, totalsignal2/(((float)signalbins*countingtimespand)));

    /* calculate background contribution to g2 */
    signalbinsd=(double)signalbins;
    noisebinsd=(double)noisebins;

    bgg2=((totalsignal1/signalbinsd-totalnoise1/noisebinsd)*totalnoise2/noisebinsd+(totalsignal2/signalbinsd-totalnoise2/noisebinsd)*totalnoise1/noisebinsd+totalnoise1/noisebinsd*totalnoise2/noisebinsd)*signalbins*timespan/((double)countingtimespan);
    bgg2N=((totalsignal1/signalbinsd-totalnoise1/noisebinsd)*totalnoise2/noisebinsd+(totalsignal2/signalbinsd-totalnoise2/noisebinsd)*totalnoise1/noisebinsd+totalnoise1/noisebinsd*totalnoise2/noisebinsd)/(totalsignal1/signalbinsd*totalsignal2/signalbinsd);

    printf("Unnormalized dark count contribution to g2 = %lf\n", bgg2);
    printf("Normalized dark count contribution to g2 = %.4lf\n", bgg2N);
    printf("-----------------------------------------------------------\n");
    free(histo); /* clean up buffer */
    fclose(outhandle);
    return 0;
}

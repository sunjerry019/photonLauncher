/* program to read in raw event files from the timestamp card for processing 
   into a g(2) function. It outputs g2 that are normalized 
   1. using the average signal rates at the end of the process;
   2. every few seconds to remove possible artifacts due to signal rate drift 
      during the process of data acquisition. 

   This program doesn't only consider subsequent events when generating the g2 histogram.
   It creates the real g2, showing the long term intensity correlation of the light field.
  
   
   usage:  g2real [-i infile] [-o outfile] [-m maxbin] [-t binsize] [-c channels] [-s signalthreshold] [-n noisethreshold] 

   options/parameters:

   -i infile:    source of the raw data stream from the timestamp card.

   -o outfile:   target output file. if not chosen, stdout is used.

   -t binwidth:  width of a time bin in the g2 function in 1/8 nsec

   -m numbins:   number of timing bins in the g2 function. default is set to 4000

   -c channel: 	 input channels of the g2 function (either on of 01,02,03,12,13,23)

   -s signalthreshold:   counts per second in 1st and 2nd channel above which a bin is considerd to contain signal 

   -n noisethreshold:    count per second in 1st and 2nd channel below which a bin is considered to contain only noise 
   
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
#define COUNTINGTIMESPAN 120000000 /* the count monitor duration in 125psec */
#define DEFAULT_EXTRAPHASE 0

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
    "threshold must not be negative.",
    "error converting extra phase or phase out of 0..0x1ff", /* 15 */
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
    long long int timespan=DEFAULT_TIMESPAN; //the size of a time bin in the g2
    unsigned long long t1, pattern; //timing and input channel of an event
    struct rawevent inbuf[INBUFSIZE]; /* input buffer */
    FILE *inhandle;
    FILE *outhandle;
    int timebinnumber = DEFAULT_BINNUM; /* number of bins in g2 */
    int index=0, retval=0; /* variables to handle input buffer, initialize index to avoid segmentation fault */
    int *histo; /* pointer to unnormalized g2 target array */
    int *temphisto; /* pointer to temporary g2 target array (if the counts is smaller than signal threshold , this data is removed*/
    double *histoN; /*pointer to g2 array which add up all normalized g2 from each processed data chunk*/
    double N, Ntotal, bgcont, ss; /*Normalization constant*/
    int i,ip;
    int extraphase = DEFAULT_EXTRAPHASE; /* phase pattern to sort */
    int ppat; /* for storing phase pattern */
    float center;
    unsigned long long rollovercorrection=0;
    unsigned long long totalnoise1=0,totalnoise2=0;
    unsigned long long totalsignal1=0,totalsignal2=0;
    unsigned long long temptotalsignal1=0, temptotalsignal2=0; /*store signal rates for a short period of time */
    unsigned long long bincnt1=0, bincnt2=0; /* record the number of counts in channel 1 and channel 2 within a counting time span */
    unsigned long long bincnt3=0; /* record the number of with pattern mask different from that of chan 1 and chan2 */
    unsigned long long signalbins=0, noisebins=0, tempsignalbins=0;
    unsigned long long signalthreshold=0; /*count rate above which g2 is considered*/
    unsigned long long noisethreshold=0; /*count rate below which a bin is considered to contain only noise*/
    unsigned long long countingtimespan=COUNTINGTIMESPAN;
    unsigned long long oldbintime=0; /*record the starting time of current 10ms bin*/
    unsigned long long timezero=0; /*record the time of the first event*/
    unsigned long long oldpattern, oldt1, delay=0, maxdelay;
    unsigned long long channel1 = DEFAULTCHANNEL1;
    unsigned long long channel2 = DEFAULTCHANNEL2;
    unsigned long long channelopt = 01;
    unsigned long long timingch1[400000]; /* store event timing for channel 1 in memory for processing later*/ 
    unsigned long long timingch2[400000]; /* store event timing for channel 2 in memory for processing later*/ 
    int storagesize=300000; /* store the max number of events timingch1 and timingch2 can store. */
    int steventnotemp1=0, steventnotemp2=0; /* indicate the numbers of events stored in timingch1 and timingch2 temporarily (because the data can be thrown away if the number of counts in the a bin is too small. */
    int steventno1=0, steventno2=0; /* indicate the numbers of events stored in timingch1 and timingch2 */
    int procpoint1=0, procpoint2=0; /* pointers that indicate the position of the processed data in timingch arrays*/
    int blockno=0; // store the numbers of processed data blocks, needed for final normalization
    double signalthresholdd=0; 
    double noisethresholdd=0;
    double countingtimespand=0;
    double signalbinsd=0, noisebinsd=0; /* create double copies to avoid silly integer/integer problems */
    double bgg2=0, bgg2N=0; /*background contribution to the g2*/
    int enoughdata=1; /* this is a flag indicating that there are still enough data in the timingch1 and timingch2 for g2 processing */
    int biggerthanmaxdelay=1; /* this is a flag indicating that there are still enough data in the timingch1 and timingch2 for g2 processing */

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
	    case 's': /* threshold of count rates in 1st channel and 2nd channel above which a time bin consist of real signal */
		if (1!=sscanf(optarg,"%lli",&signalthreshold)) return -emsg(13);
		if (signalthreshold<0) return -emsg(14);
                break;
	    case 'n': /* threshold of count rates in 1st channel and 2nd channel below which the bin is considered to contain only noise */

		if (1!=sscanf(optarg,"%lli",&noisethreshold)) return -emsg(13);
		if (noisethreshold<0) return -emsg(14);
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
    signalthresholdd = signalthreshold*0.000000000125*countingtimespan;
    noisethresholdd = noisethreshold*0.000000000125*countingtimespan;
    countingtimespand= countingtimespan*0.000000000125;
    printf("input file: %s\n", infilename);
    printf("output file: %s\n", outfilename);
    printf("   signal threshold = %.1lf/ %.1lf ms\n", signalthresholdd, countingtimespand*1000);
    printf("   noise threshold = %.1lf/ %.1lf ms\n", noisethresholdd, countingtimespand*1000);
    printf("   size of time bin of g2 histogram = %lld x 125ps\n", timespan);
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
    oldt1 = t1;
    oldbintime = t1;
    timezero = t1;

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

            //check for timing rollover problem
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

            for (ip=0;(pli[ip]>=0) && (pli[ip]!=ppat);ip++);
            if (pli[ip]<0) continue;   /*only take good patterns */
    
            //divide timing data into ~8-15ms block. Use the data in the block later once we know the contain real signal 
            if((t1-oldbintime)/countingtimespan>0)
            {
                oldbintime+=((t1-oldbintime)/countingtimespan)*countingtimespan;

                /*record temp histogram into final histogram if count rate above signal threshold*/
                if ((double)bincnt1+(double)bincnt2>(2*signalthresholdd))
                {
                    steventno1=steventnotemp1;
                    steventno2=steventnotemp2;
                    signalbins++;
		    tempsignalbins++;
                    totalsignal1+=bincnt1;
                    totalsignal2+=bincnt2;
		    temptotalsignal1+=bincnt1;
		    temptotalsignal2+=bincnt2;
                }
                else if((double)bincnt1<=noisethresholdd && (double)bincnt2<=noisethresholdd)
                {
                    noisebins++;
                    totalnoise1+=bincnt1; 
                    totalnoise2+=bincnt2;
		    steventnotemp1=steventno1;
		    steventnotemp2=steventno2;
                }
                else
		{
		    steventnotemp1=steventno1;
		    steventnotemp2=steventno2;
		}

                bincnt1=0; /*clear previous bin counts*/
                bincnt2=0; /*clear previous bin counts*/
                
		/* if the timingch1 and timingch2 arrays are almost full, analyze the g2 function from these data first */
		if((steventno1>storagesize-signalthreshold)||(steventno2>storagesize-signalthreshold))
		{
                    enoughdata=1;
		    procpoint1=0;
		    procpoint2=0;

                    // process while there are still enough data in timingch1 and timingch2
                    while((enoughdata==1)&&(procpoint1<steventno1))
		    {
		        biggerthanmaxdelay=0;

                        /*procpoint2 is used to make sure the time delay is not calculated over every element in the array */
                        for(i=procpoint2;i<steventno2;i++)
			{
                            if(timingch1[procpoint1]>=timingch2[i])
			    {
                                procpoint2=i;
			    }
			    else
			    {
                                delay=timingch2[i]-timingch1[procpoint1];
                                if(delay<maxdelay)
				{
                                    histo[delay/timespan]++;
                                    temphisto[delay/timespan]++;
				}
				else //the delay is bigger than the maximum g2 delay range specified by the user. Stop checking further
				{
				    biggerthanmaxdelay=1;
				    break;
				}
			    }
			}

			 /* when biggerthanmaxdelay==0 this means that last event in channel has a timing smaller than the maximum delay we are interested in. Then there is not enough data in the array and we should stop processing and start to get more data. */
                        if(biggerthanmaxdelay==0||procpoint1==steventno1-1)
			{
			    
			    N=temptotalsignal1*temptotalsignal2*timespan/((double)tempsignalbins*countingtimespan);

			    for(i=0;i<timebinnumber;i++)
			    {
				histoN[i]+=(temphisto[i]/N);
				temphisto[i]=0;
			    }
                            enoughdata=0; //indicate that the data in timingch1 is too few. stop processing.
			    /*remove processed points in timingch */
			    for(i=procpoint1+1;i<steventno1;i++)
			    {
                                timingch1[i-procpoint1-1]=timingch1[i];
			    }
			    for(i=procpoint2+1;i<steventno2;i++)
			    {
                                timingch2[i-procpoint2-1]=timingch2[i];
			    }

                            steventno1-=(procpoint1+1);
                            steventno2-=(procpoint2+1);
		            steventnotemp1=steventno1;
		            steventnotemp2=steventno2;
			    tempsignalbins=0;
			    temptotalsignal1=0;
			    temptotalsignal2=0;
			    blockno++;
			}
			procpoint1++;
		    }
		}
            }

            oldt1=t1; 
 
            if(pattern==channel1)
            {
                    bincnt1++;
		    timingch1[steventnotemp1]=t1;
		    steventnotemp1++;
            }
            else if(pattern==channel2)
            {
                    bincnt2++;
		    timingch2[steventnotemp2]=t1;
		    steventnotemp2++;
            }
	    else
	    {
		bincnt3++;
	    }
	}
    }
    fclose(inhandle);
 
    //calculates normalization constants and background contribution
    Ntotal=totalsignal1*totalsignal2*timespan/((double)signalbins*countingtimespan);
    bgcont=totalnoise1*totalsignal2*timespan/((double)noisebins*countingtimespan)
          +totalnoise2*totalsignal1*timespan/((double)noisebins*countingtimespan)
          -totalnoise1*totalnoise2*signalbins*timespan/((double)noisebins*noisebins*countingtimespan);
    ss=(totalsignal1/(double)signalbins-totalnoise1/(double)noisebins)*(totalsignal2/signalbins-totalnoise2/noisebins)*timespan*signalbins/((double)countingtimespan);
    
    signalbinsd=(double)signalbins;
    noisebinsd=(double)noisebins;

    bgg2=((totalsignal1/signalbinsd-totalnoise1/noisebinsd)*totalnoise2/noisebinsd+(totalsignal2/signalbinsd-totalnoise2/noisebinsd)*totalnoise1/noisebinsd+totalnoise1/noisebinsd*totalnoise2/noisebinsd)*signalbins*timespan/((double)countingtimespan);
    bgg2N=((totalsignal1/signalbinsd-totalnoise1/noisebinsd)*totalnoise2/noisebinsd+(totalsignal2/signalbinsd-totalnoise2/noisebinsd)*totalnoise1/noisebinsd+totalnoise1/noisebinsd*totalnoise2/noisebinsd)/(totalsignal1/signalbinsd*totalsignal2/signalbinsd);

   /* open out file */
    if (outfilename[0]) {
	outhandle=fopen(outfilename,"w");
	if (!outhandle) return -emsg(7);
    } else {outhandle=stdout; };
    
    /* print result */

    /* output histogram */
    fprintf(outhandle,"bin No.\tdelay\tun_g2a\tn_g2a\tn_g2b\tun_g2b\tco_g2\n");
    for (i=0;i<timebinnumber;i++) {
        center = ((i*timespan)+timespan/2.0f)*0.125;
	fprintf(outhandle,"%d\t%0.3f\t%d\t%.3lf\t%.3lf\t%.3lf\t%.3lf\n",i,center,histo[i],histo[i]/Ntotal, histoN[i]/blockno, histoN[i], (histo[i]-bgcont)/ss);
    }

    /* Print comments in the output file*/

    fprintf(outhandle, "\ninput file: %s\n", infilename);
    fprintf(outhandle, "output file: %s\n", outfilename);
    fprintf(outhandle, "   signal threshold = %.1lf/ %.1lf ms\n", signalthresholdd, countingtimespand*1000);
    fprintf(outhandle, "   noise threshold = %.1lf/ %.1lf ms\n", noisethresholdd, countingtimespand*1000);
    fprintf(outhandle, "   size of time bin of g2 histogram = %lld x 125ps\n", timespan);
    fprintf(outhandle, "   mask of channel 1 = %lld , mask of channel 2 = %lld\n\n",channel1, channel2);

    fprintf(outhandle, "total number of other patterns = %lld\n",bincnt3);
    fprintf(outhandle, "total number of signal bins = %lld, noise bin = %lld\n",signalbins, noisebins);
    fprintf(outhandle, "total noise counts:\n channel 1 : %lld (%.2f /s)\n channel 2 : %lld (%.2f /s)\n", totalnoise1, totalnoise1/((float)(noisebins*countingtimespand)), totalnoise2,  totalnoise2/((float)(noisebins*countingtimespand)));
    fprintf(outhandle, "total signal counts:\n channel 1 = %lld (%.2f /s)\n channel 2 = %lld (%.2f /s)\n\n",totalsignal1, totalsignal1/((float)(signalbins*countingtimespand)), totalsignal2, totalsignal2/(((float)signalbins*countingtimespand)));

    fprintf(outhandle, "Unnormalized dark count contribution to g2 = %lf\n", bgg2);
    fprintf(outhandle, "Normalized dark count contribution to g2 = %.4lf\n\n", bgg2N);
    fprintf(outhandle, "un_g2a:\traw histogram of delay without unnormalization.\n");
    fprintf(outhandle, "n_g2a:\tg2 normalized by using the average signal rate in channel 1 and channel 2.\n");
    fprintf(outhandle, "n_g2b:\ttime-weighted average of different g2s normalized every few ten miliseconds or a few seconds. The hope is to remove artificial contribution to g2 due signal rate drift.\n");
    fprintf(outhandle, "un_g2b:\tsimilar to n_g2a except it is the sum of many  g2s normalized every few ten miliseconds or a few seconds. It is used if one needs to join the g2 data accumulated in different file.\n");
    fprintf(outhandle, "co_g2:\tnormalized g2 corrected for the background possonian noise. The correction is done by using average signal and noise rates. Normalization is not done for every few seconds.\n\n");

    fprintf(outhandle, "processed by: g2real\n");

    //print comments on the screen
    printf("total number of other patterns = %lld\n",bincnt3);
    printf("total number of signal bins = %lld, noise bin = %lld\n",signalbins, noisebins);
    printf("total noise counts:\n channel 1 : %lld (%.2f /s)\n channel 2 : %lld (%.2f /s)\n", totalnoise1, totalnoise1/((float)(noisebins*countingtimespand)), totalnoise2,  totalnoise2/((float)(noisebins*countingtimespand)));
    printf("total signal counts:\n channel 1 = %lld (%.2f /s)\n channel 2 = %lld (%.2f /s)\n\n",totalsignal1, totalsignal1/((float)(signalbins*countingtimespand)), totalsignal2, totalsignal2/(((float)signalbins*countingtimespand)));

    printf("Unnormalized dark count contribution to g2 = %lf\n", bgg2);
    printf("Normalized dark count contribution to g2 = %.4lf\n", bgg2N);
    printf("-----------------------------------------------------------\n");


    free(histo); /* clean up buffer */
    free(histoN); /* clean up buffer */
    free(temphisto); /* clean up buffer */
    fclose(outhandle);
    return 0;
}

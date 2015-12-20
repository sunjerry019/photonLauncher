/*
To extract last 4 bits of timing info from each timestamp entry and generate a histogram.
Takes in raw timestamp files.

Usage: ./[this program] -i [infile] -o [outfile]

   -i infile:    source of the raw data stream from the timestamp card.
                 If not specified, stdin is chosen

   -o outfile:   target for the count result. if not chosen, stdout is used.

******************
INITIAL MOTIVATION
******************
To get the nominal 125ps resolution, the timestamp card takes in a 10MHz reference clock, multiplies it to a 500MHz clock signal, then 'subdivides' the 2ns period into 16 bins (4 bits). Ideally, each of these 16 bins are of equal length [125ps each], but in practice it's not quite exact. This will vary between devices, but on the same device it should be the same across all the channels.

This can show up in our results, eg in a g2 curve, small ripples/oscillations can occur where you might actually expect a straight line or a nice curve. This became an issue because we want to look at the g2 histograms from the timereversal expt in close detail.

To characterize the timestamp, have it measure a random source (eg APD measuring ambient light). The g2 should be totally flat if we look at the distribution of the last 4 bits of each timestamp entry. Any structure/fluctuations (above poisonnian error) we measure will be due to this unequal binning. From this, we can infer the "true" length of each of these 16 bins.


Victor L, Oct 2015
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FNAMELENGTH 200  /* length of file name buffers */
#define FNAMFORMAT "%200s"   /* for sscanf of filenames */
#define INBUFSIZE 4096 /* choose 32kbyte large input buffer */


/* error handling */
char *errormessage[] = {
    "No error.",
    "error parsing input file name",
    "error parsing output file name",
    "cannot open input file", 
    "error opening output file",
    "cannot malloc histogram buffer.", /* 5 */
};

int emsg(int code) {
    fprintf(stderr,"%s\n",errormessage[code]);
    return code;
}

typedef struct rawevent {unsigned int cv; /* most significan word */
    unsigned int dv; /* least sig word */} re;

int main (int argc, char *argv[]) {
    
    int opt; /* command parsing */
    char infilename[FNAMELENGTH]="";
    char outfilename[FNAMELENGTH]="";
    FILE *outhandle;
    FILE *inhandle;
    struct rawevent inbuf[INBUFSIZE]; /* input buffer */
    int index, retval; /* variables to handle input buffer */


    long long int cnt=0;
    long long int *histo;
    unsigned long long t1;
    unsigned int last4bits;
    int i;

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
    }
  }
  /* try to open input file */
    if (infilename[0]) {
  inhandle=fopen(infilename,"r");
  if (!inhandle) return -emsg(3);
    } else {inhandle=stdin; };
    
    /* open out file */
    if (outfilename[0]) {
  outhandle=fopen(outfilename,"w");
  if (!outhandle) return -emsg(4);
    } else {outhandle=stdout; };

  /* allocate memory for storing the hsitogram bins */
  histo=(long long int*)calloc(16,sizeof(long long int)); /* allocate buffer */
  if (!histo) return -emsg(5);

  //MAIN LOOP//
  while (0<(retval=fread(inbuf, sizeof(struct rawevent), INBUFSIZE, inhandle))) {
    for (index=0;index<retval;index++) {
      /* extract timing information */
      t1=((unsigned long long)inbuf[index].cv<<17) + ((unsigned long long )inbuf[index].dv >>15);
      last4bits = t1 & 0xf;

      histo[last4bits]++;
      cnt++;
    }
  }

  //OUTPUT HISTOGRAM//
  fprintf(outhandle,"#Histogram of last 4 bits of timing info of each timestamp entry.\n");
  fprintf(outhandle,"#Total counts: %lld \n", cnt);
  fprintf(outhandle,"#bin no, counts, fraction, duration (assuming 125ps/bin [nominal])\n");
  for(i=0;i<16;i++){
    fprintf(outhandle, "%d %lld %.5g %.5g\n", i, histo[i], (double)histo[i]/cnt, (double)2000*histo[i]/cnt);
  }

fclose(inhandle);
fclose(outhandle);
return 0;
}
/* program to generate a programming pattern for the DDS AD9958 chip on the
   basis of some plain commands sent to the stdin of this program. Individual
   commands are converted into binary code which can be directly piped into 
   the EP2 device file. The program also can use the EP1 commands if the
   connected device is the dds device node directly.

   usage: dds_encode [-d device] [-E | -T ] [-R] [-i sourcefile] [-a refamp]
                     [-q] [-b basedivider]

   options:
   -d device :       Device node. If if device is "-", then stdout is used, 
                     and the EP1 option disabled. Otherwise, the
                     location /dev/ioboards/dds0 is used by default. If a file 
		     is used instead, the control commands used to prepare
		     a certain configuration can be stored, and piped to the
		     DDS separately with a simple cat >device command later.

   -E                Allow the usage of the EP1 commands. This is the default.

   -T                Disallow the usage of EP1 commands, treat output device
                     as a plain stream only. Needs to be set when a file is
		     used to store the commands.

   -R                Reset before loading. Perform a device reset before sending
                     the specified command. This, however, does only a master
		     reset, not a sensible filling of the registers.

   -i sourcefile     Take the command data not from stdin, but from an input
                     file.
   -a refamp         defines reference amplitude in millivolt directly instead
                     of taking the default value of 480 mV. Reference amplitude
		     is the peak amplitude the DDS/amplifier section can
		     generate.
   -q                Quiet option. This is only useful for boards which use
                     the internal clock of the cypress chip and can keep the
		     sync_out muted.
   -b basedivider    This value is the PLL divider and determines the master
                     clock. The value of <basedivider> is an integer with
		     values between 1 and 10, corresponding to frequencies form
		     50 MHz to 500 MHz.

   Commands can be separated either by semicolons or newlines. Not sure if
   this is universal, but it may work. Here is a list of commands with
   their parameters:


   RESET
      issues a command to reset the DDS chip if possible

   MODE <modulation>
      selects the modulation type, which can be one of SINGLETONE, AM, FM or PM.
      At the moment, this selection applies to both channels commonly, but that
      should be possible to change.

   SWEEP <modulation> <channel> <deltarise> <deltafall> <risetime> <falltime> 
      complex sweep command. Modulation is as in Mode, and determines which
      of the aspects (amp, freq, phase), is sweeping upon change of the
      profile pins. Channel fixes the sweep parameters for a given channel,
      and can be 0, 1 for individual chan programming or 2 for both.
      
   LEVELS <number>
     Specifies how many modulation levels are present. Possible choices are:
      16 :profile pins change 16 different levels for channel 0
      4  : Two profile pins change the state of channel 0, the other for ch 1
      3  : This is some experimental rampup/down plus modulation mode
      2  : two level modulation, no ramps.

   AMPLITUDE <channel> <value> [units]
      determines the amplitude of a given channel. The amplitude can come with
      a unit (V, mV, Vpp, mVpp, Vrms, mVrms, dBm, ampunits) or not if the
      amplitude should be fixed in device units (0...1023). The channel
      argument can be 0, 1 for individual channel programming, or 2 for both.

   FREQUENCY <channel> <freq> [units] 
      determines the frequency of a given channel. It can come with
      a unit (Hz, kHz, MHz, frequnits) or not if the frequency should be fixed
      in device units (0...0xffffffff). The channel argument can be 0, 1 for
      individual programming, or 2 for both.

   NOAMP <channel>
      switches the amplitude multiplier stage of a given channel off and gives
      full amplitude.


   AMPSCALE <para>
      supposed to set the full range of each DAC; not yet implemented.

   PHASE <channel> <value> [units]
      determines the phase of a given channel. It can come with a unit 
      (deg, rad, mrad, phaseunits) not if the phase should be fixed
      in device units (0...0x3fff). The channel argument can be 0, 1 for
      individual programming, or 2 for both.

   TUNING <register> <value> [units]
      this sets one of the 15 additional tuning registers (1..15) to a
      frequency, amplitude or phase. Choose appropriate units to make sure
      that the register size matches the modulation type. These registers
      are selected (together with the basic amp/freq/phase settings) when
      modulation is applied via the profile pins. Tuning register 1 is also
      used to set the target frequency for the linear sweep.

   REFAMP <value> <units>
      This changes the reference amplitude chosen by default or by the
      commandl line parameter. Absolute units must be chosen.

   # <comment>
      All text after the # is ignored until the next delimiter ( a newline or 
      semicolon) and can be used for comments in a batch file


   Example 1:
   Setting up two channels with different frequencies and same amplitude in
   singletone mode can be done by sending the following command sequence to
   the program:

      Levels 2; Mode singletone
      frequency 1 125 MHz ; frequency 0 1134.77 kHz
      amplitude 2 1 Vrms

   Example 2:
   Setting up channel 0 for 16 level frequency modulation. channel 1 delivers
   a constant signal at 100 MHz with -3.5 dBm.

      Mode FM ; Levels 16
      amplitude 1 -3.5dBm ; frequency 1 100 MHz
      # setting of the base registers
      amplitude 0 0.0dBm ; frequency 1 MHz
      # the rest of the tuning registers
      Tuning 1 1.01 MHz ; Tuning 2 1.02 MHz ; Tuning 3 1.03 MHz
      Tuning 4 1.04 MHz ; Tuning 5 1.05 MHz ; Tuning 6 1.06 MHz
      Tuning 7 1.07 MHz ; Tuning 8 1.08 MHz ; Tuning 9 1.09 MHz
      Tuning 10 1.10 MHz ; Tuning 11 1.11 MHz ; Tuning 12 1.12 MHz
      Tuning 13 1.13 MHz ; Tuning 14 1.14 MHz ; Tuning 15 1.15 MHz

   Example 3:
   Setting up channel 0 for a linear sweep in frequency from 150 MHz to
   170 MHz with a rise rate of 1 kHz/msec and a fall rate of 100 kHz/usec.
   the update rates are chosen to 200x and 1x syncclk (8nsec), resulting in
   a rise word of 1000Hz/msec*0.0016msec = 1.6Hz and in a fall word of
   100kHz/usec*0.008usec=800Hz. Since the frequency resolution is
   around 0.1 Hz, there is a significant uncertainty in the rise time.
   
     Mode FM ; Levels 2
     Amplitude 0 0dB ; frequency 0 150 MHz; Tuning 1 170 MHz
     Sweep FM 0 1.6Hz 800Hz 200 1

   History:
      added refamp selection and fixed unit parsing code 1.10.09chk
      fixed sensitivity against keywords in coments 4.4.10chk
 
*/

#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <ctype.h>
#include <math.h>

#include "usbdds_io.h"


#define DEFAULT_DEVICE "/dev/ioboards/dds0"
#define DEFAULT_INPUTSOURCE "-"
#define DEFAULT_EP1MODE 1
#define DEFAULT_REFAMP 460  /* amplitude in millivolt */
#define DEFAULT_FR1END 0x00 /* keep sync clk out on */ 
#define DEFAULT_BASEDIVIDER 10 /* for 500 MHz core frequency */

#define FILENAMLEN 100
#define MAXINLEN 100


/* global variables */
FILE* outhandle; /* for output of data */
int EP1mode = DEFAULT_EP1MODE; /* 0: don't use ioctls, 1: Do use them */
char outdata[20]; /* for sending stuff out */
int fr1end = DEFAULT_FR1END; /* keeps the low 8 bits of FR1 */
int basedivider = DEFAULT_BASEDIVIDER; /* default frequency */ 

/* error handling */
char *errormessage[]= {
  "No error.",
  "device not found.", /*1 */
  "Cannot parse input file name",
  "Cannot parse output file name",
  "Cannot open input target",
  "Cannot open output target", /*5 */
  "Cannot stat output target",
  "Non-char device targets cannot have EP1 commands",
  "Unknown token",
  "No valid mode found in MODE command",
  "Cannot do reset without EP1 method", /* 10 */
  "Command not yet implemented",
  "cannot parse frequency",
  "illegal frequency",
  "Cannot find proper channel",
  "cannot parse amplitude", /* 15 */
  "cannot parse phase",
  "Amplitude scale must be 0, 1, 2 or 3",
  "cannot parse integer argument",
  "cannot parse tuning argument",
  "modulation level not supported", /* 20 */
  "error parsing ramp rate",
  "rising ramp rate out of range",
  "falling ramp rate out of range",
  "cannot parse reference amplitude",
  "Reference amplitude out of range (0-2V)", /* 25 */
  "Need absolute units for reference amplitude",
  "Cannot parse base divider",
  "Base divider out of range (1..10)",
  "Frequency exceeds Nyquist baseband limit",
};

int emsg(int a){
  fprintf(stderr, "%s\n",errormessage[a]);
  return a;
}

void makeupperstring(char *string){
    int i=0;
    while (string[i]) {
	string[i]=toupper(string[i]);
	    i++;
    }
}

#define NUMCOMMANDS 14
char * commands[]={
  "",  /* 0: do nothing */
  ".", /* terminate */
  "#", /* comment line */
  "RESET",
  "MODE",
  "SWEEP", /* 5 */
  "LEVELS",
  "AMPLITUDE",
  "FREQUENCY",
  "NOAMP",
  "AMPSCALE", /* 10 */
  "PHASE",
  "TUNING",
  "REFAMP",
};

char * modestrings[] = {
    "", "SINGLETONE", "AM", "FM","PM"};
char * units[] = {
    "", "HZ","KHZ", "MHZ", "FREQUNITS", /* these are all frequency units */
    "AMPUNITS", "V", "MV", "VPP", "VRMS","MVPP", "MVRMS", "DBM",
    "PHASEUNITS", "DEG", "MRAD", "RAD",
};
#define INPUTFREQUENCY 50000000.
double freqmultiplier[5];
double maxfrequency;

double refamp = DEFAULT_REFAMP;
double referencesteps = (1023/(DEFAULT_REFAMP/1000.));
double amplitudemultiplier[9] = {1, 1, /* no units */
				 1, 0.001, 0.5, 1.4142135624,
				 0.0005, 0.0014142135624,
				 1 /* dBm->V furhter down there */
};

#define PHASESTEP 0x4000
double phasemultiplier[5]={1,1,PHASESTEP/360., PHASESTEP/3.141592654/2000.,
			   PHASESTEP/3.141592654/2};

char channelpattern[3]={0x40, 0x80, 0xc0};

/* This function parses a number, which can be a float command. It ignores
   non-numerical characters at the beginning, and terminates with the last
   non-numerical number at the end. Return value is 0 if successful, 
   1 otherwise. The value is returned via the pointer to a double. Also,
   the newposition points to the new position after the parsing. */
int parse_number(char *string, int *newposition, double *value){
    int i=*newposition;
    int decposition = -1; int sign=0;
    char c;
    /* ignore leading whitespace */
    while (string[i]==' ' || string[i]=='\t' || 
	   string[i]==',' || string[i]==':') i++; /* needs null termination */
    if (!string[i]) return 1; /* end of string */
    *value = 0.0;
    if (string[i]=='-') {
	sign=1;i++;
    }
    do {
	c=string[i];
	//printf("parse pos: %i, >%c<, decp: %d\n",i,c,decposition);
	if (c=='.') {
	    if (decposition>=0) return 1; /* we have already a decimal point */
	    decposition=0;i++; continue;
	}
	if ((c<'0') || (c >'9')) break; /* end of number */
	*value = *value * 10.0 + (c-'0');
	if (decposition>=0) decposition++;
	i++;
    } while (1);
    
    while (decposition>0) {
	*value /= 10. ;
	decposition--;
    }
    
    if (sign) *value = -*value;
    *newposition =i;
    return 0;
}


/* This function searches for a keyword, and returns its index or 0 if none
   is found. newposition returns the position behind the found token,  */

int find_token(char *string, int *newposition, 
	       char *tokenlist[], int numtokens) {
    int i;
    char *retval = NULL;
    int np=*newposition;
    
    /* eat whitespace */
    while (string[np]==' ' || string[np]=='\t' || 
	   string[np]==',' || string[np]==':') np++;
    
    for (i=numtokens-1;i>0;i--) {
	if((retval=strstr(&string[np],tokenlist[i]))) break;
    }
    if (!i) return 0; /* no token found */
    if ((int)(retval-string) != np) return 0; /* not before some whitespace */
    *newposition = (int)(retval - string) + strlen(tokenlist[i]);
    return i;
}


int parse_command(char *cmd){
    int newposition=0;
    int retval,j;
    double rawvalue;
    int channel, finalvalue;


    /* check for empty line */
    while (cmd[newposition]==' ' || cmd[newposition]=='\t' || 
	   cmd[newposition]==',' || cmd[newposition]==':') newposition++;
    /* terminate string on first # sign found */
    for (j=newposition; cmd[j]; j++)
      if (cmd[j]=='#') cmd[j]=0;

    if (!cmd[newposition]) return 0; /* empty line is ok */

    /* convert into uppercase - ugly, modifies string...*/
    makeupperstring(cmd);

    /* find command index */
    retval=find_token(cmd, &newposition, commands, NUMCOMMANDS);
    switch (retval) {
	case 0: /* no token found */
	    return -8; /* unknown token */
	case 1: /* terminate script */
	    return 1;
	case 2: /* this is a comment line, ignore */
	    break; /* we parse it by ignoring */
	case 3: /* reset */
	    if (EP1mode) {
		ioctl(fileno(outhandle),Full_DDS_Reset);
		return 0;
	    }
	    return -10;
	case 4: /* set mode */
	    retval=find_token(cmd, &newposition, modestrings, 5);
	    if (!retval) return -9;
	    /* we have a valid mode - let's do something */
	    //printf("valide mode: %d\n",retval);
	    finalvalue=((retval-1)<<22) + 0x300;
	    outdata[0]=0;
	    outdata[1]=channelpattern[2]+0x36; /* both channels */
	    outdata[2]=0x03; /* CFR reg */
	    outdata[3]=(finalvalue >>16) &0xff;
	    outdata[4]=(finalvalue >> 8) &0xff;
	    outdata[5]=(finalvalue ) &0xff;
	    fwrite(outdata,1,6,outhandle);
	    fflush(outhandle);
	    break;

	case 5: /* sweep command */
      
	    /* get mode */
	    retval=find_token(cmd, &newposition, modestrings, 5);
	    if (!retval) return -9;
	    /* we have a valid mode - let's do something */
	    outdata[16]=(retval-1)<<6; /* later for CFR loading */

	    /* get channel */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <0 || channel >2) return -14;
	    outdata[0]=0; outdata[1]=channelpattern[channel]+0x36;
	    
	    /* get delta 1 */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -19;	    
	    retval=find_token(cmd, &newposition, units, 16);
	    /* decide argument via unit */
	    //fprintf(stderr, "sweep unit: %d\n",retval);
	    if (retval<5) {/* let's assume frequency */
		rawvalue *= freqmultiplier[retval];
		if (rawvalue<0) return -13; /* no negative frequencies */
	  if (rawvalue>maxfrequency) return -29;
	    } else if (retval<13) { /* we have amplitude */
		/* do dBm conversion into amplitude steps */
		if (retval==12) {
		    rawvalue = pow(10.,(rawvalue-10.)/20.);
		} else if (rawvalue<0) rawvalue =-rawvalue; /* no neg amp */
		/* conversion into basic units plus longwordalign - 22bit*/
		rawvalue *= amplitudemultiplier[retval-4]*(1<<22);
		if (retval>5) rawvalue *= referencesteps;
	    } else { /* we have phase , align 14 bits to MSB */
		rawvalue *= phasemultiplier[retval-12]* (1<<18);
	    }
	    finalvalue = (unsigned int)rawvalue;
	    /* we have a tuning word */
	    outdata[2]=0x08; /* rising delta word address */
	    outdata[3]=(finalvalue >>24) &0xff;
	    outdata[4]=(finalvalue >>16) &0xff;
	    outdata[5]=(finalvalue >> 8) &0xff;
	    outdata[6]=(finalvalue ) &0xff;

	    /* get delta 2 */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -19;	    
	    retval=find_token(cmd, &newposition, units, 16);
	    /* decide argument via unit */
	    if (retval<5) {/* let's assume frequency */
		rawvalue *= freqmultiplier[retval];
		if (rawvalue<0) return -13; /* no negative frequencies */
	  if (rawvalue>maxfrequency) return -29;
	    } else if (retval<13) { /* we have amplitude */
		/* do dBm conversion into amplitude steps */
		if (retval==12) {
		    rawvalue = pow(10.,(rawvalue-10.)/20.);
		} else if (rawvalue<0) rawvalue =-rawvalue; /* no neg amp */
		/* conversion into basic units plus longwordalign - 22bit*/
		rawvalue *= amplitudemultiplier[retval-4]*(1<<22);
		if (retval>5) rawvalue *= referencesteps;
	    } else { /* we have phase , align 14 bits to MSB */
		rawvalue *= phasemultiplier[retval-12]* (1<<18);
	    }
	    finalvalue = (unsigned int)rawvalue;
	    /* we have a tuning word */
	    outdata[7]=0x09; /* falling delta word address */
	    outdata[8]=(finalvalue >>24) &0xff;
	    outdata[9]=(finalvalue >>16) &0xff;
	    outdata[10]=(finalvalue >> 8) &0xff;
	    outdata[11]=(finalvalue ) &0xff;

	    /* get rising and falling ramp rate  */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -21;
	    finalvalue=(int)rawvalue;
	    if (finalvalue<0 || finalvalue >255) return -22;
	    outdata[12]=0x07; /* ramp rate reg */
	    outdata[13]=finalvalue;
	    if (parse_number(cmd, &newposition, &rawvalue)) return -21;
	    finalvalue=(int)rawvalue;
	    if (finalvalue<0 || finalvalue >255) return -23;
   	    outdata[14]=finalvalue;

	    /* set CFR*/
	    outdata[15]=0x03; /* cfr address */
	    outdata[17]=0x43; /* dwell, linear sweep on, full DAC scale */
	    outdata[18]=0x00;
	    fwrite(outdata,1,19,outhandle);
	    fflush(outhandle);
	    break;

	case 6: /* Levels command - defines number of modulation settings */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    switch (channel) {
		case 16: /* we have 16 level modulation of output 0 */
		    finalvalue = 0x2300; /* for FR1 */
		    break;
		case 4: /* we have 4 levels for each channel */
		    finalvalue = 0x5100;
		    break;
		case 3: /* 2level with rampup/down */
		    finalvalue = 0x5400; /* not clear if we can use this */
		    break;
		case 2: /* 2level, no ramp */
		    finalvalue = 0x0000;
		    break;
		default:
		    return -emsg(20);
	    }
	    finalvalue |= ((basedivider & 0x1f)<<18); /* PLL divider */
	    if (basedivider>4) finalvalue |= 0x800000; /* VCO gain control */
	    finalvalue |= fr1end; /* eventually switch off sync clock output */
	    outdata[0]=0x01; /* FR1 */
	    outdata[1]=(finalvalue >>16) &0xff;
	    outdata[2]=(finalvalue >> 8) &0xff;
	    outdata[3]=(finalvalue ) &0xff;
	    fwrite(outdata,1,4,outhandle);
	    fflush(outhandle);
	    break;
	case 7: /* Amplitude command */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <0 || channel >2) return -14;
	    /* get raw amplitude */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -15;	    
	    retval=find_token(cmd, &newposition, &units[4], 9);
	    /* do dBm conversion into amplitude steps */
	    if (retval==8) {
		rawvalue = pow(10.,(rawvalue-10.)/20.);
	    } else if (rawvalue<0) rawvalue =-rawvalue; /* no neg amplitude */
	    /* conversion into basic units */
	    rawvalue *= amplitudemultiplier[retval];
	    if (retval>1) rawvalue *= referencesteps;
	    finalvalue = (int)rawvalue;
	    if (finalvalue>1023) finalvalue=1023;
	    /* we have a frequency */
	    //fprintf(outhandle,"set amplitude in channel %d to %08x\n",
	    //    channel, finalvalue);
	    finalvalue = (finalvalue & 0x3ff) + 0x1000;
	    outdata[0]=0; outdata[1]=channelpattern[channel]+0x36;
	    outdata[2]=0x06; /* amp reg */
	    outdata[3]=(finalvalue >>16) &0xff;
	    outdata[4]=(finalvalue >> 8) &0xff;
	    outdata[5]=(finalvalue ) &0xff;
	    fwrite(outdata,1,6,outhandle);
	    fflush(outhandle);
	    break;
	case 8: /* frequency command */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <0 || channel >2) return -14;
	    /* get frequency */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -12;	    
	    retval=find_token(cmd, &newposition, units, 5);
	    rawvalue *= freqmultiplier[retval];
	    if (rawvalue<0) return -13; /* no negative frequencies */
	    if (rawvalue>maxfrequency) return -29;
	    finalvalue = (unsigned int)rawvalue;
	    /* we have a frequency */
	    //fprintf(outhandle,"set frequency in channel %d to %08x\n",
	    //    channel, finalvalue);
	    outdata[0]=0; outdata[1]=channelpattern[channel]+0x36;
	    outdata[2]=0x04; /* tuning word 0 */
	    outdata[3]=(finalvalue >>24) &0xff;
	    outdata[4]=(finalvalue >>16) &0xff;
	    outdata[5]=(finalvalue >> 8) &0xff;
	    outdata[6]=(finalvalue ) &0xff;
	    fwrite(outdata,1,7,outhandle);
	    fflush(outhandle);
	    break;
	case 9: /* noamp command */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <0 || channel >2) return -14;
	    finalvalue=0x000000; /* amplitude stage is off */
	    outdata[0]=0; outdata[1]=channelpattern[channel]+0x36;
	    outdata[2]=0x06; /* amp reg */
	    outdata[3]=(finalvalue >>16) &0xff;
	    outdata[4]=(finalvalue >> 8) &0x3f;
	    outdata[5]=(finalvalue ) &0xff;
	    fwrite(outdata,1,6,outhandle);
	    fflush(outhandle);
	    break;
	case 10: /* ampscale command */
	    return -11;
	    if (parse_number(cmd, &newposition, &rawvalue)) return -18;
	    finalvalue=(int)rawvalue;
	    if (finalvalue<0 || finalvalue >3) return -16;
	    //fprintf(outhandle,"set amplitude scale in channel %d to %08x\n",
	    //	    channel, finalvalue);
	    break;
	case 11: /* phase command */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <0 || channel >2) return -14;
	    /* get phase */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -16;	    
	    retval=find_token(cmd, &newposition, &units[12], 5);
	    rawvalue *= phasemultiplier[retval];
	    finalvalue = ((int)rawvalue) & 0x3fff; /* 14 bit mask */
	    /* we have a phase */
	    //fprintf(outhandle,"set phase in channel %d to %08x\n",
	    //    channel, finalvalue);
	    outdata[0]=0; outdata[1]=channelpattern[channel]+0x36;
	    outdata[2]=0x05; /* phase reg */
	    outdata[3]=(finalvalue >> 8) &0x3f;
	    outdata[4]=(finalvalue ) &0xff;
	    fwrite(outdata,1,5,outhandle);
	    fflush(outhandle);
	    break;
	case 12: /* tuning command */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
	    channel=(int)rawvalue;
	    if (channel <1 || channel >15) return -14;
	    /* get argument */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -19;	    
	    retval=find_token(cmd, &newposition, units, 16);
	    /* decide argument via unit */
	    if (retval<5) {/* let's assume frequency */
		rawvalue *= freqmultiplier[retval];
		if (rawvalue<0) return -13; /* no negative frequencies */
	  if (rawvalue>maxfrequency) return -29;
	    } else if (retval<13) { /* we have amplitude */
		/* do dBm conversion into amplitude steps */
		if (retval==12) {
		    rawvalue = pow(10.,(rawvalue-10.)/20.);
		} else if (rawvalue<0) rawvalue =-rawvalue; /* no neg amp */
		/* conversion into basic units plus longwordalign - 22bit*/
		rawvalue *= amplitudemultiplier[retval-4]*(1<<22);
		if (retval>5) rawvalue *= referencesteps;
	    } else { /* we have phase , align 14 bits to MSB */
		rawvalue *= phasemultiplier[retval-12]* (1<<18);
	    }
	    finalvalue = (unsigned int)rawvalue;
	    /* we have a tuning word */
	    //printf("tuning word number %d: %08x\n",
	    //   channel, finalvalue);
	    outdata[0]=0x09+channel; /* tuning word address */
	    outdata[1]=(finalvalue >>24) &0xff;
	    outdata[2]=(finalvalue >>16) &0xff;
	    outdata[3]=(finalvalue >> 8) &0xff;
	    outdata[4]=(finalvalue ) &0xff;
	    fwrite(outdata,1,5,outhandle);
	    fflush(outhandle);
	    break;
	case 13: /* reference amplitude selection */
	    /* get raw amplitude */
	    if (parse_number(cmd, &newposition, &rawvalue)) return -15;	    
	    retval=find_token(cmd, &newposition, &units[4], 9);
	    /* do dBm conversion into amplitude steps */
	    if (retval==8) {
		rawvalue = pow(10.,(rawvalue-10.)/20.);
	    } else if (rawvalue<0) rawvalue =-rawvalue; /* no neg amplitude */
	    /* make sure we have proper units */
	    if (retval<2) return -emsg(26);
	    /* conversion into basic units (volt) */
	    rawvalue *= amplitudemultiplier[retval];
	    /* set voltage */
	    //fprintf(stderr,"new ref amp in volt: %f\n",rawvalue);
	    refamp = rawvalue /1000; /* in millivolt */
	    referencesteps = 1023/rawvalue;
	    break;
	default:
	    return -11; /* command not yet implemented */
    }

    
    return 0; /* we were able to process that command */
}

int main(int argc, char *argv[]) {
  extern int opterr; 
    int opt; /* for parsing options */
    int initialreset = 0;
    char outfilename[FILENAMLEN] = DEFAULT_DEVICE;
    char infilename[FILENAMLEN] = DEFAULT_INPUTSOURCE;
    FILE* inhandle; /* for input of data */
    int retval;
    struct stat filestatus;   /* for probing for character file */ 
    double refamp = DEFAULT_REFAMP;
    double frequencystep;

    /* parser stuff */
    char cmd[MAXINLEN+1];
    int idx, ir, cmo;

    /* parse input parameters */
     opterr=0; /* be quiet when there are no options */
     while ((opt=getopt(argc, argv, "d:ETRi:a:qb:")) != EOF) {
	 switch (opt) {
	     case 'E': /* set EP1 mode */
		 EP1mode=1;
		 break;
	     case 'T': /* disable EP1 mode */
		 EP1mode=0;
		 break;
	     case 'R': /* do initrial reset */
		 initialreset=1;
		 break;
	     case 'i': /* parse input device */
		 if (sscanf(optarg,"%99s",infilename)!=1 ) return -emsg(2);
		outfilename[FILENAMLEN-1]=0; /* close string */
		break;
 	    case 'd': /* enter device file name */
		if (sscanf(optarg,"%99s",outfilename)!=1 ) return -emsg(3);
		outfilename[FILENAMLEN-1]=0; /* close string */
		break;
	     case 'a': /* reference amplitude */
		 if (sscanf(optarg,"%lf",&refamp)!=1) return -emsg(24);
		 break;
	     case 'q': /* quiet mode. Switches off sync clock output */
	         fr1end=0x20;
	         break;
	     case 'b': /* selection of base divider for main frequency */
	         if (sscanf(optarg,"%i",&basedivider)!=1) return -emsg(27);
		 if ((basedivider<1) || (basedivider>10)) return -emsg(28);
		 break;
	 }
     }

     /* establish the frequency multiplier table */
     frequencystep=((1ll<<32)/(50000000.*basedivider));
     freqmultiplier[0]=frequencystep;
     freqmultiplier[1]=frequencystep;
     freqmultiplier[2]=1000*frequencystep;
     freqmultiplier[3]=1000000*frequencystep;
     freqmultiplier[4]=1.0;
     maxfrequency=(1ll<<31)-1;
     
     /* check input source */
     inhandle=stdin;
     if (strcmp(infilename,"-")) {
	 inhandle = fopen(infilename,"r");
	 if (!inhandle) return -emsg(4);
     }
	
     /* check output consistency and open file */
     outhandle=stdout;
     if (strcmp(outfilename,"-")) {
	 outhandle = fopen(outfilename,"w+");
	 if (!outhandle) return -emsg(5);
	 
	 retval=stat(outfilename, &filestatus);
	 if (EP1mode) {
	     if (retval) return -emsg(6);
	     if (!S_ISCHR(filestatus.st_mode)) return -emsg(7); /* cannot EP1 */
	 }
     }

     /* generate reference amplitude */
     if (refamp <= 0.0 || refamp >2000) return -emsg(25); /* out of range */
     referencesteps = 1023/(refamp/1000.);

     do {
	 /* read in one line, waiting for newline or semicolon. Not nice
	    but works... */
	 idx=0;
	 while ((ir=fread(&cmd[idx], 1,1,inhandle))==1 && idx<MAXINLEN) {
	     if (cmd[idx]=='\n' || cmd[idx]==';') break;
	     idx++;
	 };
	 cmd[idx]='\0';

	 /* call command parser */
	 cmo=parse_command(cmd);
#ifdef DEBUG
    printf("parser return: %d\n",cmo);
#endif
     } while (!cmo);
     
     if (cmo<0) return -emsg(-cmo);
     
     /* close files */
     if (strcmp(outfilename, "-")) fclose(outhandle);
     if (strcmp(infilename, "-")) fclose(inhandle);

     return 0;
}

/*This program is intended to generate arbitrary patterns for the pattern generator card. 
 * 
 * Usage: arbitrarypatterngenerator [-i INPUTFILE] [-o OUTPUT] [-d DELAYFILE] [-h] (use option h for help)
 * 
 Each line of the pattern is 64 bits: 48 output bits for generating an output pattern, 15 address bits (controlword) to generate the next address in the table, and 1 clock bit. When clock bit is set to FAST (SLOW), that line takes 2 (200) clock cycles to execute, e.g. 20ns (2us) for 100MHz clock. 

The full address of each line is 19 bits long, giving 2^19=524288 lines. Each 'table' is given by the 15 address bits (total 2^15=32768 lines) and switching between tables is done via 4 external input bits. One can set specific output bits to feed back to the inputs (table control bits) via the control_input token.

This program requires two inputs: a main pattern file and a delay file to compensate for delays in different channels. For specific syntax refer to help output or sample template files. 

The accepted tokens in the pattern file are:
* 1) clock [to specify clock rate]
* 2) control
* 	a) trigger_mask [set trigger mask bit]
* 	b) trigger_input [set trigger input channel]
* 	c) control_input [set table control bits]
* 	d) control_byte [set output byte for which to use table control bits] *YET TO IMPLEMENT*
* 3) sequential
* 	Just a sequence of lines. User specifies duration and output pattern of each line. Jumps to specified table when it ends. Will automatically overflow to next table if table is full (be careful with table numbers...)
* 4) triggered
* 	Counts clicks from trigger input channel (e.g. from detector) and discriminates between two specified count rates. User specifies the table (success/failure table) to jump to if count rate is above or below the threshold. 

Delay file simply lists on/off delays in ns for each output bit.

Debugging/checking of output pattern can be done via od program to represent it in hexadecimals:
	od -t x1 -w8 filename
	Output format: Line number is in octal. First 48 bits are outbyte[0]-[5]. Within each outbyte the leftmost bit is the most significant, i.e. output is (from left, bit #) 7 6 5 4 3 2 1 0 15 14 13 12 etc...Last two bytes is the clock bit + controlword (defined as short int). Clock bit is the most significant bit. Note that these two bytes, as displayed, are *swapped* as system is little endian, and stores the least significant byte of the short first, while od reads one byte at a time when specifying -t x1, i.e. you get 7 6 5 4 3 2 1 0 CLOCKBIT 14 13 12 11 10 9 8, where numbers are bit numbers of the controlword address. 

	Changing of table_control_byte is not supported (yet). This is the BYTE of the TTL output that goes back into the ttl input.

	table_control array is the bits from the TABLE CONTROL BYTE that needs to be switched on to access that table(channel).

	Hope to include trigger token that can set certain output bytes depending on outcome (e.g. to signal timestamp). Maybe additional comments and some other tweaks.

Authors of this program so far are: 1)Syed 2)Meng Khoon 3)Victor. Author 1 knows everything. Direct all questions there. Author 3 knows nothing. 
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>

#define DEFAULT_DEVICE "/dev/ioboards/pattgen_generic1"
#define DEFAULT_INPUTSOURCE "patternfile"
#define DEFAULT_DELAYFILE "delayfile"
#define FILENAMLEN 500
#define MAXINLEN 500		/* MAX characters per line */
#define patternsize (1<<19) 
#define FASTCLOCK 0x8000 /* 1 */
#define SLOWCLOCK 0x0000 /* 0 */
#define BIT_SIZE 8
#define NUMCOMMANDS 6
#define MAX_BITS 48
#define TABLE_CONTROL_BYTE 0

long int CLOCK=100000000;
int fast_time_step_ns;
int freqmultiplier[4]={1,1,1000,1000000};
int timemultiplier[4]={1000000000,1000000,1000,1};
char trigger_mask_bit=10;
char trigger_chan=0;
char table_control[16]={0,0x08,0x10,0x18,0x20,0x28,0x30,0x38};


typedef struct tableentry {
  char outbyte[6]; /* six data bytes for 48 output lines */
  unsigned short int controlword; /* a 16 bit wide control word. The
				     least significant 15 bit form the
				     address of the next table entry,
				     the most significant bit decides
				     fixes the duration divider for
				     this particular entry. If this bit
				     is set, the duration is 2 clock
				     cycles, otherwise 200 clock cycles.
				     You can use the macros FASTCLOCK and
				     SLOWCLOCK to set this bit.
				  */
} t_e;

struct tableentry *patternbuf; /* pointer to internal table */
struct tableentry *tempbuf;   /* pointer to temporary table */
typedef struct delay {
  char has_delay;
  short int on_delay;
  short int off_delay;
} d;
struct delay *delay_table;
char * commands[]={
  "",  /* 0: do nothing */
  ".", /* terminate */
  "CLOCK",
  "TRIGGERED",
  "SEQUENTIAL",
  "CONTROL",
};

char * clocktype[]={
  "", "SLOW", "FAST"
};

char * units[] = {
  "", "HZ","KHZ", "MHZ", /* these are all frequency units */
  "", "MS", "US", "NS", 
};

char * modestrings[]={
  "", "NEW", "CONT",
  "", "TRIGGER_MASK", "TRIGGER_INPUT","CONTROL_INPUT"
};

void makeupperstring(char *string){
  int i=0;
  while (string[i]) {
    string[i]=toupper(string[i]);
    i++;
  }
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

char *errormessage[]= {
  "No error.",
  "Negative frequency.", /*1 */
  "Cannot parse input file name",
  "Cannot parse output file name",
  "Cannot open input target",
  "Cannot open output target", /*5 */
  "Unknown token",
  "Command not yet implemented",
  "No frequency supplied",
  "Negative frequency ",
  "No trigger clock",		/* 10 */
  "Invalid trigger clock",
  "No channel to use number",
  "No background count rate value",
  "No signal count rate value",
  "No success channel number",	/* 15 */
  "No failure channel number",
  "No trigger time",
  "Wrong/No time units",
  "Bits to switch on out of range",
  "Undetermined new or cont sequence",/* 20 */
  "No seqeunce use time",
  "No channel to end number",
  "Cannot parse delay file name",
  "Cannot open delay list file",
  "Undetermined control word",	/* 25 */
  "No new trigger mask bit",
  "No new trigger chan",
  "No table control channel",
  "No new table control bit",
  "Pattern overflow"		/* 30 */
};

int parse_number(char *string, int *newposition,long long *value){
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

int parse_command(char *cmd){
  int j,i,k,m,newposition=0;
  static long int current_address=0;
  int retval;
  static  int token;
  int old_token;
  long long int rawvalue, final_address=0, local_address=0;
  unsigned long trigger_clock;
  static unsigned short use_chan, end_chan;
  static unsigned char use_chan_bit;
  unsigned count_1, count_2, success_chan, failure_chan;
  unsigned long long int trigger_time_ns, use_time_ns;
  unsigned char  success_chan_bit, failure_chan_bit;
  unsigned short same;
  unsigned int chan_exceed;
  unsigned short trigger_clock_bit;
  unsigned char switch_on[MAX_BITS]={0} ;


  /* check for empty line */
  while (cmd[newposition]==' ' || cmd[newposition]=='\t' || 
	 cmd[newposition]==',' || cmd[newposition]==':') newposition++;
  if (!cmd[newposition]) return 0; /* empty line is ok */
  
  /* convert into uppercase - ugly, modifies string...*/
  makeupperstring(cmd);
  /* find command index */
  old_token=token;
  token=find_token(cmd, &newposition, commands, NUMCOMMANDS);

  if(token==0 && old_token==4)
    token=4;
#ifdef DEBUG
  fprintf(stderr,"old_token %i token number %i\n",old_token,token);
#endif
  switch (token) {
  case 0: /* no token found */
    return -6; /* unknown token */
  case 1: /* terminate script */
      /* flush tempbuf into patternbuf */
#ifdef DEBUG
    fprintf(stderr,"final current_address: %li\n",current_address);
#endif
    for(i=0,m=0;i<current_address;i++){
      
      for(j=1,same=1;j<100 && same==1;j++){ /* Check for consecutive fastclock */
	if(i+j<current_address){
	  for(k=0;k<MAX_BITS/BIT_SIZE;k++){
	    if(tempbuf[i+j].outbyte[k]==tempbuf[i].outbyte[k])
	      same=1;
	    else{
	      same=0;break;	/* Different */
	    }
	  }
	}
	else{
	  same=0;break;	/* Different */
	}
      }
      final_address=(use_chan<<15)+m;
      if(final_address>=patternsize) return -30;
      for(k=0;k<MAX_BITS/BIT_SIZE;k++)
	patternbuf[final_address].outbyte[k] = tempbuf[i].outbyte[k];
      patternbuf[final_address].controlword = (final_address+1) & ((1<<15)-1);
      chan_exceed=(final_address>>15);
      local_address=final_address & ((1<<15)-1);
      if(chan_exceed > use_chan && local_address==0){
	patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
      }
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
      if(j==100 && same==1){
	i+=99;
	patternbuf[final_address].controlword |= SLOWCLOCK;
      }
      else
	patternbuf[final_address].controlword |= FASTCLOCK;
      
      m++;	
    }
    /* End sequence, return to end chan */
    if(final_address>1){
      patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
      patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
      patternbuf[final_address].controlword &= 0x8000;
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
    }
    /* end flush */
    current_address=0;
    free(tempbuf);
    return 1;
  case 2: /* CLOCK */
    if (parse_number(cmd, &newposition, &rawvalue)) return -8;
    retval=find_token(cmd, &newposition, units, 4);
    rawvalue *= freqmultiplier[retval];
    if (rawvalue<0) return -9; /* no negative frequencies */
    CLOCK=(int)rawvalue;
    fast_time_step_ns=2e9/CLOCK;
/*     fprintf(stderr,"Clock set at %li Hz\n", CLOCK); */
    break;
    
  case 3: /* triggered mode */
      /* flush tempbuf into patternbuf */

#ifdef DEBUG
    fprintf(stderr,"final current_address: %li\n",current_address);
#endif
    for(i=0,m=0;i<current_address;i++){
      
      for(j=1,same=1;j<100 && same==1;j++){ /* Check for consecutive fastclock to convert to 1 slowclock */
	if(i+j<current_address){
	  for(k=0;k<MAX_BITS/BIT_SIZE;k++){
	    if(tempbuf[i+j].outbyte[k]==tempbuf[i].outbyte[k])
	      same=1;
	    else{
	      same=0;break;	/* Different */
	    }
	  }
	}
	else{
	  same=0;break;	/* Different */
	}
      }
      final_address=(use_chan<<15)+m;
      if(final_address>patternsize) return -30;
      for(k=0;k<MAX_BITS/BIT_SIZE;k++)
	patternbuf[final_address].outbyte[k] = tempbuf[i].outbyte[k];
      patternbuf[final_address].controlword = (final_address+1) & ((1<<15)-1);
      chan_exceed=(final_address>>15);
      local_address=final_address & ((1<<15)-1);
      if(chan_exceed > use_chan && local_address==0){
	patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
      }
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
      if(j==100 && same==1){
	i+=99;
	patternbuf[final_address].controlword |= SLOWCLOCK;
      }
      else
	patternbuf[final_address].controlword |= FASTCLOCK;
      
      m++;	
    }
    /* End sequence, return to end chan */
    if(final_address>1){
      patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
      patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
      patternbuf[final_address].controlword &= 0x8000;
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
      patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
    }
    /* end flush */
    current_address=0;
    retval=find_token(cmd, &newposition, clocktype, 3);
    
    if (retval==0) return -10;
    else if(retval==1){
      trigger_clock=CLOCK/200;
      trigger_clock_bit=SLOWCLOCK;
    }
    else if(retval==2){
      trigger_clock=CLOCK/2;
      trigger_clock_bit=FASTCLOCK;
    }
    else
      return -11;
    if (parse_number(cmd, &newposition, &rawvalue)) return -12;
    use_chan=(int)rawvalue;
    use_chan_bit=table_control[use_chan];
    if (parse_number(cmd, &newposition, &rawvalue)) return -13;
    count_1=(int)rawvalue;
    
    if (parse_number(cmd, &newposition, &rawvalue)) return -14;
    count_2=(int)rawvalue;
    
    if (parse_number(cmd, &newposition, &rawvalue)) return -15;
    success_chan=(int)rawvalue;
    success_chan_bit=table_control[success_chan];
    if (parse_number(cmd, &newposition, &rawvalue)) return -16;
    failure_chan=(int)rawvalue;
    failure_chan_bit=table_control[failure_chan];
    
    if (parse_number(cmd, &newposition, &rawvalue)) return -17;
    retval=find_token(cmd, &newposition, &units[4], 4);
    if(!retval) return -18;
    rawvalue *= timemultiplier[retval];
    trigger_time_ns=(unsigned int)rawvalue;
#ifdef DEBUG
    fprintf(stderr,"trigger_clock: %i, channel used: %i,\ncount_1: %i, count_2 %i,\n success_chan %i, failure_chan %i, time: %u ns\n", trigger_clock, use_chan, count_1, count_2, success_chan, failure_chan, trigger_time_ns);
#endif
    while(newposition < strlen(cmd)){
      parse_number(cmd, &newposition, &rawvalue);
/*       fprintf(stderr, "new value: %i\n\n", rawvalue ); */

      if(rawvalue>=0 && rawvalue<MAX_BITS)
	switch_on[rawvalue]=1;
      else
	return -19;
      newposition++;
    }

    /* After getting the necessary parameters and exit conditions, we
     calculate where we should go to wait the same amount of time to
     go up or down, we use the following formula. 
     The `center' of the table is determined such that it takes the same
     amount of time to check whether the atom is still in the trap or has left
     the trap. In order to know where the 'center' of the table is we use the
     following formula:
     
     On count rate = C_2; Off count rate = C_1; Time to check = T ~ 20ms;
     Time per step = t = 1/trigger_clock
     Number of lines in table = L
     Number of lines to skip per click = n;
     Line for Yes atom in trap = Y = n
     Line for No atom in trap = N = L - n;
     Line at wait table to jump to = X;
     
     First equation :
     No of steps from 'YES' atom to center = no of expected steps
     X - Y = (C_2 * T) * n - T * trigger_clock;
     Second equation :
     No of steps from center to 'NO' atom = no of expected steps
     N -X = T * trigger_clock - (C_0 * T) * n;
     
     Solving for n:
     n = L / ((C_2-C_1)*T + 2);
     
     Then X is:
     X = L*(C2*T+1)/(2 + (C_2-C_1)*T) - T*trigger_clock

     Of course this will give solutions 0<X < L for some reasonable
     value of C_0,1 , T and trigger_clock. L is chosen to be 28000 because of
     legacy and also because we can use the extra lines to do in table
     wait or throw atom. Max available time is ~((32000-28000)/trigger_clock)
  */
#define L 28000
    unsigned long n = L/((count_2-count_1)*trigger_time_ns/1e9 + 2);
    unsigned long X = n*(count_2*trigger_time_ns/1e9 +1) - trigger_clock*trigger_time_ns/1e9;
#ifdef DEBUG
    fprintf(stderr,"%lu %lu \n",X,n);
#endif
    /*Check if solution of X makes sense. If not, complain and exit*/
    if(X<=0 || X>=L){
		fprintf(stderr,"Fatal error in setting up trigger! X=%lu, n=%lu, L=%d\n",X,n,L);
		fprintf(stderr,"Adjust trigger parameters for trigger table %d!\n",use_chan);
		exit(1);
	}

    /* Now we create the actual pattern. First line of the pattern
       will be reserved to point into the line X that we want to
       begin from. */
    for(j=0; j<=L; j++){	/* Counting downwards part */
      i=(use_chan<<15)+j; 	/* Actual address = j+offset */

      patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= use_chan_bit; 
      patternbuf[i].outbyte[trigger_mask_bit/8] |= (1<<trigger_mask_bit%8);
      if(j==0){
	patternbuf[i].controlword = X;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==1){
	patternbuf[i].controlword = 0x0000;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= success_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==2){
	patternbuf[i].controlword = 0x0001;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= success_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j<n+4){ /* n+4 because first 3 lines used for other stuff */
	patternbuf[i].controlword = 0x0002;
      }
      else if(j<(L-2)-n){
	patternbuf[i].controlword = (i+1) & ((1<<15)-1);
      }
      else if(j<L-1){
	patternbuf[i].controlword = L-1;
      }
      else if(j==L-1){
	patternbuf[i].controlword = L;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= failure_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==L){
	patternbuf[i].controlword = 0x0000;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= failure_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      patternbuf[i].controlword |= trigger_clock_bit;
      for (k=0;k<MAX_BITS;k++)
	if (switch_on[k])
	  patternbuf[i].outbyte[k/8] |= (1<<k%8) ;
    }

    for(j=0;j<=L;j++){		/* Counting upwards part */
      i=((use_chan+(1<<trigger_chan))<<15)+j;

      patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= use_chan_bit; 
      patternbuf[i].outbyte[trigger_mask_bit/8] |= (1<<trigger_mask_bit%8);
      if(j==0){
	patternbuf[i].controlword = X;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==1){
	patternbuf[i].controlword = 0x0000;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= success_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==2){
	patternbuf[i].controlword = 0x0001;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= success_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j<n+4){/* n+4 because first 3 lines used for other stuff */
	patternbuf[i].controlword = 0x0002;
      }
      else if(j<(L-1)-n){
	patternbuf[i].controlword = (i-n+1) & ((1<<15)-1);
      }
      else if(j<L-1){
	patternbuf[i].controlword = L-1;
      }
      else if(j==L-1){
	patternbuf[i].controlword = L;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= failure_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      else if(j==L){
	patternbuf[i].controlword = 0x0000;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] ^= use_chan_bit;
	patternbuf[i].outbyte[TABLE_CONTROL_BYTE] |= failure_chan_bit;
	patternbuf[i].outbyte[trigger_mask_bit/8] ^= (1<<trigger_mask_bit%8);
      }
      patternbuf[i].controlword |= trigger_clock_bit;
      for (k=0;k<MAX_BITS;k++)
	if (switch_on[k])
	  patternbuf[i].outbyte[k/8] |= (1<<k%8) ;
    }
    break;

  case 4: /* sequential command */
      
    /* get mode */
    retval=find_token(cmd, &newposition, modestrings, 3);
#ifdef DEBUG
    fprintf(stderr,"return value: %i\n",retval);
#endif

    if (retval==1){		/* Use a new channel */

      /* flush tempbuf into patternbuf */
      for(i=0,m=0;i<current_address;i++){
	
	for(j=1,same=1;j<100 && same==1;j++){ /* Check for consecutive fastclock */
	  if(i+j<current_address){
	    for(k=0;k<MAX_BITS/BIT_SIZE;k++){
	      if(tempbuf[i+j].outbyte[k]==tempbuf[i].outbyte[k])
		same=1;
	      else{
		same=0;break;	/* Different */
	      }
	    }
	  }
	  else{
	    same=0;break;	/* Different */
	  }
	}
	final_address=(use_chan<<15)+m;
	if(final_address>patternsize) return -30;
	for(k=0;k<MAX_BITS/BIT_SIZE;k++)
	  patternbuf[final_address].outbyte[k] = tempbuf[i].outbyte[k];
	patternbuf[final_address].controlword = (final_address+1) & ((1<<15)-1);
	chan_exceed=(final_address>>15);
	local_address=final_address & ((1<<15)-1);
	if(chan_exceed > use_chan && local_address==0){
	  patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	  patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed-1];
	  patternbuf[final_address-2].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
	  patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
	}
	patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[chan_exceed];
 	if(j==100 && same==1){
	  i+=99;
	  patternbuf[final_address].controlword |= SLOWCLOCK;
	}
	else
	  patternbuf[final_address].controlword |= FASTCLOCK;

	m++;	
      }
      /* End sequence, return to end chan */
      if(final_address>1){
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
	patternbuf[final_address-1].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
	patternbuf[final_address].controlword &= 0x8000;
	patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] ^= table_control[chan_exceed];
	patternbuf[final_address].outbyte[TABLE_CONTROL_BYTE] |= table_control[end_chan];
      }
      current_address=0;
      free(tempbuf);
      /* end flush, get new buffer */
      if (parse_number(cmd, &newposition, &rawvalue)) return -12;
      use_chan=(int)rawvalue;
      if (parse_number(cmd, &newposition, &rawvalue)) return -22;
      end_chan=(int)rawvalue;
      tempbuf=(struct tableentry*) calloc(patternsize*100,
					  sizeof(struct tableentry));

    }
    else if(retval==2 || retval==0){ /* Continue sequence */
/*       current_address+=1; */
    }
    else
      return -20;    

    if (parse_number(cmd, &newposition, &rawvalue)) return -21;
    retval=find_token(cmd, &newposition, &units[4], 4);
    if(!retval) return -18;
#ifdef DEBUG
    fprintf(stderr,"return value: %i\n",retval);
#endif
    rawvalue *= timemultiplier[retval];
    use_time_ns=(unsigned long long int)rawvalue;

    while(newposition < strlen(cmd)){
      parse_number(cmd, &newposition, &rawvalue);
/*       fprintf(stderr, "new value: %i\n\n", rawvalue ); */
      if(rawvalue>=0 && rawvalue<MAX_BITS)
	switch_on[rawvalue]=1;
      else
	return -19;
      newposition++;
    }
/*     fprintf(stderr,"usetime_ns= %lli\n",use_time_ns); */
    for(j=0;j<use_time_ns/fast_time_step_ns;j++){
      for (k=0;k<MAX_BITS;k++){
	if (switch_on[k]){
	  tempbuf[current_address].outbyte[k/8] |= (1<<k%8);
	  tempbuf[current_address].controlword = (current_address+1) & ((1<<15)-1);
	  if(delay_table[k].has_delay){
	    if(j<((delay_table[k].on_delay)/fast_time_step_ns)){
/* 	      fprintf(stderr,"true\n"); */
	      if(current_address-delay_table[k].on_delay/fast_time_step_ns>0)
		tempbuf[current_address-delay_table[k].on_delay/fast_time_step_ns].outbyte[k/8] |= (1<<k%8);
	    }
/* 	    fprintf(stderr,"k=%i\tj=%i\t%i\n",k,j,(((long long int)use_time_ns - delay_table[k].off_delay)/fast_time_step_ns)); */
	    if(j>=(((long long int)use_time_ns - delay_table[k].off_delay)/fast_time_step_ns) ){
/* 	      fprintf(stderr,"j= %i",j); */
	      tempbuf[current_address].outbyte[k/8] ^= (1<<k%8);
	    }
	    else if( (((long long int)use_time_ns - delay_table[k].off_delay)/fast_time_step_ns < 0) &&
		     (current_address-delay_table[k].off_delay/fast_time_step_ns>0)){
	      tempbuf[current_address-delay_table[k].off_delay/fast_time_step_ns].outbyte[k/8] ^= (1<<k%8);
	    }
	    /* compensate delay here */
	  }
	}
      }
      current_address++;
    }

    break;

  case 5: /* Control */
    retval=find_token(cmd, &newposition, &modestrings[3], 4);
#ifdef DEBUG
    fprintf(stderr,"return value: %i\n",retval);
#endif

    if (retval==1){		/* change trigger mask */
      if (parse_number(cmd, &newposition, &rawvalue)) return -26;
      trigger_mask_bit=(char)rawvalue;
    }
    else if (retval==2){       	/* change trigger input channel */
      if (parse_number(cmd, &newposition, &rawvalue)) return -27;
      trigger_chan=(char)rawvalue;
/*       fprintf(stderr,"cmd : %s\ntable control%i: %i\n",cmd, retval ,rawvalue); */
    }
    else if (retval==3){	/* change table control bits*/
      m=sscanf(cmd, "CONTROL CONTROL_INPUT %i %llx", &retval,&rawvalue);
      if(m==0) return -28;
      else if(m==1) return -29;
      else
	table_control[retval]=(char)rawvalue;
/*       fprintf(stderr,"cmd : %s\ntable control%i: %i\n",cmd, retval ,rawvalue); */
    }
    else
      return -20;    

    break;
  default:
    return -11; /* command not yet implemented */
  }

    
    return 0; /* we were able to process that command */
}


int emsg(int a){
  fprintf(stderr, "%s\n",errormessage[a]);
  return a;
}

int main(int argc, char * argv[]) {
  int opt; /* for parsing options */
  int idx,ir,cmo;
  int blank;
  FILE* inhandle, *inhandle2, *outhandle; 
;

  char outfilename[FILENAMLEN] = DEFAULT_DEVICE;
  char infilename[FILENAMLEN] = DEFAULT_INPUTSOURCE;
  char delayfile[FILENAMLEN] = DEFAULT_DELAYFILE;
  char cmd[MAXINLEN+1],tmp;
  int bitnumber, n1,n2;
  int export_entries;

  while ((opt=getopt(argc, argv, "d:i:o:h")) != EOF) {
    switch (opt) {
    case 'i': /* parse input device */
      if (sscanf(optarg,"%99s",infilename)!=1 ) return -emsg(2);
      outfilename[FILENAMLEN-1]=0; /* close string */
      break;
    case 'o': /* enter output file name */
      if (sscanf(optarg,"%99s",outfilename)!=1 ) return -emsg(3);
      outfilename[FILENAMLEN-1]=0; /* close string */
      break;
    case 'd': /* enter delay list file name */
      if (sscanf(optarg,"%99s",delayfile)!=1 ) return -emsg(23);
      outfilename[FILENAMLEN-1]=0; /* close string */
      break;
    case 'h': /* Print out help file  */
      printf("Generate lookup table for pattern generator.\n");
      printf("Usage: %s [OPTIONS] \n\n",argv[0]);
      printf("\t-i\t\tInput sequence file. Default=%s\n",infilename);
      printf("\t-o\t\tOutput pattern file. Default=%s\n",outfilename);
      printf("\t-d\t\tChannel delays file. Default=%s\n",delayfile);
      printf("\nCurrent implemented commands are:\n\n");
      printf("To change the used clock frequency.\nCLOCK frequency [units]\t Example: clock 100 MHz\n\n");
      printf("To change the used output-input feedback bits. Output bits must be from byte number 0, ie bits 0->7 only.\nCONTROL CONTROL_INPUT table_channel output_bit_in_hex(0x00->0xff)\t Example: control control_input 4 0x20\n\n");
      printf("To change the trigger mask which is an output bit that goes to a coincidence card with the detector clicks.\nCONTROL TRIGGER_MASK output_bit(0-47)\t Example: control trigger_mask 10\n\n");
      printf("To change the trigger input channel from the TTL'ed output of the coincidence card(masked trigger).\nCONTROL TRIGGER_INPUT input_bit(0-3)\t Example: control trigger_input 0\n\n");
      printf("To create a new sequential list, starting beginnig from use_table and ends in end_table after the sequence is completed.\nSEQEUNTIAL NEW use_table end_table time [bits to turn on(0-47)]\n Example: sequential new 2 4 100 us 8 9 10\n Example2: sequential new 0 0 200us 8\n\n");
      printf("To create a subsequent steps in the made sequential list.\n[SEQEUNTIAL] [CONT] time [bits to turn on(0-47)]\n Example: sequential cont 100 us 7 11 12\n Example2: 200us 6\n\n");
      printf("To create a triggered condition from an external input.\nTRIGGERED clock_type(FAST,SLOW) table_to_use low_count_rate_per_second high_count_rate_per_second if_success_goto_table if_failure_goto_table time_to_trigger [units] [bits to turn on(0-47)]\n Example: triggered slow 0 200 5000 2 0 20 ms 8 9 10\n Example2: triggered slow 4 200 5000 2 0 20 ms 8 9 10\n\n");
      printf("Caveats.\n1) User has to ensure that the trigger pulse is about 98%% of the time step of the trigger_clock_type.\n");
      printf("2) User has to ensure that no sequence/trigger overlap each other.\n");
      return 0;
      break;
    case '?':
      printf("Error! Usage: %s [-i INPUTFILE] [-o OUTPUT] [-d DELAYFILE] [-h] (use option h for help)\n",argv[0]); 
      exit(1);
    }

  }
  
  inhandle = fopen(infilename,"r");
  if (!inhandle) return -emsg(4);

  outhandle=stdout;
  if (strcmp(outfilename,"-")) {
    outhandle = fopen(outfilename,"w+");
    if (!outhandle) return -emsg(5);
  }
  inhandle2 = fopen(delayfile,"r");
  if (!inhandle2) return -emsg(24);
  
  patternbuf=(struct tableentry *) calloc( patternsize,  /* number of entries */
					   sizeof(struct tableentry) /* size of one structure */
					   );
  tempbuf=(struct tableentry*) calloc(patternsize*100,
				      sizeof(struct tableentry)
				      );
  delay_table=(struct delay*) calloc( MAX_BITS,  
				      sizeof(struct delay)
				      );
  /* Read delay file */
 do{
    if(fgets(cmd, MAXINLEN, inhandle2) != NULL)
      blank=sscanf(cmd, "%i %i %i", &bitnumber,&n1,&n2);
    else blank=0;
/*     fprintf(stderr, "blank = %i,%i %i %i\n", blank, bitnumber,n1,n2);  */
    delay_table[bitnumber].has_delay=1;
    delay_table[bitnumber].on_delay=n1;
    delay_table[bitnumber].off_delay=n2;
  }while(blank);
      
/*   for(idx=0;idx<MAX_BITS;idx++) */
/*     fprintf(stderr,"%i,%i,%i,%i\n",idx, */
/* 	    delay_table[idx].has_delay, */
/* 	    delay_table[idx].on_delay, */
/* 	    delay_table[idx].off_delay); */
  do {
    /* read in one line, waiting for newline or semicolon. Not nice
       but works... */
    idx=0;
    while ((ir=fread(&cmd[idx],1,1,inhandle))==1 && idx<MAXINLEN) {
      if (cmd[idx]=='#') { 	/* Ignore comments till end of line*/
	idx++;
	while ((ir=fread(&tmp,1,1,inhandle))==1 && idx<MAXINLEN){
	  if (tmp=='\n'){ 
/* 	    fprintf(stderr,"broken\n"); */
	    idx=-1; 
	    break;
	  }
	  idx++;
	}
      }
      else if (cmd[idx]=='\n' || cmd[idx]==';'){
	break;
      }
      idx++;
    };
    cmd[idx]='\0';
/*     fprintf(stderr,"%s",cmd); */

    /* call command parser */
    cmo=parse_command(cmd);
#ifdef DEBUG
    printf("parser return: %d\n",cmo);
#endif
    for(idx=0;idx<MAXINLEN;idx++)
      cmd[idx]=0;
  } while (!cmo);

  if (cmo<0) 
    return -emsg(-cmo);
      
  
  export_entries = patternsize;
#ifdef DEBUG2
  for(i=0; i<patternsize; i++)
    if(i%2)
      patternbuf[i].outbyte[0] |= 0x40;
#endif
  fwrite(patternbuf,sizeof(struct tableentry),export_entries,outhandle);
  if (strcmp(outfilename, "-"))
    fclose(outhandle);

  return 0;
}

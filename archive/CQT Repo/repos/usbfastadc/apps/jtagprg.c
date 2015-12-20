/* This program is supposed to interpret the SVF command files and generate
   a bit sequence for the JTAG chain. Optional argument:

   -d devicefilename   Uses the specified device instead of
                       /dev/ioboards/usbprog0

   Takes a SVF file from stdin and generates bit patterns. Comments and
   readback test failures are sent to stderr.

   first code      1.11.2010chk
   works with lattice svf file      4.11.2010chk
   fixed multiline arguments        24.7.2012chk
   added option for different device file 28.11.2012chk

   ToDo: Head/tail check needs to be implemented.

*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <math.h>

#include "usbprog_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "Error returned from ioctl call",
  "Error in initializing JTAG call",
  "Frequency spec too low",
  "Not a stationary state", /* 5 */
  "Header/trailer too long",
  "Bitstream too long",
  "Error shifting data stream",
  "Mismatch in data matching",
  "Error in bit chain comparison", /* 10 */
  "Wrong mode indx in shift call", 
  "Timing value negative",
  "Unknown command",
  "Command not yet implemented",
  "Missing length argument for header", /* 15 */
  "Cannot parse integer argument",
  "Integer argument out of range",
  "Unexpected token",
  "Error parsing bit chain",
  "End state argument expexted", /* 20 */
  "Illegal state argument", 
  "Missing 'HZ' indicator",
  "Cannot parse float argument",
  "Non-positive frequency argument",
  "Arguments botched up",  /* 25 */
  "Missing state argument",
  "Path selection not implemented",
  "Wrong argument number",
  "Too many arguments in statement",
  "Single argument too long", /* 30 */
  "Statement ended with incomplete argument",
  "Cannot parse device file name",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbfastadc0"

/* ---------------------------------------------------------------------*/
/* Some structures handling bit chains. Bit chains are stored in a way
   that allows simple transmission to the programmer
 */
#define MAXCHAINBYTES 1000
typedef struct bit_chain {
  int length; 
  char content[MAXCHAINBYTES];
} bitchain;

/* main bit chains including expected patterns and masks */
struct bit_chain d_tdi, d_tdo, d_mask, d_smask; /* data pattern */
struct bit_chain i_tdi, i_tdo, i_mask, i_smask; /* instruction pattern */

/* header/trailer bit chains. */
struct bit_chain header_dr, header_ir; /* tdi data, contains main length */
struct bit_chain trailer_dr, trailer_ir;
struct bit_chain h_dr_tdo, h_ir_tdo, t_dr_tdo, t_ir_tdo; /* tdo data */
struct bit_chain h_dr_ma, h_ir_ma, t_dr_ma, t_ir_ma; /* mask data */
struct bit_chain h_dr_sma, h_ir_sma, t_dr_sma, t_ir_sma; /* smask data */

/* some bit chain handling primitives */
/* concatenate:: target|source -> target */
int append_bit_chain(struct bit_chain *target, struct bit_chain *source) {
  int sourceshift, sshift2; /* how many bits to shift source to match target */
  int i, j; /* source / target index */
  int k = target->length; /* counting variable */
  int u;

  //printf(" target content: "); for (i=0;i<10;i++) printf("%02x ",target->content[i]);
  //printf(" src content: "); for (i=0;i<10;i++) printf("%02x ", source->content[i]);printf("\n");
   if ((k + source->length + 7)/8 >  MAXCHAINBYTES) return -1;
  sourceshift = k % 8; sshift2 = 8- sourceshift;
  j = k/8; /* stuff to be added here */
  target->content[j] &= (1<<sourceshift)-1; /* clear spurious bits */
  i=0;
  //printf("k: %d, j: %d\n",k,j);
  k=source->length;
  while(k>0) {
    //printf(" in loop: k=%d\n",k);
    u=source->content[i];
    target->content[j] |= (u<<sourceshift) & 0xff;
    i++; j++; 
    //printf(" in loop: k=%d, i=%d, j=%d, u=%02x, shift2=%d\n",k,i,j,u,sshift2);

    if (j<MAXCHAINBYTES) target->content[j] = ((u&0xff)>>sshift2);
    k -= 8;
  }
  //printf("old target length/ src len: %d %d\n",target->length, source->length);

  target->length += source->length;
  //printf("new target length: %d\n",target->length);
  return 0;
}
/* extract a segment of a bit chain */
int sub_bit_chain(struct bit_chain *stream, int from, int length){
  int s, t;
  int shift, shift2;
  if (stream == NULL) return -1; 
  if (length<0 || from<0 || from+length>=stream->length) 
    return -1; /* illegal range */

  shift= from % 8; shift2 = 8-shift;
  s = from / 8; /* byte index for start (source) */
  for (t=0; t<(length+7)/8; t++) {
    stream->content[t] = stream->content[s]>>shift;
    s++;
    stream->content[t] |= (stream->content[s]<<shift2) & 0xff;
  }
  if (length % 8) stream->content[t-1] &= (1<<(length % 8))-1;

  return 0;
}

/* comparison; result: -1: error, 0: same, 1: difference */
/* the mask (if provided) defines which bits are checked  */
int compare_bit_chains_masked(struct bit_chain *a, struct bit_chain *b,
			      struct bit_chain *mask) {
  int i;
  char c=0;
  struct bit_chain *m = mask;
  if (a == NULL ||  b == NULL) return -1;
  if (a->length != b->length) return -1; /* error condition */
  if (a->length != m->length) m=NULL; /* no masking in this case */
  i=a->length /8; /* last byte index */
  c=a->content[i] ^ b->content[i];
  c &= ((1<<(a->length % 8))-1); 
  if (m) { /* We need to do masking */
    c &= m->content[i];
    while (i>0) {
      i--;
      c |= (a->content[i] ^ b->content[i]) & m->content[i];
    }
  } else { /* no mask */
    while (i>0) {
      i--;
      c |= (a->content[i] ^ b->content[i]);
    }
  }
  return c?1:0;
}

/*----------------------------------------------------------------------*/
/* Some code snippets that implement the SVF file primitives defined by the
   programmer. The handle argument points to the device file. 
   They return zero on success or an error code > 0 , and write log info into
   stdout for now */
/* not sure what it should do yet; hatdware initialization */
int JTAG_init(int handle) {
  int retval;
  retval = ioctl(handle,JTAG_initialize);
  if (retval) { /* test if echo is correct */
    return 3; /* wrong response */
  }
  return 0;
}

#define CLOCK_PERIODE_0 8.0E-6 /* clock periode in sec with delay = 0;
				   for runtest loop (shortest) */
#define CLOCK_PERIODE_1 1.67E-6 /* clock periode in sec for delay increment */
int delayvalue = 0;
/* this function translates the maximum freq request into a delay request */
int Set_Frequency(int handle, double freq) {
  int val;
  if (freq <= 0.0) return 4; /* too low freq */
  val = ceil((1.0/freq-CLOCK_PERIODE_0)/CLOCK_PERIODE_1);
  if (val>255) return 4; /* too low freq */
  if (val<0) val=0; /* avoid trouble */

  // printf(" delay value is programmed to: %d\n",val);
  if (ioctl(handle, Set_Delay, val)) { /* test if echo is correct */
    return 2; /* wrong response */
  }
  delayvalue=val;
  return 0;
}

/* sets end state of data/IR transfer. State is one out of four stable states */
int Set_ENDDR(int handle, int state) {
  if (state <0 || state >3) return 5; /* not stationary state */
  if (ioctl(handle, JTAG_ENDDR, state)) return 2;
  return 0;
}
int Set_ENDIR(int handle, int state) {
  if (state <0 || state >3) return 5; /* not stationary state */
  if (ioctl(handle, JTAG_ENDIR, state)) return 2;
  return 0;
}
int Go_State(int handle, int state) {
  if (state <0 || state >3) return 5; /* not stationary state */
  if (ioctl(handle, JTAG_runstate, state)) return 2;
  return 0;
}

/* code to convert a bit chain into a text */
char hexencode[16]="0123456789abcdef";
void chain2text(struct bit_chain *c, char *text) {
  int i=0, j=(c->length+3)/4;
  text[j+2]=0;/* terminate text */
  text[j+1]=')'; text[0]='(';
  for (i=0; i<c->length; i+=4, j--) {
    text[j]=hexencode[(c->content[i/8]>>(i&4?4:0))&0xf];
  }
}
/* send data stream; masking partially implemented. Parameters:
   mode: 0 for data, 1 for Instruction 
   tdi: input stream
   tdo: output pattern to be expexted. If NULL, no test
   mask: mask for output pattern. if NULL, mask is ignored */
int shift_data_IR(int handle, int mode, 
		  struct bit_chain *tdi, struct bit_chain *tdo,
		  struct bit_chain *mask) {
  int retval;
  struct bit_chain *header, *trailer;
  int command;
  struct bit_chain message;
  //int i;
  char rettext[256]; /* contains return text in case of mismatch */

  /* setting of data/instruction mode differences */
  switch (mode) {
  case 0: /* data */
    header=&header_dr; trailer = &trailer_dr; command = JTAG_scandata;
    break;
  case 1: /* data */
    header=&header_ir; trailer = &trailer_ir; command = JTAG_scanIR;
    break;
  default:
    return 11; /* wrong mode */
  }

  /* make bit string */
  message.length=0;
  if (header->length) append_bit_chain(&message, header);
  if (tdi->length) {
    retval=append_bit_chain(&message, tdi);
      if (retval) return 7;
  }
  if (trailer->length) {
    retval=append_bit_chain(&message, trailer);
    if (retval) return 7;
  }

  //printf("data stream length: %d content:\n",message.length);
  //for (i=0; i<16; i++) printf("%02x ", message.content[i]&0xff);
  //printf("\n");
  /* send stream */
  retval=ioctl(handle, command, &message);
  printf("point 2: retval= %d, err: %d\n",retval, errno);
  if (retval) return 8;

  /* ToDo: Header test */
  /* ToDo: Trailer test */

  if (tdo) { /* we need to do comparison */
    //printf("data returned: %d content:\n",message.length);
    // for (i=0; i<16; i++) printf("%02x ", message.content[i]&0xff);
    //printf("\n");

    /* strip margins */
    sub_bit_chain(&message, header->length, tdi->length); 
    /* compare result */
    retval=compare_bit_chains_masked(&message, tdo, mask);
    if (retval<0) return 10; /* error */
    if (retval>0) {
      chain2text(&message, rettext);
      printf(" mismatch return data: length: %d, content: %s\n",
	     message.length, rettext);
      return 9; /* Mismatch detected */    
    }
  }
  return 0;
}

#define MAX_CLOCKCYCLES ((1<<15)-1)
/* runtest command implement. clocks and timing are minimal values */
int runtest(int handle, int state, int clocks, double mintime) {
  int minclock, timclk, this_t;
  double period;
  if (state <0 || state >3) return 5; /* not stationary state */
  if (clocks<0 || mintime<0.0) return 12;
  minclock=clocks;
  /* integrate timing */
  period = CLOCK_PERIODE_0+ CLOCK_PERIODE_1 * delayvalue;
  timclk = ceil(mintime / period);
  if (timclk>minclock) minclock=timclk; /* use the larger of both */

  /* Run a number of clock cycles */
  do {
    this_t = minclock>MAX_CLOCKCYCLES?MAX_CLOCKCYCLES:minclock;
    if (ioctl(handle, JTAG_runstate, state | (this_t<<8))) return 2;
    minclock -= this_t;
  } while (minclock>0);
  return 0;
}
/* trst code. state is 0 ot 1 */
int set_trst(int handle, int state) {
  if (ioctl(handle, JTAG_setTRST, state)) return 2;
  return 0;
}

/*-------------------------------------------------------------------------*/
/* SVF parser code */
#define ARGUMENTLENGTH 512 /* max number of argument entries */
/* argument handling for parser */
#define MAXARGUMENTS 11
char *argument[MAXARGUMENTS]; /* holds pointers to arguments */
#define NUMCOMMAND 28
char *commandname[] ={
  "HDR", /* 0 */
  "HIR",
  "ENDDR",
  "ENDIR",
  "FREQUENCY",
  "RUNTEST", /* 5 */
  "SDR",
  "SIR",
  "STATE",
  "TDR",
  "TIR", /* 10 */
  "TRST",
  "TDI",
  "TDO",
  "MASK",
  "SMASK", /* 15 */
  "RESET",
  "IDLE",
  "DRPAUSE",
  "IRPAUSE",
  "HZ", /* 20 */
  "TCK",
  "SCK",
  "SEC",
  "MAXIMUM",
  "ENDSTATE", /* 25 */
  "ON",
  "OFF",
  "ABSENT",
};
/* convert keyword into number */
int get_keyword(char *x) {
  int i;
  for (i=0; i<NUMCOMMAND && strncmp(x,commandname[i],256); i++);
  return i;
}
/* init hex text decoder: this is just an array for speed reasons. */
char hexdecode[256];
void init_hexdecode(){
  int i=255; do {hexdecode[i]=-1;i--;} while (i>0);
  for (i=0; i<10; i++) hexdecode['0'+i]=i;
  for (i=0; i<6; i++)  hexdecode['A'+i]=hexdecode['a'+i]=i+10;
}
/* parsing a hex text into a bitchain. return value is >=0 on success */
int parse_bitchain(char *in, struct bit_chain *out) {
  int j, len;
  char c;
  len=strlen(in);
  if (in[0]!='(' || in[len-1]!=')') return -1; /* wrong format */
  for (j=0; j<len-2; j++) {
    c=hexdecode[(unsigned int)in[len-2-j]];
    if (c<0) return -1; // wrong char
    if (j & 1) { //odd bits
      out->content[j/2] |= (c<<4);
    } else {
      out->content[j/2] = c;
    }
  }
  /* fill rest up w 0 */
  if (j & 1) j++;
  for (j/=2; j< MAXCHAINBYTES; j++) out->content[j]=0;
  return 0;
}

/* main interpreter for a statement. Gets passed all the arguments in global
   string variables, which are trimed for whitespace and termination chars.
   The fucntion parameter args holds how many text items are stored in the
   argument array. */
int parse_statement(int handle, int args){
  int i,j,n;
  int retval;
  struct bit_chain *a=NULL, *atdo=NULL, *am=NULL, *asma=NULL;
  double x,y; /* for float args */
  int state1, state2;
  int cycles;
  
  printf("Parsing >%s< with %d arguments.\n",argument[0],args-1);
  i=get_keyword(argument[0]);
  switch (i) {
  case 0: /* HDR */
  case 1: /* HIR */
  case 6: /* SDR */
  case 7: /* SIR */
  case 9: /* TDR */
  case 10: /* TIR */
    if (args<2) return 15; /* missing length arg */
    /* select command-specific target chains */
    switch (i) {
    case 0: a = &header_dr; atdo=&h_dr_tdo; am=&h_dr_ma; asma=&h_dr_sma; break;
    case 1: a = &header_ir; atdo=&h_ir_tdo; am=&h_ir_ma; asma=&h_ir_sma; break;
    case 6: a = &d_tdi; atdo=&d_tdo; am=&d_mask; asma=&d_smask; break;
    case 7: a = &i_tdi; atdo=&i_tdo; am=&i_mask; asma=&i_smask; break;
    case 9:  a = &trailer_dr; atdo=&t_dr_tdo; 
      am=&t_dr_ma; asma=&t_dr_sma; break;
    case 10: a = &trailer_ir; atdo=&t_ir_tdo; 
      am=&t_ir_ma; asma=&t_ir_sma; break;
    }
    /* parse bit number argument */
    if (1!=sscanf(argument[1],"%d",&n)) return 16; /* no number */
    if (n<0) return 17; /* out of range */
    a->length=n;
    
    /* retrieve all optional bit chain arguments */
    atdo->length=0;  /* by default, don't test */
    for (j=2; j<args; j+=2) {
      switch (get_keyword(argument[j])) {
      case 12: //TDI
	if (parse_bitchain(argument[j+1],a)<0) return 19;
	break; 
      case 13: //TDO
	if (parse_bitchain(argument[j+1],atdo)<0) return 19;
	atdo->length=n;
	break;
      case 14: //MASK
	if (parse_bitchain(argument[j+1],am)<0) return 19;
	am->length=n;
	break;
      case 15: //SMASK
	if (parse_bitchain(argument[j+1],asma)<0) return 19;
	asma->length=n;
	break;
      default:
	return 18; // unexpected token
      }
    }
    /* only get into action for shift commands */
    if (i==6 || i==7) {
      retval=shift_data_IR(handle,
			   i-6, /* mode */
			   a,  /* in data */
			   atdo->length?atdo:NULL, /* TDO data */
			   am /* mask data */);
      return retval;
    }
    break;
  case 2: /* ENDDR */
  case 3: /* ENDIR */
    if (args!=2) return 20; /* missing state arg */
    /* try parsing state */
    j=get_keyword(argument[1]);
    if (j<16 || j>19) return 21; /* illegal end state */
    if (i==2) return Set_ENDDR(handle, j-16);
    return Set_ENDIR(handle, j-16);
    break;
  case 4: /* FREQUENCY */
    switch (args) {
    case 1: /* no argument */
      return Set_Frequency(handle, 1E008); /* max freq */
    case 3: /* freq argument */
      if (get_keyword(argument[2])!=20) return 22; /* missing HZ */
      if (1!=sscanf(argument[1],"%lf",&x)) return 23;
      if (x<=0.0) return 24;
      // printf("Frequency command: %lf\n",x);
      return Set_Frequency(handle, x); /* max freq */
    default:
      return 25;
    }
    break;
  case 5: /* runtest */
    state2=-1;state1=-1;
    /* check for state argument */
    n=get_keyword(argument[1]);
    if (n<16 || n>19) { /* no endstate */
      j=1; /* next argument */
    } else {
      state1=n-16; j=2;
    }
    n=get_keyword(argument[j+1]);
    /* check clock cycle arg */
    cycles=0;
    if (n==21 || n==22) { /* we have TCK/SCK arg */
      if (1!= sscanf(argument[j],"%d",&cycles)) return 16;
      if (cycles<0) return 17;
      j+=2;
    }
    x=0.0;y=0.0;
    while (j<args) { /* we have more args */
      if (args-j<2) return 25; /* arg botchup */
      if (get_keyword(argument[j+1])==23 ) { // "SEC" keyword
	if (1!=sscanf(argument[j],"%lf",&x)) return 23;
	j+=2; continue;
      }
      if (get_keyword(argument[j])==24) { /* MAXIMUM keyword */
	if (args-j<3) return 25; /* arg botchup */
	if (get_keyword(argument[j+2])!=23) return 25; /* arg botchup */
	if (1!=sscanf(argument[j],"%lf",&y)) return 23;
	j+=3; continue;
      }
      if (get_keyword(argument[j])==25) { /* ENDSTATE keyword */ 
	n=get_keyword(argument[j+1]);
	if (n<16 || n>19)  /* no endstate */
	  return 21; /* illegal */
	state2=n-16; j+=2; continue;
      }
      return 25; /* arg botchup */
    }
    /* we got a legal set of params... no maxtime test */
    retval=runtest(handle, state1, cycles, x); /* this runs */
    if (retval) return retval;
    if (state2>0) retval=Go_State(handle, state2); /* new state */
    return retval;
    break;
  case 8: /* STATE */
    if (args<2) return 26; /* missing path arg */
    if (args>2) return 27; /* no pathselect */
    state1=get_keyword(argument[1]);
    if (state1<16 || state1>19) return 21; /* illegal end state */
    return Go_State(handle, state1-16); /* new state */
    break;
  case 11: /* TRST */
    if (args!=2) return 28; /* wrong no args */
    state1=get_keyword(argument[1]);
    if (state1<26 || state1>28) return 21; /* illegal end state */
    if (state1<28) return set_trst(handle, state1);
    break;
  default:
    return 13;
  }
  return 0;
}

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
  
    int retval=0;
    //  int option, parameter;
    int line_number, i;
    FILE *inhandle = stdin; /* temporary version */
    char this_line[257];
    int parsestatus; /* 0: search statement, >0 in statement */
    int argumentstatus; /* 0: waiting for arg, 1: in arg; 2: open paranthesis */
    char *sp; /* for parsing the line */
    char ch; /* for latest character */
    int opt; /* for parsing options */

    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(32);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       }
    }
    
    handle=open(devicefilename,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }


    /* prepare some global defaults */
    header_dr.length=0; header_ir.length=0;
    trailer_dr.length=0; trailer_ir.length=0;
    for (i=0; i<MAXARGUMENTS;i++) argument[i]=(char *)malloc(ARGUMENTLENGTH);

    init_hexdecode();

    /* initialize JTAG interface */
    retval=JTAG_init(handle);
    if (retval) return -emsg(retval);

    /* input line text parser loop */
    line_number=0;
    parsestatus=0; /* we wait for statement */
    argumentstatus=0; /* outside argument */
    i=0; /* index into running argument */
    do {
      line_number++;
      if (NULL==fgets(this_line, sizeof(this_line), inhandle)) break;
      //printf("line: %d,>%s<\n",line_number,this_line);


      /* going through all characters of the line one by one :( */
      for (sp=this_line; (ch=sp[0]); sp++) { /* assign character in test */
	//printf("     P3: stat: %d, ch: %c \n", argumentstatus, ch);
	if (ch=='!') break; /* this is a comment, ignore rest of line */
	if (ch=='/') 
	  if (sp[1]=='/') break; /* ignore rest of line */
	if ((ch==' ') || (ch=='\r') || (ch== '\n') || (ch== '\t')) { /* whitespace */
	  if (argumentstatus==0) continue; /* this is empty line or EOL */
	  if (argumentstatus==2) continue; /* still in an ongoing argument */
	  /* here, we need to be in parsemode==1, i.e., now we need to
	     terminate the argument */
	  argument[parsestatus][i]=0; /* terminate end of string */
	  //printf("     P1: Argument: %s, stat: %d\n",
	  //	 argument[parsestatus], argumentstatus);

	  parsestatus++; /* switch to next possible argument */
	  if (parsestatus>=MAXARGUMENTS) {
	    fprintf(stderr, "Source file line %d: ",line_number);
	    return -emsg(29);
	  }

	  argumentstatus=0; i=0; /* back to fresh argument read status */

	} else { /* we got a nonwhitespace character */
	  if ( argumentstatus == 0 ) 
	    argumentstatus = 1; /* we now have an argument running */
	  if ( ch=='(' ) argumentstatus = 2; /* we have an open argument */
	  if ( ch==')' ) argumentstatus = 1; /* argument just closed */
   
	  if ( ch==';' ) { /* end of statement. Start interpreter */
	    if (argumentstatus != 1) /* incomplete argument at end of statem */
	      return -emsg(31); 
	    argument[parsestatus][i]=0; /* terminate last argument */
	    //printf("     P2: Argument: %s\n",argument[parsestatus]);

	    parsestatus++;  /* add last argument to counter */
	    argumentstatus=0; i=0; /* go for fresh argument */

	    /* execute interpreter */

	    //fprintf(stderr, "Source file line %d: ",line_number);
	    //  printf(" -- line: %d args: %d\n",line_number, parsestatus);
	    //  for (j=0; j<parsestatus; j++) {
	    //	printf(" -- arg[%d]: %s\n",j, argument[j]); }

	    retval=parse_statement(handle, parsestatus);
	    if (retval) { /* an error occured */
	      return -emsg(retval);
	    } 
	    parsestatus=0; /* go for fresh statement */
	  } else {  /* by dafault, add char to argument */
	      argument[parsestatus][i]=ch; i++;
	      /* do some test if i exceeds argument length */
	      if (i>=ARGUMENTLENGTH) return -emsg(30);
	  }
	}
      } /* end of characters parsing in line loop */
      
    } while (1); /* end of parsing lines loop */
    
    printf("total lines: %d\n",line_number);
    close(handle);
    
    return 0;

}

/* program to read a jedec file, and generate a jtag command set to program a
   MachXO2 chip via the embedded jtag command sets for several FX2 devices.

   Should be expandable to a number of devices, but I thought that before 
   several times.

   Strategy:
    1. Read in the jedec file
    2. Check file consistency
    3. carry out the programming

    usage:
    jedecparse [-f jedecfile]

    options:
    -f jedecfile      take the specified file instead of stdin

   Status:
   First code 7.2.2015christian Kurtsiefer


*/
#include <stdio.h>
#include <unistd.h>
#include <string.h>


#define READBUFSIZE 0x10000 /* read in a single go */
#define EFIELDBYTES 32
#define UFIELDBYTES 32


/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot parse source file name", /* 1 */
  "Cannot open source file",
  "Unknown command letter",
  "Unknown Q parameter identifier",
  "digit 0-9 expected in parameter definition of Q parameter", /* 5 */
  "Security mode inde out of range (0-3)",
  "Default fuse value out of range (0 or 1)",
  "cannot malloc fusefield buffer",
  "illegal repeat definition of fuse field size in QF command",
  "Premature use of link field command L (no length info)", /* 10 */
  "Illegal character in Link address definition",
  "Illegal character in link value definition",
  "expect hex digit character (0-9, a-f, A-F)", 
  "illegal binary digit in E field definition",
  "illegal hex character in U field definition", /* 15 */
  "illegal hex character in transmission checksum",
  "Linkfield checksum mismatch in jedec file",
  "Transmission checksum mismatch in jedec file",
  "Cannot allocate space for E/U fields",
};

int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};
int emsgl(int code, int line) {
    fprintf(stderr,"line %d: %s\n",line, errormessage[code]);
  return code;
};


/* Structure that contains the fusefield and other descriptors */
typedef struct jedecinfo {
    int pinnumber;
    int fusenumber;
    int securitymode;
    int efieldbits;
    int ufieldbits;
    unsigned char *efield;
    unsigned char *ufield;
    unsigned char *fusefield;
} jedec_info;

struct jedecinfo jed; /* holds global jedec info */

/* helper function to convert ascii to value */
int hextoc(char c) {
    char c2=c;
    if ((c2>='0') && (c2<='9')) return c2-'0';
    c2 |= 0x20; 
    if ((c2<'a') || (c2>'f')) return -1; /* in case of error */
    return c2-'a'+10; 
}
int dectoc(char c) {
    char c2=c;
    if ((c2>='0') && (c2<='9')) return c2-'0';
    return -1;  /* in case of error */
}

/* code that generates a jedecinfo structure from a jedec file. Return value
   is 0 on success, or an error indicator (<0) */
int populate_jed_structure(FILE *sourcehandle, struct jedecinfo *js) {
    char readbuffer[READBUFSIZE]; /* read buffer */
    int readbufidx, readbufentries; /* reading index for next character */

    int linenumber; /* this is the line number of the input file for debug */
    int parsemode; /* decide which parsing mode.
		      0: Wait for beginning of file
		      1: Wait for command
		      2: Note mode (ignore until *)
		      3: Q mode (will need a submode)
		      4: G mode (needs a number)
		      5: F mode (default fuse, needs 0 or 1)
		      6: L mode (link field);
		      7: C mode (checksum field)
		      8: E field definition
		      9: U field definition
		      10: Passed end; reading checksum
		   */
    int subparsemode=0; /* for Q mode:  0: no mode yet.
			              'P': Pin number
			              'F': Fuse number
			   for U mode: 0: binary.
			               1: hex
		      */
    int qlength=0, qvalue=0;
    char c;
    unsigned int checksum1, checksum2;
    int fuseindexlength=0;
    int defaultfusevalue=0;
    int fuseindex=0;
    int linkadchars=0;
    int i;
    unsigned char tmp;
    int tchks1o=0, tchks2o=0; /* observed checksums */
    int tchks1c=0, tchks2c=0; /* claimed checksums */

    
    /* initialization of bitfield parameters */
    js->pinnumber = 0;
    js->fusenumber = 0;
    js->securitymode = 0;
    js->fusefield = NULL; /* no fusefield populated */
    
    /* allocation of U and E bit spaces, E/U field parameter initialization */
    js->efield = (unsigned char *)malloc(EFIELDBYTES);
    js->ufield = (unsigned char *)malloc(UFIELDBYTES);
    if ((js->efield==NULL) || (js->ufield==NULL)) return -emsg(19);
    for (i=0; i<EFIELDBYTES; i++) js->efield[i]=0;
    for (i=0; i<UFIELDBYTES; i++) js->ufield[i]=0;
		    
    js->efieldbits=0;
    js->ufieldbits=0;

    /* initialize read buffer, and fill it */
    readbufentries=0; readbufidx=0;
    
    /* input parser loop */
    parsemode=0; checksum1=0; checksum2=0; linenumber=1;

    do {
	readbufentries = fread(readbuffer, sizeof(char), READBUFSIZE,
			       sourcehandle); /* fill buffer */
	if (readbufentries==0) break; /* end of file */
	for (readbufidx=0; readbufidx<readbufentries; readbufidx++) {
	    /* here starts the character parsing */
	    c=readbuffer[readbufidx]; /* get single byte */
	    checksum1 += (unsigned char) c; /* overall checksum */
	    
	    /* ignore whitespace */
	    if (c=='\n') linenumber++; /* just to be helpful for debug */
	    if ((c=='\r') || (c=='\n')) continue;

	    switch (parsemode) {
	    case 0: /* waiting for start */
		if (c==0x02) { /* STX character - begin parsing  */
		    parsemode=1; checksum1=2;
		}
		break;
	    case 1: /* waiting for command */
		switch (c) {
		case 'N': /* Note command starts */
		    parsemode=2;
		    break;
		case '*':/* ignore termination and whitespace*/
		    break;
		case 'Q': /* parameter command */
		    parsemode=3; subparsemode=0;
		    break;
		case 'G': /* security fuse thing */
		    parsemode=4; qvalue=0;
		    break;
		case 'F': /* default fuse value */
		    parsemode=5; qvalue=0;
		    break;
		case 'L': /* Link field address */
		    if (fuseindexlength==0) 
			return -emsgl(10,linenumber); /* no lenght */
		    parsemode=6; linkadchars=fuseindexlength;
		    fuseindex=0;
		    break;
		case 'C': /* checksum test */
		    parsemode=7; qvalue=0;
		    break;
		case 'E': /* E field definition */
		    parsemode=8;
		    break;
		case 'U': /* U field definition */
		    parsemode=9; subparsemode=0;
		    break;
		case 3: /* end of file position */
		    parsemode=10; tchks1o=checksum1 & 0xffff;
		    tchks1c=0;
		    break;
		default: /* unknown command letter */
		    fprintf(stderr, "Received 0x%02x (>%c<); ",c, c);
		    return -emsgl(3, linenumber);
		}
		break;
	    case 2: /* note mode; ignore until star */
		if (c=='*') parsemode=1;
		break;
	    case 3: /* parameter Q mode */
		if (subparsemode==0) { /* determine subparsemode */
		    if (strchr("PF", c)==NULL) { /* wrong para */
			//fprintf(stderr, "Q subcommand %c ;", c); 
			return -emsgl(4, linenumber);
		    }
		    subparsemode = c; qlength=0; qvalue=0;
		} else {
		    if (c=='*') { /* save as value */
			switch (subparsemode) {
			case 'P': js->pinnumber=qvalue;
			    break;
			case 'F': js->fusenumber=qvalue;
			    fuseindexlength=qlength;
			    /* reserve space for fuse field */
			    if (js->fusefield) 
				return -emsgl(9, linenumber); /* double def */
			    js->fusefield = (unsigned char *)
				malloc((js->fusenumber+7)/8);
			    if (!js->fusefield) 
				return -emsgl(8, linenumber);
			    /* fill fuse field with default */
			    tmp=defaultfusevalue?0xff:00;
			    for (i=0; i<(js->fusenumber+7)/8; i++) {
				js->fusefield[i]=tmp;
			    }
			    break;
			}
			parsemode=1;
		    } else {
			i=dectoc(c); if (i<0) return -emsgl(5, linenumber);
			qlength++; qvalue = 10*qvalue + i;
		    }
		}
		break;
	    case 4: /* security mode "G" */
		if (c=='*') { /* save as value */
		    if (qvalue>3) {
			//fprintf(stderr, " G value: %d; ",qvalue);
			return -emsgl(6, linenumber);
		    }
		    js->securitymode=qvalue;
		    parsemode=1;
		} else {
		    i=dectoc(c); if (i<0) return -emsgl(5, linenumber);
		    qlength++; qvalue = 10*qvalue +i;
		}
		break;
	    case 5: /* default fuse value "F" */
		if (c=='*') { /* save as value */
		    if (qvalue>1) {
			//fprintf(stderr, " F value: %d; ",qvalue);
			return -emsgl(7, linenumber);
		    }
		    defaultfusevalue=qvalue;
		    parsemode=1;
		} else {
		    i=dectoc(c); if (i<0) return -emsgl(5, linenumber);
		    qlength++; qvalue = 10*qvalue + i;
		}
		break;
	    case 6: /* link field definition */
		if (linkadchars>0) { /* we need to load address */
		    i=dectoc(c); if (i<0) return -emsgl(11, linenumber);
		    fuseindex = fuseindex*10 + i; linkadchars--;
		} else if (c=='*') {
		    parsemode=1;
		} else {
		    if ((c<'0') || (c>'1')) return -emsgl(12, linenumber);
		    tmp=1<<(fuseindex%8); /* bit value */
		    if (c=='1') {
			js->fusefield[fuseindex/8] |=tmp;
			checksum2 += tmp;
		    } else {
			js->fusefield[fuseindex/8] &= ~tmp;
		    }
		    fuseindex++;
		}
		break;
	    case 7: /* checksum test */
		if (c=='*') {
		    tchks2o=checksum2; 
		    tchks2c=qvalue;
		    parsemode=1;
		} else {
		    i=hextoc(c);
		    if (i<0) return -emsgl(13, linenumber);
		    qvalue = qvalue*16+i;
		}
		break;
	    case 8: /* E field definition */
		if (c=='*') { /* we are done; all bits defined */
		    parsemode=1;
		    break;
		}
		if ((c<'0') || (c>'1')) { /* wrong digit */
		    return -emsgl(14,linenumber);
		}
		if (c=='1') 
		    js->efield[js->efieldbits/8] |= (1<<(js->efieldbits%8));
		js->efieldbits++;
		break;
	    case 9: /* U field definition */
		if (c=='*') { /* we are done; all bits defined */
		    parsemode=1;
		    break;
		}
		if (c=='H') { /* we are in hex mode */
		    subparsemode=1;
		    break;
		}
		switch (subparsemode) {
		case 0: /* binary read */
		    if ((c<'0') || (c>'1')) { /* wrong digit */
			return -emsgl(14,linenumber);
		    }
		    if (c=='1') 
			js->ufield[js->ufieldbits/8] 
			    |= (1<<(js->ufieldbits%8));
		    js->ufieldbits++;
		    break;
		case 1: /* hex mode */
		    i=hextoc(c); 
		    //printf("char: %c, uf: %d, u: %02x %02x %02x %02x\n",
		    //	   c, js->ufieldbits, js->ufield[0], js->ufield[1],
		    //	   js->ufield[2], js->ufield[3]);
		    if (i<0) return -emsgl(15, linenumber);		    
		    js->ufield[js->ufieldbits/8] 
			|= i<<((js->ufieldbits%8)>3?4:0);
		    js->ufieldbits +=4;
		    break;
		}
		break;
	    case 10: /* end of file reached */
		/* simply ignore all text, add to transmission checksum */
		i=hextoc(c); if (i<0) return -emsgl(16, linenumber);
		tchks1c = tchks1c*16 + i;
		break;
	    default: 
		fprintf(stderr, "Undefined parse state: %d \n",parsemode);
		return 0;
	    }
	    
	}
    } while (parsemode<10);

    /* consistency checks */
    if (tchks2o != tchks2c) return -emsg(17);
    if (tchks1o != tchks1c) return -emsg(18);

    return 0; /* everything went well */
}  


int main (int argc, char *argv[]) {
    int opt; /* for option parsing */
    char sourcefilename[200] = "";
    FILE *inputstream = stdin; /* default: stdin */
    int i, retval;


    /* parse options */
    while ((opt=getopt(argc, argv, "f:")) != EOF) {
	switch (opt) {
	case 'f': /* input file name */
	    if (1!=sscanf(optarg,"%199s", sourcefilename)) return -emsg(1);
	    break;
	}
    }
    /* try to open source file */
    sourcefilename[199]=0; /* safety termination */
    if (sourcefilename[0]) { /* we have a name */
	inputstream = fopen(sourcefilename, "r");
	if (!inputstream) return -emsg(2);
    }
    
    /* pass info on to jedecfileparser */
    retval=populate_jed_structure(inputstream, &jed);
    if (retval) return -retval; /* an error has occured */
    

    printf(" Pin number: %d\n", jed.pinnumber);
    printf(" Fuse number: %d\n", jed.fusenumber);
    printf("security mode: %d\n", jed.securitymode);
    
    printf("E bits: %d\n", jed.efieldbits);
    for (i=0; i<(jed.efieldbits+7)/8; i++)
	printf(" %02x",jed.efield[i]);
    printf("\n\n");

    printf("U bits: %d\n", jed.ufieldbits);
    for (i=0; i<(jed.ufieldbits+7)/8; i++)
	printf(" %02x",jed.ufield[i]);
    printf("\n\n");
 
    printf("F bits: %d\n", jed.fusenumber);
#ifdef debug_showfusefield
    for (i=0; i<(jed.fusenumber+7)/8; i++) {
	printf(" %02x",jed.fusefield[i]);
	if ((i%16)==15) printf("\n");
    }
    printf("\n");
#endif

   
    return 0;
}

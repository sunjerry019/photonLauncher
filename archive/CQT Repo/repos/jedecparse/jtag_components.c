/* This file contains the code that deals with talking to the usb device with 
   elementary svf commands, based on bit chains and the programming interface.

   Taken from the jtagprog code used for the Lattice isp4000 devices.

*/

#include <stdio.h>
#include <stdint.h>
#include <sys/ioctl.h>
#include <string.h>
#include <math.h>
#include "usbprog_io.h"
#include "bitchain.h"

/* error definitions (dirty, should be in separate file */
#define ERR_USBDRIVER 25
#define ERR_FREQDEF 26
#define ERR_JTAGSTATE 27
#define ERR_WRONGSHIFTMODE 28
#define ERR_CHAINLENGTH 29
#define ERR_CHAINCOMPARISON 30
#define ERR_MISMATCH 31

/* some bit chain handling primitives */
/* concatenate:: target|source -> target */
int append_bit_chain(struct bit_chain *target, struct bit_chain *source) {
    int sourceshift, sshift2; /* how many bits to shift source to match target */
    int i, j; /* source / target index */
    int k = target->length; /* counting variable */
    int u;
    
    //printf(" target content: "); for (i=0;i<10;i++) printf("%02x ",target->content[i]);
    //printf(" src content: "); for (i=0;i<10;i++) printf("%02x ", source->content[i]);printf("\n");
    if ((k + source->length + 7)/8 >  MAXCHAINBYTES) {
	fprintf(stderr, "length issue: k: %d, length: %d\n",
		k,source->length);
	return -1;
    }
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
	return ERR_USBDRIVER; /* wrong response */
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
    if (freq <= 0.0) return ERR_FREQDEF; /* too low freq */
    val = ceil((1.0/freq-CLOCK_PERIODE_0)/CLOCK_PERIODE_1);
    if (val>255) return ERR_FREQDEF; /* too low freq */
    if (val<0) val=0; /* avoid trouble */
    
    // printf(" delay value is programmed to: %d\n",val);
    if (ioctl(handle, Set_Delay, val)) { /* test if echo is correct */
	return ERR_USBDRIVER; /* wrong response */
    }
    delayvalue=val;
    return 0;
}

/* sets end state of data/IR transfer. State is one out of four stable states */
int Set_ENDDR(int handle, int state) {
    if (state <0 || state >3) return ERR_JTAGSTATE; /* not stationary state */
    if (ioctl(handle, JTAG_ENDDR, state)) return ERR_USBDRIVER;
    return 0;
}
int Set_ENDIR(int handle, int state) {
    if (state <0 || state >3) return 5; /* not stationary state */
    if (ioctl(handle, JTAG_ENDIR, state)) return ERR_USBDRIVER;
    return 0;
}
int Go_State(int handle, int state) {
    if (state <0 || state >3) return ERR_JTAGSTATE; /* not stationary state */
    if (ioctl(handle, JTAG_runstate, state)) return ERR_USBDRIVER;
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

#define SHIFT_MODE_INSTRUCTION 1
#define SHIFT_MODE_DATA 0
/* send data stream; masking partially implemented. Parameters:
   mode: 0 for data, 1 for Instruction 
   tdi: input stream
   tdo: output pattern to be expexted. If NULL, no test
   mask: mask for output pattern. if NULL, mask is ignored */
int shift_data_IR(int handle, int mode, 
		  struct bit_chain *tdi, struct bit_chain *tdo,
		  struct bit_chain *mask) {
    int retval;
    //    struct bit_chain *header, *trailer;
    int command;
    struct bit_chain message;
    //int i;
    char rettext[256]; /* contains return text in case of mismatch */
    
    /* setting of data/instruction mode differences */
    switch (mode) {
    case SHIFT_MODE_DATA: /* data */
	//header=&header_dr; trailer = &trailer_dr;
	command = JTAG_scandata;
	break;
    case SHIFT_MODE_INSTRUCTION: /* instruction */
	//header=&header_ir; trailer = &trailer_ir; 
	command = JTAG_scanIR;
	break;
    default:
	return ERR_WRONGSHIFTMODE; /* wrong mode */
    }
    
    /* make bit string */
    message.length=0;
    //if (header->length) append_bit_chain(&message, header);
    if (tdi->length) {
	retval=append_bit_chain(&message, tdi);
	if (retval) return ERR_CHAINLENGTH;
    }
    //if (trailer->length) {
    //	retval=append_bit_chain(&message, trailer);
    //	if (retval) return ERR_CHAINLENGTH;
    //}

    //printf("data stream length: %d content:\n",message.length);
    //for (i=0; i<16; i++) printf("%02x ", message.content[i]&0xff);
    //printf("\n");
    /* send stream */
    retval=ioctl(handle, command, &message);
    //printf("point 2: retval= %d, err: %d\n",retval, errno);
    if (retval) return ERR_USBDRIVER;
    
  /* ToDo: Header test */
  /* ToDo: Trailer test */

    if (tdo) { /* we need to do comparison */
	//printf("data returned: %d content:\n",message.length);
	// for (i=0; i<16; i++) printf("%02x ", message.content[i]&0xff);
	//printf("\n");
	
	/* strip margins */
	//sub_bit_chain(&message, header->length, tdi->length); 
	/* compare result */
	//printf("point bling\n");
	retval=compare_bit_chains_masked(&message, tdo, mask);
	//printf("pong\n");
	if (retval<0) return ERR_CHAINCOMPARISON; /* error */
	if (retval>0) {
	    chain2text(&message, rettext);
	    printf(" mismatch return data: length: %d, content: %s\n",
		   message.length, rettext);
	    chain2text(tdo, rettext);
	    printf("                       length: %d expected: %s\n",
		   tdo->length, rettext);

	    return ERR_MISMATCH; /* Mismatch detected */    
	}
    }
    return 0;
}

#define MAX_CLOCKCYCLES ((1<<15)-1)
/* runtest command implement. clocks and timing are minimal values */
int runtest(int handle, int state, int clocks, double mintime) {
    int minclock, timclk, this_t;
    double period;
    if (state <0 || state >3) return ERR_JTAGSTATE; /* not stationary state */
    if (clocks<0 || mintime<0.0) return ERR_FREQDEF;
    minclock=clocks;
    /* integrate timing */
    period = CLOCK_PERIODE_0+ CLOCK_PERIODE_1 * delayvalue;
    timclk = ceil(mintime / period);
    if (timclk>minclock) minclock=timclk; /* use the larger of both */
    
    /* Run a number of clock cycles */
    do {
	this_t = minclock>MAX_CLOCKCYCLES?MAX_CLOCKCYCLES:minclock;
	if (ioctl(handle, JTAG_runstate, state | (this_t<<8))) 
	    return ERR_USBDRIVER;
	minclock -= this_t;
    } while (minclock>0);
    return 0;
}
/* trst code. state is 0 ot 1 */
int set_trst(int handle, int state) {
    if (ioctl(handle, JTAG_setTRST, state)) return ERR_USBDRIVER;
    return 0;
}

/*----------------------------------------*/
/* higher level commands useful for XO2 programming */

/* send 8 bit commmand, no data */
/* return is either zero (success) or an error code >0 */
int send_cmdonly(int handle, int command) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    return retval;
}

int send_dataonly(int handle, int data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = data & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}

void populate_bitchain(struct bit_chain *b, uint32_t c) {
    b->content[0] = c & 0xff; b->content[1] = (c >>8) & 0xff;
    b->content[2] = (c >> 16) & 0xff; b->content[3] = (c>>24)&0xff;
}

/* send 8 bit commmand with 32 bit argument / match / mask inputs */
/* return is either zero (success) or a mismatch or other error code >0 */
int sendreceive_32(int handle, int command, 
		   uint32_t in, uint32_t out, uint32_t mask) {
    struct bit_chain msg, outchain, maskchain;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=32;         populate_bitchain(&msg, in);
    outchain.length=32;    populate_bitchain(&outchain, out);
    maskchain.length=32;   populate_bitchain(&maskchain, mask);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, &outchain, &maskchain);
    if (retval) return retval; /* some error happened */
    return 0; /* everything went fine */
}

/* send 8 bit commmand with 8 bit argument, no tests */
/* return is either zero (success) or an error code >0 */
int send_8(int handle, int command, int data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=8;  populate_bitchain(&msg, data);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}

/* send 8 bit commmand with 16 bit argument, no tests */
/* return is either zero (success) or an error code >0 */
int send_16(int handle, int command, int data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=16;  populate_bitchain(&msg, data);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}

/* verify 16 bit argument */
/* return is either zero (success) or an error code >0 */
int verify_16(int handle, int in, int out, int mask) {
    struct bit_chain ic, oc,mc;
    int retval;
    /* populate content chains */
    ic.length=16;  populate_bitchain(&ic, in);
    oc.length=16;  populate_bitchain(&oc, out);
    mc.length=16;  populate_bitchain(&mc, mask);

    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &ic, &oc, &mc);
    return retval;
}

/* send 8 bit commmand with 24 bit argument, no tests */
/* return is either zero (success) or an error code >0 */
int send_24(int handle, int command, int data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    //msg.content[1]=data & 0xff;
    //msg.content[2]=(data>>8) & 0xff;
    //msg.content[3]=(data>>16) & 0xff;

    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=24;  populate_bitchain(&msg, data);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
    			 &msg, NULL, NULL);
    return retval;
}


/* send 8 bit commmand with 208 one bits for Boundary scan preparation. */
/* return is either zero (success) an error code >0 */
int Bscan_208(int handle, int command) {
    struct bit_chain msg;
    int retval, i;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    
    /* populate content chains */
    msg.length=208; for (i=0; i<208/8; i++) msg.content[i]=0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}
/* ominous bypass test code; not clear what this does... */
/* return is either zero (success) an error code >0 */
int Bypasstest(int handle) {
    struct bit_chain msg, outchain, maskchain;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = 0xff;
    outchain.length=8; outchain.content[0]=0;
    maskchain.length=8; maskchain.content[0]=0xc0;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, &outchain, &maskchain);
    return retval;
}

/* Read LSC_BUSY register. similar to sendreceive_32, but does a 8 bit
   read and test. return is either zero (success) or a mismatch (31) or
   other error code >0 */
int LSC_Busy_test(int handle) {
    struct bit_chain msg, outchain, maskchain;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = 0xf0; /* this is LSC_CHECK_BUSY */
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=8;         msg.content[0]=0;
    outchain.length=8;    outchain.content[0]=0;
    maskchain.length=8;   maskchain.content[0]=0x80; /* test bit 7 */
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, &outchain, &maskchain);
    if (retval) return retval; /* some error happened */
    return 0; /* everything went fine */
}

/* send 8 bit commmand with a 128 bit argument, no tests. Argument is a
   pointer to the start address of the buffer from which 16 bytes are taken.
   return is either zero (success) or an error code >0 */
int send_128bit(int handle, int command, unsigned char *data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=128;  memcpy(msg.content, data, 16);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}

/* send 8 bit commmand with a 64 bit argument, no tests. Argument is a
   pointer to the start address of the buffer from which 8 bytes are taken.
   return is either zero (success) or an error code >0 */
int send_64bit(int handle, int command, unsigned char *data) {
    struct bit_chain msg;
    int retval;
    /* send 8 bit instruction */
    msg.length=8; msg.content[0] = command & 0xff;
    retval=shift_data_IR(handle, SHIFT_MODE_INSTRUCTION,
			 &msg, NULL, NULL);
    if (retval) return retval; /* some error happened */
    /* populate content chains */
    msg.length=64;  memcpy(msg.content, data, 8);
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, NULL, NULL);
    return retval;
}


/* send 8 bit commmand with a 128 bit argument, do test. Argument is a
   pointer to the start address of the buffer from which 16 bytes are taken.
   return is either zero (success) or an error code >0 */
int verify_128bit(int handle, unsigned char *data) {
    struct bit_chain msg, outchain, mask;
    int retval, i;
    /* populate content chains */
    msg.length=128;
    outchain.length = 128;mask.length = 128;
    for (i=0; i<16; i++) { msg.content[i]=0; mask.content[i]=0xff;}
    for (i=0; i<16; i++) outchain.content[i] = data[i];
    printf("copied...\n");
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, &outchain, &mask);
    return retval;
}
/* send 8 bit commmand with a 64 bit argument, do test. Argument is a
   pointer to the start address of the buffer from which 8 bytes are taken.
   return is either zero (success) or an error code >0 */
int verify_64bit(int handle, unsigned char *data) {
    struct bit_chain msg, outchain, mask;
    int retval, i;
    /* populate content chains */
    msg.length=64;
    outchain.length = 64;mask.length = 64;
    for (i=0; i<8; i++) { msg.content[i]=0; mask.content[i]=0xff;}
    for (i=0; i<8; i++) outchain.content[i] = data[i];
    printf("copied...\n");
    retval=shift_data_IR(handle, SHIFT_MODE_DATA,
			 &msg, &outchain, &mask);
    return retval;
}

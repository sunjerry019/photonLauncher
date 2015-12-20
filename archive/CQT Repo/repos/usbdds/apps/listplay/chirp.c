/* program example to test elements of the listplay mode;

   This code generates a table of configuration entries for a linear chirp
   on a single channel (0), and an amplitude sweep with a Gaussian envelope
   over xxx elements.

   Once this code has run, the elements are stepped through with pulses at
   the P3 input, and may be reset to the head of the list with a pulse on P2.
   The minimum pulse width for the P3 pulse is (something small), while the
   P2 pulse needs to be at least 10 usec long. In case that there is a transfer
   into the FIFO taking place, the P2 pulse needs to be at least 100us long.
   
   For each table entry, we need:
   - frequency setting for the tuning word (that is 5 bytes)
   - amplitude setting (that is 4 bytes)

   So each update sequence cluster is 9 bytes long.
   
   Initially, we need to have a sequence which does the following:
   - slect one channel (0) and IO mode (singletone) (2 bytes)
   - set FR1 register to something senisble (4 bytes)
   - set CFR0 (4 bytes)
   - set CTFW0 (5 bytes, initial condition)
   - set ACR register (4 bytes)
   
   so the initialization sequence is 19 bytes long.
   
   In this code, we reset the device into standard EP2 mode, then transmit
   the initialization code. The we stop the standard EP2 mode, switch over to
   the listplay mode and transfer the chirp data into the system.

   The program is left in the Listplay mode, so the chirp can either be
   repeated with subsequent clock pulses on P3, or reset to the beginning
   of the sequence with the trigger input (P2).

 */

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <math.h>


#include "usbdds_io.h"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Error opening device", /* 1 */
  "timing out of range",
  "malloc failed",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define DEVICENAME "/dev/ioboards/dds0"

/* some parameters for the chirp generation; points are centered in half
   of the pulse */
#define NUMBER_OF_ENTRIES 100
#define START_FREQ 1123000
#define END_FREQ   2000000
#define SIGMA_AMPLITUDE 20   /* in multiples of entry steps */
#define CENTER_AMPLITUDE 50  /* where is the Gaussian centered */


/* this function fills the buffer with a control word for a tuning
   info both for frequency and amplitude. Frequency is specified in
   Hertz, amplitude in integer values between 0-1023.   */
#define BYTES_PER_TUNING 9
void maketuningword(unsigned char *buffer, int frequency, int amplitude) {
  unsigned long long tempbuf;
  tempbuf=0x100000000ll*frequency;
  tempbuf = tempbuf / 500000000; /* this now contains the scaled freq */
  buffer[0]=0x04; /* frequency tuning word */
  buffer[1]=(tempbuf>>24) & 0xff;
  buffer[2]=(tempbuf>>16) & 0xff;
  buffer[3]=(tempbuf>>8) & 0xff;
  buffer[4]=tempbuf & 0xff;
  
  buffer[5]=0x06; /* select ACR register */
  buffer[6]=0; /* amplitude ramp rate */
  buffer[7]=0x14 | ((amplitude>>8 )&0x03); /* enable Ampl, load @ioupdate */
  buffer[8]=amplitude & 0xff;
}

/* this is the buffer for the initial register setting */
unsigned char initialconfig[23] = {
  0x01, 0xa8, 0x00, 0x20, /* FR1: 2 levels, no rampup/down*/
  0x00, 0xf6, /* chan 0, 4 bit serial */
  0x03, 0x00, 0x03, 0x00, /* CFR0: no modulation, fullswing amp, no autoclear */
  0x00, 0xf6, /* chan 0, 4 bit serial */
  0x04, 0x05, 0x1e, 0xb8, 0x51, /* CTW0 zero frequency to start with */
  0x00, 0xf6, /* chan 0, 4 bit serial */
  0x06, 0x00, 0x13, 0xff  /* ACR: zero amplitude Amp on, rate off */
};

int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    int retval, i;
    unsigned long long freq;
    double amp;
    unsigned char *configtable;
    
    /* get some memory */
    configtable = (unsigned char *)malloc(10000);
    if (!configtable) return -emsg(3);

    /* open device */
    handle=open(DEVICENAME,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
	fprintf(stderr, "errno: %d",errno);
	return -emsg(1);
    }

    /* send basic configuration string to device */
    retval=ioctl(handle, Full_DDS_Reset);
    printf("device was reset; retval: %d\n",retval);
    //sleep(1);
    retval=write(handle, initialconfig, 23);
    printf("init string sent; retval for write: %d\n",retval);


    /* prepare the configuration table with 1000 entries*/
    for (i=0;i<NUMBER_OF_ENTRIES; i++) {
      freq = START_FREQ+(END_FREQ-START_FREQ)*i/NUMBER_OF_ENTRIES;
      amp = ((double)i-CENTER_AMPLITUDE)/SIGMA_AMPLITUDE;
      //printf("%d: argument : %f",i, amp);
      amp = 1023.0*exp(0.0-amp*amp/2);
      //printf("amplitude: %f\n",amp);
      maketuningword(&configtable[i* BYTES_PER_TUNING],
		     (unsigned int)freq,
		     lrint(amp));
    }

    /* now attempt to set device in listplay mode with 9 entries per cluster */
    retval=ioctl(handle,Stop_Transfer ); 
    //printf("transfer stopped. retval: %d\n",retval);
    retval=ioctl(handle,ListplayMode, BYTES_PER_TUNING ); /* 10 entries */
    //printf("set in listplay mode; retval: %d\n",retval);
    retval=ioctl(handle,StartListplayMode ); 
    //printf("transfer stopped. retval: %d\n",retval);

    retval=write(handle, configtable,NUMBER_OF_ENTRIES * BYTES_PER_TUNING);
    printf("init string sent; retval for write: %d\n",retval);


    free(configtable);

    close(handle);
    
    return 0;

}

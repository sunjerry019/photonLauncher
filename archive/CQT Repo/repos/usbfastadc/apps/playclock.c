/* program to program the clock/ADC chips on the board via the SPI interface.
   preliminary to test out the board
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "usbfastadc_io.h"


/* error handling */
char *errormessage[] = {
  "No error.",
  "Cannot open device.", /* 1 */
  "Cannot parse device fila name",
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

#define FILENAMLEN 200
#define DEFAULTDEVICENAME "/dev/ioboards/usbfastadc0"

/* read back status registers located in 0x22c, 0x22d. parameter is handle,
   return is 0x22c in its 0..7, 0x22D in bits 8..15 */
int getstatusbits(int handle) {
  char buffer[10];
  int retval;
  buffer[0]=2; /* read back two bytes */
  buffer[1]=0x02; buffer[2]=0x2d; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  //for (i=0; i<6; i++) printf("  %d:0x%02x\n",i,buffer[i]&0xff);
  return ( (buffer[3]<<8) & 0xff00 ) + (buffer[4] & 0xff);
}
/* read back some registers */
void readregister(int handle, int adr, int num) {
  char buffer[256];
  int retval, i;
  buffer[0]=num; /* read back some bytes */
  buffer[1]=(adr >>8)&0x1f; buffer[2]=adr & 0xff; /* high starting address */
  retval=ioctl(handle, CLOCKCHIP_READ, buffer);
  if (retval) printf("error in reading ioctl, retval=%d\n",retval);
  for (i=0; i<num; i++) printf("%03x: 0x%02x\n",adr-i,buffer[3+i]&0xff);

}



int main(int argc, char *argv[]){
    int handle; /* file handle for usb device */
    char devicefilename[FILENAMLEN] = DEFAULTDEVICENAME;
    int opt; /* for parsing options */
    int retval,i;

    char spidata[250]; /* array that gets sent to the devices */

    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "d:")) != EOF) {
       switch (opt) {
       case 'd': /* enter device file name */
	 if (sscanf(optarg,"%99s",devicefilename)!=1 ) return -emsg(2);
	 devicefilename[FILENAMLEN-1]=0; /* close string */
	 break;
       }
    }

    /* open device */
    handle=open(devicefilename,O_RDWR | O_NONBLOCK);
    if (handle==-1) {
      fprintf(stderr, "errno: %d; ",errno);
      return -emsg(1);
    }

    /* reset device */
    spidata[0]=1; /* 1 bytepayload data */ 
    spidata[1]=0; spidata[2]=0;/* address of register */
    spidata[3]=0x24; /* issue a reset */

    //retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    //printf("return value from write 1: %d\n",retval);

    /* PLL2 configuration, registers 0xf6..0xf0 */
    spidata[0]=7;
    spidata[1]=0x00; spidata[2]=0xf6;/* address of register, start w 0xf6 */
    spidata[3]=0x00; spidata[4]=0x00; /* PLL2 filter loop control */
    spidata[5]=0x00; /* VCO divider control, div-by-4 */
    spidata[6]=0x08; /* VCO control: treat ref as valid*/
    spidata[7]=0x03; /* PLL2 control: normal mode */
    spidata[8]=0x30; /* PLL2 feedback divider. A=0, B=48 (total N: 192) */
    spidata[9]=0x10; /* PLL charge pump control (56 uA) */
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from write PLL2: %d\n",retval);

    /* Output configurations channel 3-0 */
    spidata[0]=12;
    spidata[1]=0x01; spidata[2]=0xa1;/* address of register, start w 0x1a1 */
    spidata[3]=0x00; spidata[4]=0x1f; spidata[5]=0x20; /* ch 3 */ 
    spidata[6]=0x00; spidata[7]=0x2f; spidata[8]=0x02; /* ch 2 /48, LVDS 3.5mA*/ 
    spidata[9]=0x00; spidata[10]=0x2f; spidata[11]=0x08; /* ch 1: /48 */ 
    spidata[12]=0x00; spidata[13]=0x1f; spidata[14]=0x20; /* ch 0 */
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from write out 0-3: %d\n",retval);

    /* Output configurations channel 4,5 */
    spidata[0]=6;
    spidata[1]=0x01; spidata[2]=0xb3;/* address of register, start w 0x1b3 */
    spidata[3]=0x00; spidata[4]=0x1f; spidata[5]=0x20; /* ch 5 */ 
    spidata[6]=0x00; spidata[7]=0x1f; spidata[8]=0x20; /* ch 4 */ 
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from write out 4,5: %d\n",retval);

    /* PLL1 parameter set */
    spidata[0]=13;
    spidata[1]=0x00; spidata[2]=0x1c;/* address of register, start w 0x1c */
    spidata[3]=0x48; /* select refa, Vcc/2 when no signal */
    spidata[4]=0x30; /* 0x1b: OSC_in is feedb ref, ZD, REFA in CMOS mode */
    spidata[5]=0x28; /* 0x1a: REFA is enabled, REFA, OSCinREFB in cmos mode */
    spidata[6]=0x03; /* 0x19: normal operation, minimum antibacklash */
    spidata[7]=0x0c; /* 0x18: 6 uA pump current */
    spidata[8]=0x0;  /* 0x17: feedback MSB0 */
    spidata[9]=0x14; /* 0x16: feedback LSB: 20 */
    spidata[10]=0x00; spidata[11]=0x01; /* 0x15: reserved , 0x14: test div*/
    spidata[12]=0x00; spidata[13]=0x01; /* 0x13/0x12: REFB R divider=1 */
    spidata[14]=0x00; spidata[15]=0x0a; /* 0x11/0x10: REFA R divider=10 */

    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from PLL1 control: %d\n",retval);
   
    /* PLL1 ouput control */
    spidata[0]=2;
    spidata[1]=0x01; spidata[2]=0xbb;/* address of register, start w 0x1bb */
    spidata[3]=0x80; /* PLL1 output driver off, no routing to outputs 0,1 */
    spidata[4]=0x18; /* 0x1ba: PLL1 output divider=8, output strenght=weak*/
    //retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    //printf("return value from PLL1 OUTPUT control: %d\n",retval);
    
    


    /* power down control of PLLs */
    spidata[0]=1; /* 1 bytepayload data */ 
    spidata[1]=2; spidata[2]=0x33;/* address of register */
    spidata[3]=0x0; /* powerdown distribution down rest up */
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from powercontrol: %d\n",retval);
    

    /* update registers */
    spidata[0]=1; /* 1 bytepayload data */ 
    spidata[1]=2; spidata[2]=0x34;/* address of register */
    spidata[3]=0x1; /* issue a reset */
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from write 3: %d\n",retval);
    
    /* initiate calibration */
    spidata[0]=1; /* 1 bytepayload data */ 
    spidata[1]=0; spidata[2]=0xf3;/* address of register */
    spidata[3]=0xa;
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from init calibration: %d\n",retval);

    /* update registers */
    spidata[0]=1; /* 1 bytepayload data */ 
    spidata[1]=2; spidata[2]=0x34;/* address of register */
    spidata[3]=0x1; /* issue a reset */
    retval=ioctl(handle, CLOCKCHIP_WRITE, spidata);
    printf("return value from write 3: %d\n",retval);

    /* some test */
    readregister(handle,0xf5, 5);
    /* populate SPI data with something simple */
    
    for (i=0; i<3; i++) {
      printf("status bits: %04x\n",getstatusbits(handle));
      usleep(500000);
    }
    /* send stuff to SPI interface */

    /* read out a SPI register */

    close(handle);
    
    return 0;

}

/* code to test the PLL on the new pattern generator board. This is
   preliminary code, not meant for any production boards. 
   The sequence below works as of 25 May 2014, together with a device driver
   and card firmware.
*/

#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include "usbpattgen_io.h"
#include <unistd.h>
#include <sys/ioctl.h>

#define DEFAULT_DEVICENAME "/dev/ioboards/pattgen_generic0"

/* error handling */
char *errormessage[] = {
  "No error.",
  "Unable to open USB device.", /* 1 */
  "error parsing frequency argument.",
  "error sending USB command for RF initialize",
  "error sending USB command for PLL string",
  "readback error", /* 5 */
  "Frequency below VCO capability",
  "Frequency above VCO capability",
  "Main PLL divider out of range",
  "Error submitting RFsource config over USB",
  "Cannot parse device file name",  /* 10 */
};
int emsg(int code) {
  fprintf(stderr,"%s\n",errormessage[code]);
  return code;
};

char SoftReset[4] = { /* plays with reg 0x00 for update*/
  3, /* send one byte only */
  0x00, 0x00, /* to the update register */
  0x24
};

char PLL2config[10] = { /* this programs the PL2 related registers from
			   0xf0..f6. Parameters are 4GHz operation */
  9,  /* number of bytes sent to chip: 2 adr/dir + 7 data */
  0x60, 0xf6, /* streaming write, starting at 0xf6 */
  0x00, 0x00, /* 0xf6/f5: PLL2 loop control: cp1=0pf, Rz=3250, Rp2=900 */
  0x06,       /* 0xf4: VCO divider to 10 (gives 400 MHz base freq ) */
  0x08,       /* 0xf3: VCO2 control: treat ref as valid */
  0x03,       /* 0xf2: PLL2 control: charge pump normal, */
  0x32,       /* 0xf1: PLL2 fb divider: A=0, B=50 ->divider ratio 200 */
  0x10       /* 0xf0: Charge pump control PLL2: about 35 uA */
};

char Channel1_config[6] = { /* this programs the channel 1 related registers
				from 0x199..0x19B to LVPECL, 50MHz */
  5,  /* number of bytes sent to chip: 2 adr/dir + 7 data */
  0x41, 0x9b, /* 3-byte-write , starting at 0x19b */
  0x00, 0x07, /* 0x19a/b: phase 0, divider 8 */
  0x03        /* 0x199: LVDS (7mA), obey sync */
  
};

char Channel4_config[6] = { /* this programs the channel 1 related registers
				from 0x199..0x19B to CMOS, 50MHz */
  5,  /* number of bytes sent to chip: 2 adr/dir + 7 data */
  0x41, 0xB0, /* 3-byte-write , starting at 0x19b */
  0x00, 0x07, /* 0x19a/b: phase 0, divider 8 */
  0x08        /* 0x199: CMOS at ch4+ output, obey sync */
  
};

char PLL1config[17]= { /* this programs the PLL1 related registers from
			  0x10..0x1d */
  16, /* number of bytes sent to chip: 2 address/direction + 14 data */
  0x60, 0x1d, /* streaming write, starting at address 0x1d */
  0x00, /* 0x1D: PLL1 loop zero control to 883 kOhm */
  0x48, /* 0x1c: PLL1 misc control: osc_ctl to vcc/2 if noref, force ref A */
  0x30, /* 0x1b: internal zero delay, no zero delay, zdin single ended mode */
  0x2c, /* 0x1a: REFA differential, other ref in power down, osc_in SE mode */
  0x03, 0x0c, /* 0x19/18: PLL1 charge pump ctl: normal op, 6 uA */
  0x00, 0x14, /* 0x17/16: PLL1 feedback divider to 20 (1MHz loop op ) */
  0x00, /* 0x15: reserved */
  0x01, /* 0x14: test divider ->1 */
  0x00, 0x0a, /* 0x13/12: ref B R divider ->10 */
  0x00, 0x0a /* 0x11/10: ref A R divider ->10 for 10 MHz input ref */
};

char PLL1Output[5] = {
  4,
  0x21, 0xbb,
  0x80,
  0x03
};

char poweronPLL[4] = { /* PLL powerdown bits are switched off */
  3,
  0x02, 0x33, /* registre 0x233 */
  0x00
};

/* list of configuration sequences for the PLL */
char submitRF[4] = { /* plays with reg 0x234 for update*/
  3, /* send one byte only */
  0x02, 0x34, /* to the update register */
  0x01
};

char StartVCOcalibration[4] = { /* issues a calib start */
  3,
  0x00, 0xf3,
  0x0a
};

char StartSync[4] = {
  3,
  0x02, 0x32, 0x01
};
char StopSync[4] = {
  3,
  0x02, 0x32, 0x00
};


char ConfigureStatus0[4] = { /* setting of the FS0 mux */
  3,
  0x02, 0x30,
  0x02  /* pll1 is locked */
};


char scratch[64]; /* for readback */

int main(int argc, char *argv[]) {
  int handle; /* file handle for usb device */
  char devicefilename[200]=DEFAULT_DEVICENAME; /* name of device */
  int i;
  
  handle=open(devicefilename,O_RDWR);
  if (handle==-1) return -emsg(1);

  /* initialize PLL chip */
  //if (ioctl(handle, InitializeRFSRC)) return -emsg(3);

  /* send one of the configuration strings */

  printf("point 0\n");
  if (ioctl(handle, SubmitPLLtext, SoftReset)) return -emsg(4);

  printf("point 1\n");
  if (ioctl(handle, SubmitPLLtext, PLL2config)) return -emsg(4);

  printf("point 2A\n");
  if (ioctl(handle, SubmitPLLtext, ConfigureStatus0)) return -emsg(4);


  printf("point 3\n");
  if (ioctl(handle, SubmitPLLtext, Channel1_config)) return -emsg(4);
  if (ioctl(handle, SubmitPLLtext, Channel4_config)) return -emsg(4);

  printf("point 2\n");
  if (ioctl(handle, SubmitPLLtext, PLL1config)) return -emsg(4);

  printf("point 3a\n");
  if (ioctl(handle, SubmitPLLtext, PLL1Output)) return -emsg(4);


  printf("point 4\n");
  if (ioctl(handle, SubmitPLLtext, poweronPLL)) return -emsg(4);

  printf("point 4a\n");
  if (ioctl(handle, SubmitPLLtext, submitRF)) return -emsg(4);

  printf("point 5\n");
  if (ioctl(handle, SubmitPLLtext, StartVCOcalibration)) return -emsg(4);

  printf("point 6\n");
  if (ioctl(handle, SubmitPLLtext, submitRF)) return -emsg(4);

  printf("point 6a\n");
  if (ioctl(handle, SubmitPLLtext, StartSync)) return -emsg(4);
  if (ioctl(handle, SubmitPLLtext, submitRF)) return -emsg(4);
  if (ioctl(handle, SubmitPLLtext, StopSync)) return -emsg(4);
  if (ioctl(handle, SubmitPLLtext, submitRF)) return -emsg(4);

  printf("point 7\n");
  scratch[0]=2; scratch[1]=0xa2; scratch[2]=0x2d;
  i=ioctl(handle, ReadPLLtext, scratch);
  printf("return value: %d\n",i);

  for (i=0; i<20; i++) {
    printf("%02x ",scratch[i]&0xff);
  }
  printf("\n");

  usleep(50000);

  printf("point 8\n");
  scratch[0]=2; scratch[1]=0xa2; scratch[2]=0x2d;
  i=ioctl(handle, ReadPLLtext, scratch);
  printf("return value: %d\n",i);

  for (i=0; i<20; i++) {
    printf("%02x ",scratch[i]&0xff);
  }
  printf("\n");

  return 0;

}

/* usbfastadc_io.h: commands to interface the test timestamp unit.
   taken from fastadc. work in progress.


 Copyright (C) 2010-2015 Christian Kurtsiefer, National University
                         of Singapore <christian.kurtsiefer@gmail.com>
--
   This header file is used by the firmware on the FX2 chip, the device driver,
   and the user program that eventually talks to the usb device.

   The usb command structure for the EP1 packets is as follows:
   ofs  what
   0    packet length in bytes
   1    command byte
   2    start of data section, as described below

   Selection of what commands are used are done with the "firmware" define

   More explanation to come.  */

#define _CLOCKCHIP_WRITE      50   /* sends a command via the SPI interface
				      into the clock generation chip. Argument
				      structure: 2 bytes length (of data,
				      excluding the command word, MSB first),
				      then command word (MSB first), then
				      optional data. Firmware overwrites adr
				      and r/w selection. ioctl Argument is
				      pointer to a buffer with this argument*/
#define _CLOCKCHIP_READ       51   /* sends a command via the SPI interface
				      into the clock generation chip. Argument
				      structure: 2 bytes length (of data,
				      excluding the command word, MSB first),
				      then command word (MSB first). Data is
				      returned in the same buffer, but does not
				      overwrite the first four command/len
				      bytes. Firmware overwrites adr
				      and r/w selection. ioctl Argument is
				      pointer to a buffer with this argument */
#define _ADCCHIP_WRITE        52   /* Same as clockchip_write, but for ADC */
#define _ADCCHIP_READ         53   /* Same as clockchip_read, but for ADC */
#define _WRITE_CPLD           54   /* Writes two bytes into the config space
				      of the CPLD. Format: low byte high byte */
#define _START_STREAM         55   /* Start continuous acquisition; no
				      additional parameters */
#define _START_LIMITED        56   /* Start acquisition w limited number of
				      events. Parameter: number of samples */
#define _STOP_STREAM          57   /* Stop acquisition. no additional
				      parameters */
#define _GETRDYLINESTAT       58   /* Return status line byte  */
#define _GETBYTECOUNT         59   /* Returns 16 bit number  */
#define _FLUSH_FIFO           60   /* issue a inpktend2  */
#define _RESET_TRANSFER       61   /* abort GPIF, switch to internal clock */
#define _GET_TCB              62   /* get full TCB content */
#define _SET_OVERFLOWFLAG     63   /* one byte arg: if !=0, break on ovflow */
#define _WRITE_CPLD_LONG      64   /* write two 16bit words into the CPLD,
				      LSB is first, MSB second */
#define _SET_POWER_STATE      65   /* takes one byte argument; if !0, power
				      switchmode converters on */
#define _GET_POWER_STATE      66   /* returns a 1 byte value with IOA status */

/* commands that only make sense in the USB driver side, not in the firmware */
#define _Start_USB_machine    70   /* start USB engine on host */
#define _Stop_USB_machine     71   /* stop USB engine on host */
#define _Get_transferredbytes 72   /* return number of bytes safely accessible
				      in mmaped buffer. The returned quantity
				      can roll over at 2**31 bytes */
#define _Get_errstat          73   /* get error status during read */


/* Check if we have already a firmware selection */
#ifndef IOCBASE

#ifdef firmware
#define IOCBASE 0x00 /* we stay bytewise */
#define IOCBASEW 0x00
#define IOCBASEWR 0x00
#else
#include <linux/ioctl.h>
#define IOCBASE 0xaa00
#define IOCBASEW 0xaa00
#define IOCBASEWR 0xaa00
#endif

#endif


/* here are the definitions which restore the values for both firmware and
   driver/application domain */

#define CLOCKCHIP_WRITE    ( _CLOCKCHIP_WRITE | IOCBASEW )
#define CLOCKCHIP_READ     ( _CLOCKCHIP_READ  | IOCBASEWR )
#define ADCCHIP_WRITE      ( _ADCCHIP_WRITE   | IOCBASEW )
#define ADCCHIP_READ       ( _ADCCHIP_READ    | IOCBASEWR )
#define WRITE_CPLD         ( _WRITE_CPLD      | IOCBASEWR )
#define START_STREAM       ( _START_STREAM    | IOCBASEWR )
#define START_LIMITED      ( _START_LIMITED   | IOCBASEWR )
#define STOP_STREAM        ( _STOP_STREAM     | IOCBASEWR )
#define GETRDYLINESTAT     ( _GETRDYLINESTAT  | IOCBASEWR )
#define GETBYTECOUNT       ( _GETBYTECOUNT    | IOCBASEWR )
#define FLUSH_FIFO         ( _FLUSH_FIFO      | IOCBASE )
#define RESET_TRANSFER     ( _RESET_TRANSFER  | IOCBASE )
#define GET_TCB            ( _GET_TCB         | IOCBASEWR )
#define SET_OVERFLOWFLAG   ( _SET_OVERFLOWFLAG| IOCBASEW )
#define WRITE_CPLD_LONG    ( _WRITE_CPLD_LONG | IOCBASEW )
#define SET_POWER_STATE    ( _SET_POWER_STATE | IOCBASEW )
#define GET_POWER_STATE    ( _GET_POWER_STATE | IOCBASEW )

/* definitions that are only used in host side USB driver - no need to pollute
   firmware namespace */
#ifndef firmware

#define Start_USB_machine    ( _Start_USB_machine    | IOCBASE )
#define Stop_USB_machine     ( _Stop_USB_machine     | IOCBASE )
#define Get_transferredbytes ( _Get_transferredbytes | IOCBASEWR )
#define Get_errstat          ( _Get_errstat          | IOCBASEWR )

#endif

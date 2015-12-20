/* usbprog_io.h: commands to talk to the usb programmer. Work in progress.


 Copyright (C) 2010 Christian Kurtsiefer, National University
                         of Singapore <christian.kurtsiefer@gmail.com>
--

   definitions of ioctl commands for the usb-timetag card executed by 
   the firmware in the card interface  */

#define  _Reset_Target        1    /* needs no argument */
#define  _Unreset_Target      2    /* takes a 16bit value as argument */
#define  _Send_Word           3    /* sends 4 bytes, returns 4 bytes  */
#define  _Set_Delay           4    /* set one byte as delay value */

/* JTAG command definition */
#define _JTAG_ENDDR           5    /* end state for the data shift;
				      needs one byte argument */
#define _JTAG_ENDIR           6    /* end state for the instruction shift;
				      needs one byte argument */
#define _JTAG_freq            7    /* sets maximal frequency...CHANGE THS!! 
				      argument size TBD */
#define _JTAG_runstate        8    /* moves to particular state and runs there;
				      argument is 16 bit int */
#define _JTAG_scandata        9    /* goes through data shift; argument
				      structure TBD */
#define _JTAG_scanIR          10   /* goes through instruction shift; argument
				      structure TBD */
#define _JTAG_setTRST         11   /* set TRST line; takes one byte argument.
				      state of this line is in lsb */
#define _JTAG_forcestate      12   /* moves to a particular state, rest as in
				      JTAG_runstate */
#define _JTAG_initialize      13   /* brings JTAG engine and lines in
				      well-defined state; no arguments */
#define _SWD_Write            14   /* send out a 32bit word. Argument is
				      control byte plus four data bytes.
				      returns the Ack status */
#define _SWD_Read             15   /* read 32bit word. Argument is
				      control byte. returns ack and parity */
#define _SWD_Acquire          16   /* Tries to acquire the debug port. The
				      one-byte arg decides if a program key
				      should be deployed (for bit 0 set), and if
				      8 clock pulses should be sent after the
				      main transfer (for bit 1 set). If bit 2
				      is set, the Read mode inserts a clock
				      pulse for a turnover after a read. This
				      seems necessary for newer silicon revs,
				      and is compatible with the ARM spec for
				      the SWD protocol, but it does not work
				      with some of the earlier revs. Returns 2
				      bytes, ack status and residual attempts */
#define _SWD_Reset            17   /* send a number of high pulses down the
				      data line. parameter is one byte with
				      the number of pulses. No return value */
#define _SWD_Sendword         18   /* send 16 bits down the data line.
				      parameter is two bytes with the bit
				      pattern, lsb first. Used for jtag/swd
				      mode switching. No return value */
				      
				      
/* value definitions for different states of the JTAG state machine */
#define TST_LOGIC_RESET 0
#define RUN_TST_IDLE    1
#define PAUSE_DR        2
#define PAUSE_IR        3
#define SHIFT_DR        4
#define SHIFT_IR        5


/* The following is an attempt to make the ioctl commands compliant to the
   recommendation for ioctl numbers in a linux system and maintain the one-byte
   size for commands sent over the USB channel since it appears that the
   single byte ioctls get swallowed by the OS otherwise. So for now, the
   header file does need to be preceeded by a compiler statement to define
   "firmware" if the header file is used to generate firmware code. */

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

/* here are the definitions which restore the values for both firmware and
   driver/application domain */

#define  Reset_Target        ( _Reset_Target | IOCBASE )
#define  Unreset_Target      ( _Unreset_Target | IOCBASE )
#define  Send_Word           ( _Send_Word | IOCBASEWR )
#define  Set_Delay           ( _Set_Delay | IOCBASEW )

#define  JTAG_ENDDR          (_JTAG_ENDDR | IOCBASEW)
#define  JTAG_ENDIR          (_JTAG_ENDIR | IOCBASEW)
#define  JTAG_freq           (_JTAG_freq | IOCBASEW)
#define  JTAG_runstate       (_JTAG_runstate | IOCBASEW)
#define  JTAG_scandata       (_JTAG_scandata | IOCBASEWR)
#define  JTAG_scanIR         (_JTAG_scanIR | IOCBASEWR)
#define  JTAG_setTRST        (_JTAG_setTRST | IOCBASEW)
#define  JTAG_forcestate     (_JTAG_forcestate | IOCBASE)
#define  JTAG_initialize     (_JTAG_initialize | IOCBASE)

#define  SWD_Write           ( _SWD_Write   | IOCBASEWR)
#define  SWD_Read            ( _SWD_Read    | IOCBASEWR)
#define  SWD_Acquire         ( _SWD_Acquire | IOCBASEWR)
#define  SWD_Reset           ( _SWD_Reset   | IOCBASE)
#define  SWD_Sendword        (_SWD_Sendword | IOCBASEW)

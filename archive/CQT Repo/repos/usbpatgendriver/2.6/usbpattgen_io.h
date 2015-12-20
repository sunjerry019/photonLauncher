/* ioctl() definitions for the pattern generator. Both used for communication
   with the firmware on the EP1 interface, and (for the larger values) to 
   communicate with the host side driver */

#define  _Reset_Pattern_unit  1    /* prepare clean state of the device; 
				     details TBD */
#define  _SendDac             2    /* takes a 16bit value as argument for value
				     and 8 bit value for channel */
#define  _InitDac             3    /* initialize DAC, no args  */
#define  _InitializeRFSRC     4    /* initialize RF PLL, noargs */
#define  _Rf_Reference        5    /* selects the internal or ext ref src */
#define  _Send_RF_parameter   6    /* PLL programming stuff, takes 16 bit wrd */

/* The three modes of operation are Run, Idle and Prog; frm each mode, there
   can be a jump to another mode. Abortion of the Programming will wait until
   the EP2 is completely empty. */
#define  _RunMode             7    /* switch system into running mode */
#define  _IdleMode            8    /* put RAM machinery in halt mode, more 
				     specifics need TBD */
#define  _PatternRAM_lseek    9    /* prepare address counter; can be 32 or 24
				     bit wide address, but only 24 bits are
				     digested by the firmware. */
#define _ProgMode             10   /* put machine into programming mode */
#define _ForceIdle            11   /* stops programming regardless of pending
				     buffer content */
#define _ForceRun             12   /* stops program regarding of EP2 buffer
				     content */
#define _Send_AUXRF_parameter 13   /* sets the divider/phase combo */
#define _RequestStatus        99   /* request status for debugging 
				     10: return GPIFTCNT */

/* new commands for playing with clock chip directly */
#define _SubmitPLLtext        14   /* in ioctl mode, takes a pointer to a
				     character sequence that gets sent
				     to the PLL device. The first byte there
				     contains the byte count for the following
				     bytes. In firmware mode, the text stream
				     follows the usb identifier. */
#define _ReadPLLtext        15   /* in ioctl mode, takes a pointer to a
				     character sequence that gets sent
				     to the PLL device. The first byte there
				     contains the byte count for the following
				     bytes. In firmware mode, the text stream
				     follows the usb identifier. */
#define _AltRunMode         16   /* like RunMode, but with alt run bit set */
#define _ForceAltRun        17   /* like ForceRun, but with alt run bit set */
#define _WriteParameters    18   /* takes a few bytes of parameters written
				   to the mode registers of the CPLD */
#define _ResetCPLD          19   /* no parameters, resets the CPLD and leaves
				   system in idle state */


#ifndef IOCBASE

#ifdef firmware
#define IOCBASE 0x00 /* we stay bytewise */
#define IOCBASEW 0x00
#define IOCBASEWR 0x00
#else
#include <linux/ioctl.h>
#define IOCBASE 0xa400
#define IOCBASEW 0xa400
#define IOCBASEWR 0xa400
#endif

#endif


/* implementation of actual commands */
#define Reset_Pattern_unit     ( _Reset_Pattern_unit | IOCBASE  )
#define SendDac                ( _SendDac            | IOCBASEW )
#define InitDac                ( _InitDac            | IOCBASE )
#define InitializeRFSRC        ( _InitializeRFSRC    | IOCBASE )
#define Rf_Reference           ( _Rf_Reference       | IOCBASEW )
#define Send_RF_parameter      ( _Send_RF_parameter  | IOCBASEW )
#define RunMode                ( _RunMode            | IOCBASE )
#define IdleMode               ( _IdleMode           | IOCBASE )
#define PatternRAM_lseek       ( _PatternRAM_lseek   | IOCBASEW )
#define ProgMode               ( _ProgMode           | IOCBASE )
#define ForceIdle              ( _ForceIdle          | IOCBASE )
#define ForceRun               ( _ForceRun           | IOCBASE )
#define Send_AUXRF_parameter   ( _Send_AUXRF_parameter | IOCBASEW )
#define RequestStatus          ( _RequestStatus      | IOCBASEWR )
#define SubmitPLLtext          ( _SubmitPLLtext      | IOCBASEW )
#define ReadPLLtext            ( _ReadPLLtext        | IOCBASEWR )
#define AltRunMode             ( _AltRunMode         | IOCBASE )
#define ForceAltRun            ( _ForceAltRun        | IOCBASE )
#define WriteParameters        ( _WriteParameters    | IOCBASEW )
#define ResetCPLD              ( _ResetCPLD          | IOCBASE )


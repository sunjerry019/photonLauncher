/* definitions of ioctl commands for the usb-co16 adapter execuded by 
   the firmware with EP1 commands; will also be used as ioctls where
   possible for the USB driver calls 
*/

#define  _Reset_Hardware      1    /* needs no argument */
#define  _SendDac             2    /* takes a 16bit value as argument */
#define  _InitDac             3    /* initialize DAC, no args  */
#define  _Set_PortA           4    /* takes a one byte argument */
#define  _Readback_PortA      5    /* takes no argument but returns a byte */
#define  _Set_Inhibitline     7    /* switch off data taking. Also resets timer */ 
#define  _Reset_Inhibitline   8    /* allow data taking. no args */
#define  _Set_MasterReset     9    /* set MR (i.e. disables it) */
#define  _Clear_MasterReset   10   /* clear MR (i.e., resets hardware) */
#define  _Initialize_FIFO     11   /* clears EZ internal FIFO */
#define  _Stop_nicely         12   /* switches off the GPIF cleanly */
#define  _Autoflush           13   /* allow submission of urbs after a 
				     define multiples of 10 msec */
#define  _StartTransfer       14   /* start GPIF engine */
#define  _ManualFlush         15   /* committ last packet by hand */
#define  _RequestStatus       16   /* requests either status info, or one of
				     the descriptor packets at EP1 in. Used
				     for checking the emptyness of FIFOs */
#define  _Timed_Inhibit       17   /* takes 16 bit argument (or more?) to set
				     a timer on for a multiple of 10
				     milliseconds, then disables the inhibit
				     line, until the time is elapsed. */
#define  _TimeToGo            18   /* returns the time in msec the internal
				     timer still has to go */
#define  _GetVersion          19   /* returns the version number of the
				      firmware / card. For later extension to
				      more commands if everything is on one
				      card. */


// needs to be fixed.
/* internal commands for the driver to handle the host driver aspects */
#define  _Start_USB_machine   100  /* prepare DMA setup */
#define  _Stop_USB_machine    101  /* end data acquisition */
#define  _Get_transferredbytes 102 /* how many bytes have been transferred */
#define  _Reset_Buffering     103  /* give local buffer a restart */
#define  _Get_errstat         104  /* read urb error status */


/* The following is an attempt to make the ioctl commands compliant to the
   recommendation for ioctl numbers in a linux system and maintain the one-byte
   size for commands sent over the USB channel since it appears that the
   single byte ioctls get swallowed by the OS otherwise. So for now, the
   header file does need to be preceeded by a compiler statement to define
   "firmware" if the header file is used to generate firmware code. */

#ifdef firmware
#define IOCBASE 0x00 /* we stay bytewise */
#define IOCBASEW 0x00
#define IOCBASER 0x00
#define IOCBASEWR 0x00
#else
#include <linux/ioctl.h>
#define IOCBASE 0xab00
#define IOCBASER 0x8000ab00
#define IOCBASEW 0x4000ab00
#define IOCBASEWR 0xc000ab00
#endif

#define  Reset_Hardware      ( _Reset_Hardware | IOCBASE )
#define  SendDac             ( _SendDac | IOCBASEW )
#define  InitDac             ( _InitDac | IOCBASE )
#define  Set_PortA           ( _Set_PortA | IOCBASEW )
#define  Readback_PortA      ( _Readback_PortA | IOCBASER )
#define  Set_Inhibitline     ( _Set_Inhibitline | IOCBASE )
#define  Reset_Inhibitline   ( _Reset_Inhibitline | IOCBASE )
#define  Set_MasterReset     ( _Set_MasterReset | IOCBASE )
#define  Clear_MasterReset   ( _Clear_MasterReset | IOCBASE )
#define  Initialize_FIFO     ( _Initialize_FIFO | IOCBASE )
#define  Stop_nicely         ( _Stop_nicely | IOCBASE )
#define  Autoflush           ( _Autoflush | IOCBASEW )
#define  StartTransfer       ( _StartTransfer | IOCBASE )
#define  ManualFlush         ( _ManualFlush | IOCBASE )
#define  RequestStatus       ( _RequestStatus | IOCBASEWR )
#define  Timed_Inhibit       ( _Timed_Inhibit | IOCBASEW )
#define  TimeToGo            ( _TimeToGo | IOCBASER )
#define  GetVersion          ( _GetVersion | IOCBASER )


// needs to be fixed.
/* internal commands for the driver to handle the host driver aspects */
#define  Start_USB_machine   ( _Start_USB_machine | IOCBASE )
#define  Stop_USB_machine    ( _Stop_USB_machine | IOCBASE )
#define  Get_transferredbytes ( _Get_transferredbytes | IOCBASER )
#define  Reset_Buffering     ( _Reset_Buffering | IOCBASE )
#define  Get_errstat         ( _Get_errstat | IOCBASER )

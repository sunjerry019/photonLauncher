/* ioctl() definitions for the digital output card. Both used for communication
   with the firmware on the EP1 interface, and (for the larger values) to 
   communicate with the host side driver */

#define  Reset_Pattern_unit  1   /* prepare clean state of the device; 
				    details TBD */
#define Set_Timer            3   /* Set internal timer register, sets PA7 clock
				    output. The periode is defined as a 16 bit
				    parameter y, which translates into a periode
				    of the output via 
				    periode = (0xffff - y ) * 2 microseconds.
				    The ioctl takes an integer argument for y */

#define Start_Transfer       4   /* enable transfer */
#define Stop_Transfer        5   /* End transfer */
#define Port_Pattern         6   /* 16bit wide port pattern which is shown
				    to the output lines if no GPIF transfer is
				    active */
#define Wordwide_Output      7   /* switch output mode to wordwide */
#define Bytewide_Output      8   /* switch output mode to bytewide output */
#define RequestStatus        99   /* request status for debugging 
				     10: return GPIFTCNT */

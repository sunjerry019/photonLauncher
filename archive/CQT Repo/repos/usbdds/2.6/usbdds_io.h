/* !!!Code in transit to entertain firmware version 2.0.0 onwards with the 
   Listplay option. start of migration: 13.12.09chk

ioctl() and USB firmware command definitions for the DDS. This is for
   firmware version 0.2.0 onwards, and usb driver version 0.1.0 onwards.

   These definitions are both used for communication
   with the firmware on the EP1 interface, and (for the larger values) to 
   communicate with the host side driver from user space. For the USB interface,
   these commands are sent via EP1 to the device with the following format:

   byte 0: length <n> of message in bytes, including the checksum
   byte 1: command token. These are the definitions listed below.
   byte 2 to <n-2>: data bytes.
   byte <n-1>: checksum. This is a sum over all <n-1> previous bytes mod 0xff.

   The ioctl() versions sometimes take a 32 bit parameter; read commands come
   directly back in form of a return value.

   consolidated version 21.9.09 chk
*/

#define  _Reset_DDS_unit     1    /* prepare clean state of the device; 
	 			     details TBD */
#define  _WriteDisplay       2    /* takes a null-terinated string internally,
				     will be mapped to a write command on the
				     higher level. In usbcore->device communic,
				     the data goes straight to the display,
				     following the mepty space parsing rules
				     also implemented for the ATMEL MCUs. */
#define _Start_Transfer      3    /* allow for EP2 packet transfers to the
				     DDS */
#define _Stop_Transfer       4    /* end EP2 packet transfers to the DDS */
#define _IOupdate_off        5    /* Writes to the DDS are performed without
				     a IOUPDATE at the end */
#define _IOupdate_on         6    /* Writes to the DDS are performed with
				     a IOUPDATE at the end; this is the
				     initial state of the firmware */
#define _SendDirectStream    7    /* This is the command for sending a direct
				     stream to the DDS via the EP1 interface;
				     not sure at the moment how a ioctl
				     command maps to that purpose easily. */
#define _Full_DDS_Reset      8    /* carries out a master reset on the DDS
				     chip as command number 1, but also prepares
				     the chip into the nibble-transport mode
				     such that consequent byte loading can take
				     place with 8 bit wide words. It also
				     switches on the EP2 transfer mode so
				     command uploading could take place without
				     any ioctl involvement by piping a command
				     file into the device node. This will be
				     the default restart mode of the device.*/
#define _IOUpdate_regular   9     /* Switches to a waveform that updates every
				     n bytes with n=1..128 and a pause of m
				     sync clock cycles with m=1..255. The
				     parameters n and m are bytes passes in
				     sequence n,m after the EP1 command byte,
				     or as a 16 bit value in an ioctl command.*/
#define _IOUpdate_reg_trig  10    /* Same as IOUpdate_regular, but uses input
				     line 3 as a trigger (need to check) */


#define _ListplayMode       11    /* sets the transfer mode for list operation.
                                     takes a one byte parameter, which defines
                                     after how many hardware signals the thing
				     should start. puts the list write pointer
				     to zero, and the read pointer as well.
				     From this command onwards, EP2 writes end
				     up in the playlist RAM. The GPIF engine is
				     passive, and needs to be activated with
				     the ActivateListplayMode command */
#define _StartListplayMode  12    /* Switch on the update list mode. This
				     starts the table at the beginning */
#define _ListplayLseek      13    /* goto a particular location of the list,
				     determined by a 16 bit parameter
				     indicating the list index for the next
				     output. The byte position is given by the
				     argument of this call times the listmode
				     chunk length. Not sure yet if needed. */
#define _StopListplayMode   14    /* Halt the lis mode operation; this
				     deactivates the GPIF engine, but leaves
				     the list pointer where it was. (not sure
				     if this can be maintained. */

#define _WriteClockchip     15    /* sends a number of bytes to the clockchip.
				     Format: The command byte is followed by 
				     a two-byte length argument (lsb first, msb
				     set to zero), then by length data bytes.
				     the first byte contains will be the first
				     SPI command byte, including write index
				     and transfer type.  The kernel interface
				     is given a pointer to a buffer that
				     contains at least 4 bytes, starting 
				     with length argument. */

#define _ReadClockchip      16    /* reads  back something from the clockchip.
				     To the usb device, a six byte message is
				     sent, with the length argument in pos. 2,3
				     encoding the number of bytes to be read.
				     Bytes 4,5 of the usb message contain the
				     read address command. The usb device
				     returns the the cmd word, plus the data
				     read from the device. The kernel interface
				     is given a pointer to a buffer that
				     contains 4 bytes, starting with length.
				     On return, it contains the response of
				     the device, plus the command sent to it.
				  */



#define _RequestStatus       99   /* request status. Acts as an initiator for
				     an EP1 readback command. */


/* For the firmware, the following definitions specify the readback value in the
   next EP1in command via the RequestStatus command. For higher level drivers,
   it specifies the ioctl() command, which returns the value directly. */
  
#define _Get_Firmware_Version 100 /* returns a the firmware version as a 32bit
				     value, with the following bit encoding:
				        <31:24>: Firmware version
				        <23:16>: Revision level
					<15:0>: Patchlevel or svn status */
#define _Get_Board_Version   101  /* returns a 32 bit board specification,
				     with the following bit encoding:
				        <31:24>: Board version
					<23:16>: Board revision level
					<15:8>: board configuration
					<7:0>:  subrevision/patchlevel */
#define _Get_Base_Chip       102 /* returns a 32 bit number with the main chip
				    numerical base code. */
#define _Get_Reference_Freq  103 /* returns a 32 bit number with the reference
				    frequency supplied to the chip, in Hz. */
#define _Get_Serial_Number   104 /* returns a 32 bit serial number of the
				    board. */
#define _Get_Amplitudes      105 /* returns reference amplitudes for both
				    channels in millivolt. bits <31:16> are
				    for channel 1, bis <15:0> for channel 0 */


/* Here are transitional comands sent to the firmware, mostly for debugging at
   the moment. Don't rely on a stable set of definitions for now. */

#define _Get_Buffer_writeindex 106
#define _Get_Buffer_readindex  107
#define _Get_Buffer_bytecount  108
#define _Get_Buffer_content    109

#define Largest_Readback_number 109

/* There should be a series of simple commands to set various DDS parameters.
   This is not implemented, since it is not clear how to structure a reasonably
   versatile and useful high-level interface.
 */


/* These are ioctl() definitions for the basic linux USB driver which are not
   handled by the firmware in any significant way; they are here anyways to
   make sure that there are not too many header files floating around */
#define _Get_Driver_Version  1000 /* Used to retreive a 32 bit number for the
				     driver version with the bit encoding:
				       <31:24> version number
				       <23:16> revision number
				       <15:0>  patch level/svn code. */
#define _Read_EP1_8bit       2000 /* ioctl() command to retreive a one-byte
				     return value from an EP1 readback */
#define _Read_EP1_32bit      2004 /* ioclt() command to retrieve a 4-byte
				     return value from a EP1in readback */


/* For debugging ONLY, don't rely on these things to be stable */
#define _Write_Dummybuf_To_EP2 2005 /* write driver-internal buffer to EP2; the
				       transfer size is given by ioctl arg */
#define _Write_Dummybuf_Byte   3000 /* argument is (adr & 0x3ff)<<8 + value */
#define _Read_Dummybuf_Byte    3001 /* arg is (adr & 0x3ff)<<8 */
#define _Write_Dummybuf_To_EP1 3002 /* send dummy buf content to EP1out; arg
				       is the size in bytes. */

#ifdef firmware
#define IOCBASE 0x00 /* we stay bytewise */
#define IOCBASEW 0x00
#define IOCBASEWR 0x00
#else
#include <linux/ioctl.h>
/* the offset 0xa000 is used to avoid problems with low number ioctls I have
   see on several machines. No idea what the reason is... */
#define IOCBASE 0xa000
#define IOCBASEW 0xa000
#define IOCBASEWR 0xa000
#endif

/* here goes the definition for the ioctls that work both with firmware
   and device driver. */

#define Reset_DDS_unit          ( _Reset_DDS_unit        | IOCBASE     )
#define WriteDisplay            ( _WriteDisplay          | IOCBASEW    )
#define Start_Transfer          ( _Start_Transfer        | IOCBASE     )
#define Stop_Transfer           ( _Stop_Transfer         | IOCBASE     )
#define IOupdate_off            ( _IOupdate_off          | IOCBASE     )
#define IOupdate_on             ( _IOupdate_on           | IOCBASE     )
#define SendDirectStream        ( _SendDirectStream      | IOCBASEW    )
#define Full_DDS_Reset          ( _Full_DDS_Reset        | IOCBASE     )
#define IOUpdate_regular        ( _IOUpdate_regular      | IOCBASE     )
#define IOUpdate_reg_trig       ( _IOUpdate_reg_trig     | IOCBASE     )
#define ListplayMode            ( _ListplayMode          | IOCBASE     )
#define StartListplayMode       ( _StartListplayMode     | IOCBASE     )
#define ListplayLseek           ( _ListplayLseek         | IOCBASE     )
#define StopListplayMode        ( _StopListplayMode      | IOCBASE     )
#define WriteClockchip          ( _WriteClockchip        | IOCBASEW    )
#define ReadClockchip           ( _ReadClockchip         | IOCBASEWR   )
#define RequestStatus           ( _RequestStatus         | IOCBASE     )
#define Get_Firmware_Version    ( _Get_Firmware_Version  | IOCBASEWR   )
#define Get_Board_Version       ( _Get_Board_Version     | IOCBASEWR   )
#define Get_Base_Chip           ( _Get_Base_Chip         | IOCBASEWR   )
#define Get_Reference_Freq      ( _Get_Reference_Freq    | IOCBASEWR   )
#define Get_Serial_Number       ( _Get_Serial_Number     | IOCBASEWR   )
#define Get_Amplitudes          ( _Get_Amplitudes        | IOCBASEWR   )
#define Get_Buffer_writeindex   ( _Get_Buffer_writeindex | IOCBASEWR   )
#define Get_Buffer_readindex    ( _Get_Buffer_readindex  | IOCBASEWR   )
#define Get_Buffer_bytecount    ( _Get_Buffer_bytecount  | IOCBASEWR   )
#define Get_Buffer_content      ( _Get_Buffer_content    | IOCBASEWR   )


#define Get_Driver_Version      ( _Get_Driver_Version    | IOCBASEWR   )
#define Read_EP1_8bit           ( _Read_EP1_8bit         | IOCBASEWR   )
#define Read_EP1_32bit          ( _Read_EP1_32bit        | IOCBASEWR   )
#define Write_Dummybuf_To_EP2   ( _Write_Dummybuf_To_EP2 | IOCBASEW    )
#define Write_Dummybuf_Byte     ( _Write_Dummybuf_Byte   | IOCBASEW    )
#define Read_Dummybuf_Byte      ( _Read_Dummybuf_Byte    | IOCBASEWR   )
#define Write_Dummybuf_To_EP1   ( _Write_Dummybuf_To_EP1 | IOCBASEW    )

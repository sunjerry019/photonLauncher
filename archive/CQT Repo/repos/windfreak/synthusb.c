/*	This program aims to allow us to control windfreak usb synthesizer without having to use the labview GUI. Will start by trying to implement simple commands (reset, RF on/off, freq/amplitude change).
 * 	
 * Usage: synthusb [-f frequency] [-p power] [-s serial] [-o] 
 * 
 * Options:
 * -f frequency	:	set output frequency in MHz. Range=137.5MHz-4400MHz. Default resolution=1kHz.
 * -p power			:	set output power. Choose from 0-3
 * -s serial		:	provide device serial number (of part thereof) to locate correct device
 * 								Needed if there are >1 FTDI devices connected
 * -o						:	set device to power-down mode 			
 * 
 * 	We will first need to work out the 6 registers to send to the synthesizer chip (Analog Devices AD4350), then package it into a form that is correctly interpreted by the USB controller (FTDI FT245R)
 * 
 * The ftd2xx library used to communicate with the FTDI chip appears to conflict with ftdi_sio driver. If opening the device fails, check for modules ftdi_sio and usbserial using lsmod, and remove with rmmod.
 * 
 * Victor Mar2013
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include "ftd2xx.h"


#define MAX_DEVICES 20
#define BUF_SIZE 414 //length of total instruction
#define DEV_SERIAL_SEARCH ""
#define BAUD_RATE 300
//default settings. not all settings implemented...
#define RF_MHZ 201.45
#define PHASE 1
#define RF_OUT_PWR 3
#define RF_OUT_EN 1
#define AUX_OUT_EN 0
#define REF_DIVIDER 5
#define AUX_OUT_PWR 0
#define AUX_OUT_SEL 0
#define REF_MHZ 10.0
#define LOW_NOISE 1
#define MUX_OUT 6
#define PWR_DOWN 0
#define REF_DIV2 0
#define REF_X2 0
#define FPFD_MHZ REF_MHZ/REF_DIVIDER
#define DBL_BUFF 1
#define ICP 0xF
#define MUTE_TILL_LD 0
#define BAND_SEL_DIV 140

char *errormessage[]={
	"No error",
	"Error parsing frequency",	// 1 //
	"Frequency out of range (137.5-4400MHz)",
	"Error parsing RF power",
	"RF power out of range (0-3)",
	"Error parsing device serial search string", // 5 //
	"Error listing FTDI devices",
	"Error: no suitable device found",
	"Error reseting device",
	"Error setting data characteristics",
	"Error setting flow control", // 10 //
	"Error setting baud rate",
	"Error setting bit mode",
	"Error setting DTR signal",
	"Error setting RTS signal",
	"Error writing to device",	// 15 //
};

int emsg(int a){
	fprintf(stderr, "%s\n",errormessage[a]);
	return a;
}

int main(int argc, char *argv[]){
	
	//UCHAR BitMode;
	unsigned char writeBuffer[BUF_SIZE + 1];
	char * 	pcBufLD[MAX_DEVICES + 1];
	char 	cBufLD[MAX_DEVICES][64];
	DWORD dwBytesWritten;
	FT_STATUS	ftStatus;
	FT_HANDLE	ftHandle;
	int	iNumDevs = 0;
	int	i, j, bufCounter,LE,LED;
	int dev_found=0,dev_index=0;
	int data,clock;
	unsigned int reg[6];
	int Int=0, Mod=0, RF_div=0, RF_div_bin;
	long long int Frac=0;
	double x=0.0, vco_freq=0.0;
	//GetOpt variables
	int opt,opterr;
	double rf_mhz=RF_MHZ;
	int pwr_down=PWR_DOWN, rf_out_pwr=RF_OUT_PWR;
	char dev_serial_search[100]=DEV_SERIAL_SEARCH;
	
	//Parse input parameters
	opterr=0; /*be quiet when there are no options*/
	while((opt=getopt(argc,argv,"f:p:s:o")) != EOF){
		switch (opt){
			case 'f': //set frequency in MHz
				if(sscanf(optarg,"%lf",&rf_mhz)!=1) return -emsg(1);
				if(rf_mhz<137.5 || rf_mhz>4400.0) return -emsg(2);
				break;
			case 'p': //set RF power (0-3)
				if(sscanf(optarg,"%d",&rf_out_pwr)!=1) return -emsg(3);
				if(rf_out_pwr<0 || rf_out_pwr>3) return -emsg(4);
				break;
			case 's': //set device serial to search for correct device
				if(sscanf(optarg,"%99s",dev_serial_search)!=1) return -emsg(5);
				dev_serial_search[99]=0; //close string
				break;
			case 'o': //set device to power down
				pwr_down=1;
				break;
		}
	}	
	
	//Get list of FTDI devices. Need to locate correct device. 
	//If running >1 FTDI device, supply serial number as argument.

	for(i = 0; i < MAX_DEVICES; i++) {
		pcBufLD[i] = cBufLD[i];
	}
	pcBufLD[MAX_DEVICES] = NULL;
	
	ftStatus = FT_ListDevices(pcBufLD, &iNumDevs, FT_LIST_ALL | FT_OPEN_BY_SERIAL_NUMBER);
	if(ftStatus != FT_OK) return -emsg(6);
	
	for(i = 0; ( (i <MAX_DEVICES) && (i < iNumDevs) ); i++) {
		if(strstr(cBufLD[i],dev_serial_search)!=NULL){
			dev_found=1;
			dev_index=i;
			break;
		}
		//printf("Device %d Serial Number - %s\n", i, cBufLD[i]);
	}
	if(!dev_found) return -emsg(7);
	
	//Open and initialize device
	if((ftStatus = FT_OpenEx(cBufLD[dev_index], FT_OPEN_BY_SERIAL_NUMBER, &ftHandle)) != FT_OK){
			/* 
				This can fail if the ftdi_sio driver is loaded
		 		use lsmod to check this and rmmod ftdi_sio to remove
				also rmmod usbserial
		 	*/
			printf("Error FT_OpenEx(%d), device %d\n", (int)ftStatus, i);
			printf("Use lsmod to check if ftdi_sio (and usbserial) are present.\n");
			printf("If so, unload them using rmmod, as they conflict with ftd2xx.\n");
			return (int)ftStatus;
	}
	if (ftStatus == FT_OK) printf("Opened device %s\n", cBufLD[dev_index]);
	

	/*try to reset*/
	if((ftStatus = FT_ResetDevice(ftHandle)) != FT_OK) return -emsg(8);

	//Set data characteristics
	if((ftStatus = FT_SetDataCharacteristics(ftHandle, FT_BITS_8, FT_STOP_BITS_1,FT_PARITY_NONE)) != FT_OK) return -emsg(9);
	
	//Set flow control
	if((ftStatus = FT_SetFlowControl(ftHandle, FT_FLOW_RTS_CTS, 0x11, 0x13)) != FT_OK) return -emsg(10);
	
	//Set baud rate	
	if((ftStatus = FT_SetBaudRate(ftHandle, 300)) != FT_OK) return -emsg(11);
		
	//Set bit mode
	if((ftStatus = FT_SetBitMode(ftHandle, 0x7F, 0x01)) != FT_OK) return -emsg(12);
	
	//Set "Data Terminal Ready" signal
	if((ftStatus = FT_SetDtr(ftHandle)) != FT_OK) return -emsg(13);
		
	//Set "Request to Send" signal
	if((ftStatus = FT_SetRts(ftHandle)) != FT_OK) return -emsg(14);		

	/*Start working out the registers. First calculate some values...
	 * RFout=[INT+(FRAC/MOD)]*f_pfd/RFdiv
	 * f_pfd=REFin*[(1+D)/(R*(1+T))]
	 * D:REF_x2, R=ref_divider, T=ref_div2
	 * Using default values (10MHz ref, D,T off, R=5)
	 * 
	 * RFout=[INT+(FRAC/MOD)]*2MHz/RFdiv
	 * 
	 * Chip works between 2.2-4.4GHz, so first choose divider value RFdiv 
	 * (1,2,4,8,16) to get correct INT value.
	 * Then choose MOD*RFdiv=2000 to give 1kHz step resolution.
	 * Lastly choose FRAC/MOD to get correct frequency.
	 */
	x=2200.0/rf_mhz;
	if(x<=1) RF_div_bin=0;
	else if(x<=2) RF_div_bin=1;
	else if(x<=4) RF_div_bin=2;
	else if(x<=8) RF_div_bin=3;
	else if(x<=16) RF_div_bin=4;
	RF_div=(1<<RF_div_bin);
	
	vco_freq=rf_mhz*RF_div;
	Int=(int)floor(vco_freq/(FPFD_MHZ));
	Mod=2000/RF_div;
	Frac=vco_freq*Mod/(FPFD_MHZ)-Mod*Int;
	printf("Freq=%f MHz,Int=%d,Mod=%d,Frac=%lld,RF_div=%d,RF pwr=%d\n",rf_mhz,Int,Mod,Frac,RF_div,rf_out_pwr);
	
	//Start filling out registers
	reg[0]=(Int<<15)+(Frac<<3);
	
	reg[1]=(1<<27)+(PHASE<<15)+(Mod<<3)+1;
	
	if(LOW_NOISE)reg[2]=0;
	else reg[2]=(3<<29);
	if(REF_X2)reg[2]+=(1<<25);
	if(REF_DIV2)reg[2]+=(1<<24);
	if(DBL_BUFF)reg[2]+=(1<<13);
	if(pwr_down)reg[2]+=(1<<5);
	reg[2]+=(MUX_OUT<<26)+(REF_DIVIDER<<14)+(ICP<<9)+(1<<7)+(1<<6)+2;
	
	reg[3]=0x4B3;
	
	if(MUTE_TILL_LD)reg[4]=(1<<10);
	else reg[4]=0;
	if(AUX_OUT_SEL)reg[4]+=(1<<9);
	if(AUX_OUT_EN)reg[4]+=(1<<8);
	if(RF_OUT_EN)reg[4]+=(1<<5);
	reg[4]+=(1<<23)+(RF_div_bin<<20)+(BAND_SEL_DIV<<12)+(AUX_OUT_PWR<<6)+(rf_out_pwr<<3)+4;
	
	//reg5 has 2 'reserved' pins set to 1 on AD4350 data sheet, but windfreak software doesn't...I followed data sheet
	reg[5]=0x00580005;
	
	printf("Registers 5-0: %08X,%08X,%08X,%08X,%08X,%08X\n",reg[5],reg[4],reg[3],reg[2],reg[1],reg[0]);
	
	/* Now prepare data to be written to FTDI chip
	 * 4 outputs go to AD4350 chip: 
	 * D0->LE (load enable. When high, shift register data is loaded onto correct register)
	 * D1->Clk (data is clocked into 32bit shift regsiter on CLK rising edge)
	 * D2->Serial data (the registers calculated above)
	 * D3->Shiny shiny LED.
	 * (D7 is connected to MUXout, but not used here)
	 * 
	 * Data sheet says for correct initialization we have to set registers 5-0 in descending order
	 */
	 bufCounter=0;
	 LE=0,LED=1;
	 for(i=5;i>=0;i--){
		 for(j=0;j<65;j++){
			 if(j%2==1)clock=1; //generate rising CLK edges
			 else clock=0; 
			 if((j/2)<32)data=(reg[i] >> (31-(j/2)) ) & 1; //Load most significant bit first
			 else data=0;
			 writeBuffer[bufCounter]=(LED<<3)+(data<<2)+(clock<<1)+LE;
			 //if(i==0) printf("%d\n",writeBuffer[bufCounter]);
			 bufCounter++;
		 }
		 writeBuffer[bufCounter]=0b00001000;bufCounter++;
		 writeBuffer[bufCounter]=0b00001001;bufCounter++;
		 writeBuffer[bufCounter]=0b00001001;bufCounter++;
		 writeBuffer[bufCounter]=0b00000000;bufCounter++;
		 
	 }
	//Write data to device
	ftStatus = FT_Write(ftHandle, writeBuffer, BUF_SIZE, &dwBytesWritten);
	if(ftStatus == FT_OK) printf("Written %d bytes\n",dwBytesWritten);
	else return -emsg(15);
	
	/*ftStatus = FT_GetBitMode(ftHandle, &BitMode);
	if(ftStatus == FT_OK) printf("%X\n",BitMode);*/
	
	if(pwr_down) printf("Device set to power down\n");
	//Cleanup
	FT_Close(ftHandle);
	printf("Closed device %s\n",cBufLD[dev_index]);
	return 0;
}

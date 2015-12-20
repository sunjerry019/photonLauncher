/* structure definition for bitchains used for CPLD and FPGA programming
   via JTAG.

*/
#define MAXCHAINBYTES 2000
typedef struct bit_chain {
  int length; 
  char content[MAXCHAINBYTES];
} bitchain;

/* function declarations */
int send_cmdonly(int handle, int command);
int send_dataonly(int handle, int data);
int sendreceive_32(int handle, int command, 
		   uint32_t in, uint32_t out, uint32_t mask);
int JTAG_init(int handle);
int Set_ENDDR(int handle, int state);
int Set_ENDIR(int handle, int state);
int Go_State(int handle, int state);
int runtest(int handle, int state, int clocks, double mintime);
int send_8(int handle, int command, int data);
int send_16(int handle, int command, int data);
int send_24(int handle, int command, int data);
int Bscan_208(int handle, int command);
int Bypasstest(int handle);
int LSC_Busy_test(int handle);
int send_128bit(int handle, int command, unsigned char *data);
int verify_128bit(int handle, unsigned char *data);
int send_64bit(int handle, int command, unsigned char *data);
int verify_64bit(int handle, unsigned char *data);
int verify_16(int handle, int in, int out, int mask);

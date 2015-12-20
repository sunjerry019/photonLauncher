/* program to talk to serial line with 115200 baud, 8 bits, 1 stop, no parity

   usage:
   getresponse [-B baudrate] 
               [-d devicefile ]
               [-t timeout] [ -n]
	       [-s | text]
	       [-X]

   options:
   -B baudrate     selects a baud rate. not all are implemented yet since
                   I am lazy 

   -d devicename   device name of the serial interface; default is /dev/ttyUSB0

   -t timeout:     sets the timeout of the device for any call in milliseconds

   -n:             no text requested

   -c:             Replace commas in the command text by white spaces.

   -s:             command is not provided following the options, but read from
                   stdin. This is necessary if a command contains space
		   characters, since with them the command parsing option with
		   getopt() fails. In this case, just echo the text into stdin
		   of the program.

   -X:             disable xon/xoff handshake

   Sends text to a serial interface (default currently: /dev/ttyUSB0)
   and waits for responsea , terminated with \r. At the moment, it implements
   XON/XOFF handshake for both input and output, but no hardware handshake.
   See myterm flags below for details.

   There is a problem with reading in commands that do contain empty spaces,
   since this breaks the parsing of options with getopt. The way our of this
   is to provide the command via stdin (and leave the text following the
   arguments away). Alternatively, the -c option can be used. When invoked,
   all commas are replaced by white spaces.

*/

#include <termios.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <string.h>

#include <unistd.h>



#define DEFAULT_TIMEOUT 3 /* timeout in seconds */
#define DEFAULTDEVICENAME "/dev/ttyUSB0"
#define DEFAULTBAUDRATE 9600

#define LOC_BUFSIZ 1000
#define FNAMELENGTH 200      /* length of file name buffers */
#define FNAMFORMAT "%200s"   /* for sscanf of filenames */
#define CMDLENGTH 500        /* command */

#define BAUDNUM 8
int baudlist[BAUDNUM] = {50, 300, 1200, 2400, 4800, 9600, 19200, 115200};
speed_t baudflag[BAUDNUM] = {B50, B300, B1200, B2400, B4800, B9600, B19200, B115200};

/* error handling */
char *errormessage[] = {
    "No error.",
    "Missing command string", /* 1 */
    "Error opening device file",
    "cannot parse baud rate",
    "illegal baud rate", 
    "error in select call", /* 5 */
    "timeout while waiting for response",
    "illegal timeout value",
};
int emsg(int code) {
    fprintf(stderr,"%s\n",errormessage[code]);
    return code;
};

/* timeout stuff */
struct timeval timout = {DEFAULT_TIMEOUT,0}; /* default timeout  */

char cntrl[2]={27,')'};

int main(int argc, char *argv[]){
    int opt; /* option parsing */
    int fh;  /* device file handle */
    int cnt;    struct termios myterm;
    fd_set fds;   /* file descriptors for select call */
    int maxhandle;
    char buf2[LOC_BUFSIZ];  /* input buffer */
    int i, n, retval;
    char command[CMDLENGTH];  /* command line to be read in */
    char devicefilename[FNAMELENGTH] = DEFAULTDEVICENAME;
    int baudrate = DEFAULTBAUDRATE; 
    int baudindex;
    int notextoption = 0;
    int stdinoption=0;
    int commaoption=0;
    int disableflowcont=0;

    /* parse option(s) */
    opterr=0; /* be quiet when there are no options */
    while ((opt=getopt(argc, argv, "B:d:t:nsX")) != EOF) {
	switch (opt) {
	    case 'B': /* choose baudrate */
		if (1!=sscanf(optarg,"%i",&baudrate)) return -emsg(3);
		break;
	    case 'd': /* parse device file */
		if (1!=sscanf(optarg,FNAMFORMAT,devicefilename)) return -emsg(2);
		break;
	    case 't': /* timeout */
		if (1!=sscanf(optarg,"%i",&i)) return -emsg(2);
		if (i<0) return -emsg(7);
		timout.tv_sec = i/1000;
		timout.tv_usec = (i%1000)*1000;
		break;
	    case 'n': /* no text option */
		notextoption=1;
		break;
	    case 's': /* read text from stdin */
	      stdinoption=1;
	      break;
	    case 'c': /* replace commas by whitespace */
	      commaoption=1;
	      break;
	    case 'X': /* disable xon/xoff */
	      disableflowcont=1;
	      break;
	}
    }
    
    /* generate baud index */
    for (baudindex=0;baudindex<BAUDNUM;baudindex++) 
	if (baudlist[baudindex]==baudrate) break;

    if (baudindex==BAUDNUM) return -emsg(4);

    /* parse command */
    if ((argc!=optind+1) || stdinoption) { /* get argument from stdin */
      if (1!=fscanf(stdin, "%490s", command)) 
	return -emsg(1); /* no commans string */;
    } else {
      sscanf(argv[optind],"%490s",command);
    }

    if (commaoption) {
      i=0;
      while(command[i]) {
	if (command[i]==',') command[i]=' ';
	i++;
      }
    }
 
    n=strlen(command);
    command[n]='\r';command[n+1]='\n';
    command[n+2]=0;   /* create return at the end */
    
    /* open device */
    fh=open(devicefilename,O_NOCTTY|O_RDWR);
    if (fh==-1) return -emsg(2);
    
    maxhandle=fh+1;  /* for select call */
    
    setbuf(stdin,NULL);
    
    /* set terminal parameters */
    cfmakeraw(&myterm);
    myterm.c_iflag = (myterm.c_iflag & ~ICANON)|IGNBRK|IXANY;
    if (disableflowcont==0)  myterm.c_iflag |= IXON|IXOFF;
    myterm.c_oflag = (myterm.c_oflag );
    /* mental note to whenever this is read: disabling the CRTSCTS flag
       made the random storage of the send data go away, and transmit
       data after a write immediately.... */
    myterm.c_cflag = (myterm.c_cflag & ~CRTSCTS)|CLOCAL|CREAD|HUPCL;
    
    cfsetospeed(&myterm, baudflag[baudindex]);
    cfsetispeed(&myterm, baudflag[baudindex]);
      
    tcsetattr(fh,TCSANOW, &myterm);
    
    tcflush(fh,TCIOFLUSH); /* empty buffers */

    /* send command */
    write(fh,command,strlen(command));

    
    if (notextoption) return 0; /* we are done here */
    
    for(;;) {
	FD_ZERO(&fds);
	FD_SET(fh,&fds); /* watch for stuff from serial */
	retval = select(maxhandle,&fds,NULL, NULL, &timout);
	if (retval<0) return -emsg(5);
	if (retval==0) return -emsg(6);

	
	/* serial->stdout handler */
	if (FD_ISSET(fh,&fds)) {
	    cnt=read(fh, &buf2,sizeof(buf2));
	    if (cnt<0) break;
	    if (cnt==0) {
		continue;
	    } else {
		fwrite(&buf2,sizeof(char),cnt,stdout);
		if (buf2[cnt-1] == '\n') return 0;
	    };
	};
	
	
    };

    fprintf(stdout,"\n");
    close(fh);
    return 0;
}

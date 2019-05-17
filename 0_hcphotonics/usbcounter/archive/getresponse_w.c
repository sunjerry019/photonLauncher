/* program to talk to serial line with 9600 baud, 8 bits, 1 stop, no parity

   usage:
   getresponse text

   sends text to ttyUSB0 and waits for response, terminated with \r

   the input is processed such that all commas are replaced by spaces.

   This is a modified version, which has a built in timeout of 1 second.
   That time can be modified with the constant DEFAULT_TIMEOUT chk310108

*/

#include <termios.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <string.h>

#define LOC_BUFSIZ 1000
#define SERIALDEVICE "/dev/ttyUSB0"

#define oldseparator ','
#define newseparator ' '

/* timeout in seconds */
#define DEFAULT_TIMEOUT 3

int main(int argc, char *argv[]){
  int fh;
  int cnt;
  struct termios myterm;
  fd_set fds;   /* file descriptors for select call */
  int maxhandle;
  char buf2[LOC_BUFSIZ];  /* input buffer */
  int x,n,i;
  int accnt=0;
  char command[500];
  struct timeval timeout; /* for storing the timeout in the select call */
  int retval; 


  /* parse command */
  if (argc!=2) {
    fprintf(stderr, "wrong no of args.\n");
    return -1;
  }
  sscanf(argv[1],"%490s",command);
  n=strlen(command);
  command[n]='\n';command[n+1]=0;  /* create return at the end */
 
  /* open device */
  fh=open(SERIALDEVICE,O_NOCTTY|O_RDWR|O_NDELAY);
 
  maxhandle=fh+1;  /* for select call */

  setbuf(stdin,NULL);

  /* set terminal parameters */
  cfmakeraw(&myterm);
  myterm.c_iflag = (myterm.c_iflag )|IGNBRK|IXON|IXANY|IXOFF;
  myterm.c_oflag = (myterm.c_oflag );
  myterm.c_cflag = (myterm.c_cflag )|CLOCAL|CREAD|HUPCL;

  cfsetospeed(&myterm,B9600);

  tcsetattr(fh,TCSANOW, &myterm);

  /* send command */
  write(fh,command,strlen(command));
  tcflush(fh,TCIFLUSH);
  tcdrain(fh);

  for(;;) {
    timeout.tv_sec=DEFAULT_TIMEOUT; timeout.tv_usec=0; /* set timeout */
    FD_ZERO(&fds);
    FD_SET(fh,&fds); /* watch for stuff from serial */
    retval=select(maxhandle,&fds,NULL,NULL,&timeout);
   
      return 0;
    }
    x=1*(FD_ISSET(0,&fds) !=0) + 2*(FD_ISSET(fh,&fds) !=0);
    accnt++;
    
    /* serial->stdout handler */
    if (FD_ISSET(fh,&fds)) {
      cnt=read(fh, &buf2,sizeof(buf2));
      if (cnt<0) break;
      if (cnt==0) {
	  continue;
      } else {
	  for (i=0;i<cnt;i++) {
	      if (buf2[i]=='\r') buf2[i]=' ';
	      if (buf2[i]==oldseparator) buf2[i]=newseparator;	      
	  }

	  fwrite(&buf2,sizeof(char),cnt,stdout);
	  
	  if (buf2[cnt-1] == '\n') {
	  fflush(stdout);
	  return 0; 
	  }
      };
    };
    
    
  };
  
  close(fh);
  return 0;
}








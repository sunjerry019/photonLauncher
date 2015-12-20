/* generate a simple pattern */

#include <stdio.h>
#include <stdlib.h>

#define patternsize (1<<19)

unsigned int binaryToGray(unsigned int num) {
  return (num>>1) ^ num;
}

int main(int argc, char * argv[]) {
    char *patternbuf;
    int i, adr1, adr2;
    int next_adr, val,v2=0;
    patternbuf = (char *)malloc(patternsize*8);
    
    // simple loop

    for (i=0;i<patternsize  ;i++) {
	next_adr=0;
	val=0;v2=0;
	
	if (i<14) next_adr = i+1;
	
	val=i & 0xff;
	v2= (i>>8) & 0xff;
	
	//if ((i&0x7fff)==255) {next_adr=0;}
	adr1=i; //binaryToGray(i); //current address
	adr2=next_adr; //binaryToGray(next_adr); //binaryToGray(next_adr);
	

	patternbuf[adr1*8+0]=val;
	patternbuf[adr1*8+1]=v2;
	patternbuf[adr1*8+2]=adr2 & 0xff; 
	patternbuf[adr1*8+3]=(adr2 >>8) & 0xff;
	patternbuf[adr1*8+4]=(i==0?255:0);
	patternbuf[adr1*8+5]=val;
	patternbuf[adr1*8+6]= adr2 & 0xff;
	patternbuf[adr1*8+7]=((adr2 >>8) & 0x7f) | 0x80;
    }

    fwrite(patternbuf,patternsize,8,stdout);
    return 0;
}

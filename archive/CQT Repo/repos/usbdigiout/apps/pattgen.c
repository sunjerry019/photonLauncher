/* program to generate a pattern to be sent to the output; contains a
   binary file which counts up 16 bit values */

#include <stdio.h>
#include <stdint.h>

#define length 100000
int main(int argc, char *argv[]) {
    uint16_t bla[length];
    int i;
    for (i=0;i<length;i++) {
       /* for detectors in a row, each side, interleaved with zeros */
	bla[i]=~((i&1)?0:(0x11<<((i/(length/4))%4))); 
    }
    
    fwrite(bla,sizeof(uint16_t),length,stdout);
    return 0;
}



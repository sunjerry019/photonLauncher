/* program to generate a simple pattern. Feel free to modify.

program invocation:   simplepattern > targetfile.dat

The program first fills an internal memory buffer with a pattern, and then
saves it into a file. Alternatively, the pattern can be saved into the pattern
generator device directly.

Here is the pattern we to be generated. It consists of 7 steps, and should loop
after it has reached the end. The sequence starts always with step 0 (hope this
is implemented correctly in the hardware...)

step  0 1 2 3 4 5 6 7

out0  0 1 0 0 0 0 0 0

out1  0 0 1 0 1 0 1 0

speed s s s s f f f f

Here, speed indicates if the original clock rate, divided by 2 should be used
(f for fast), or the initial clock rate divided y 100 (s for slow).

We need to encode for each step the address or number of the next step. For all
but the last entry, we need to use a value i+1 for the "next address" entry of
step i.

To complete the pattern, we fill all other (unused) bits with 0, and possibly
all unused patterns with a jump to step 0 in case the reset does not work
properly.

*/
    
#include <stdio.h>
#include <stdlib.h>
    
/* This line defines the number of table entries. The device is made up of
   RAM chips with 19 address bits, therefore we have 2^19=524,288 entries: */

#define patternsize (1<<19) 
    
    
/* definition of a table entry. Each table entry consists of a word of 6 data
   bytes for the 48 output lines, and one control word (16 bit wide) which
   specifies the next address and the duration bit for this particular table
   entry.
*/  

typedef struct tableentry {
	char outbyte[6]; /* six data bytes for 48 output lines */
	unsigned short int controlword; /* a 16 bit wide control word. The
					   least significant 15 bit form the
					   address of the next table entry,
					   the most significant bit decides
					   fixes the duration divider for
					   this particular entry. If this bit
					   is set, the duration is 2 clock
					   cycles, otherwise 200 clock cycles.
					   You can use the macros FASTCLOCK and
					   SLOWCLOCK to set this bit.
					*/
} t_e;

#define FASTCLOCK 0x8000
#define SLOWCLOCK 0x0000

int main(int argc, char * argv[]) {
    struct tableentry *patternbuf; /* pointer to internal table */
    int i;  /* counting variabl */
    int export_entries; /* how many table entries are exported */

    /* first, we have to allocate the interal table space. We use calloc to
       make sure all the table is filled with zeros initially, so we only
       need to set the bits we need and can safely ignore the rest */
    patternbuf = (struct tableentry *)calloc(
	patternsize,   /* number of entries */
	sizeof(struct tableentry) /* size of one structure */
	);
    
    /* now we need to fill the first seven entries. Here, we do it in a simple
       loop to go through all entries and construct the table entry in the
       internal buffer. Since all other entries are zero, we don't need to
       worry about them.
    */
#define PATTERNLENGTH 8 /* we have entries 0 to 7 */

/* some definitions to keep the pattern generation readable */
#define OUTPUT_ZERO   1  /* bit value for first output OUT 0 */
#define INDEX_ZERO    0  /* Output 0 resides in the first out data byte */

#define OUTPUT_ONE    2  /* bit value for second output, OUT 1 */
#define INDEX_ONE     0  /* Output 1 resides in the first out data byte */


    for (i=0;i<PATTERNLENGTH  ;i++) {
	/* first, we take care of the "next address" component in the 
	   control word for table entry i: */
	if (i<7) {
	    patternbuf[i].controlword = i+1;
	} else {
	    patternbuf[i].controlword = 0; /* return to step 0 */
	}
	
	/* Here, we define the speed of each section. The high speed bit
	   needs to be set for table entries 4 to 7. We do this here by
	   logically OR with the FASTCLOCK pattern to avoid nonsense with
	   some signed/unisgned issues */
	if (i>3) patternbuf[i].controlword |= FASTCLOCK;

	/* now we define the pattern of the outputs itself. Here, it is done
	   in a very crude algorithmic way. This should be done more
	   efficiently in a more complex pattern */

	/* output 0 */
	if (i==1) patternbuf[i].outbyte[INDEX_ZERO] |= OUTPUT_ZERO;
	
        /* output 1 */
	if ((i==2) || (i==4) || (i==6)) 
	    patternbuf[i].outbyte[INDEX_ONE] |= OUTPUT_ONE;
    }
 
    /* now we just write the array to standard out. We can save the whole
       array, but also get away with only exporting the number of entries
       which contain useful infromation if they are in ordered sequence. */

    //export_entries = patternsize; /* all entries */
     export_entries = 8;   /* alternative for only 8 entries */

    fwrite(patternbuf,sizeof(struct tableentry),export_entries,stdout);

    return 0;
}

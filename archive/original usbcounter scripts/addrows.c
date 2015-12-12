/* programm to add a current counter tuple to a temporary file 

   usage: addrows num file

   The programm reads a text line from stdin, and then adds the first
   num-1 lines of the file to a buffer, which then is written back to
   the file. If the file does not exist, it is created and contains only
   the line from stdin.

   */

#include <stdio.h>

#define stringlength 200
#define maxlines 300

int main(int argc, char *argv[]){
  int lines;   /* number of lines */
  char fname[100];  /* filename */
  FILE *datafile;
  char buffer[maxlines][stringlength]; /* text buffer */
  int lineold;    /* number of lines in old file */
  char inbuffer[stringlength];  /* nput buffer */
  int i;

  if (argc!=3) return -1;
  if (sscanf(argv[1],"%d",&lines)!=1) return -2;
  if ((lines<=0)|(lines>maxlines)) return -2;
  
  if (sscanf(argv[2],"%s",fname)!=1) return -3;
  
  /* open input file for reading */
  datafile=fopen(fname,"r");
  lineold=0;
  if (datafile!=NULL) {
    do {
      if (fgets(buffer[lineold],stringlength,datafile)==NULL) break;
      lineold++;
    } while (lineold<lines);
    fclose(datafile);
  };
  
  /* read line from stdin */
  fgets(inbuffer,stringlength,stdin);

  /* reopen text file and write out buffers */
  datafile=fopen(fname,"w");
  if (datafile==NULL) return -1;
  fprintf(datafile,"%s",inbuffer); /* first line */
  for (i=0;(i<lineold)&&(i<lines-1);i++) fprintf(datafile,"%s",buffer[i]);

  fclose(datafile);
  return 0;
}






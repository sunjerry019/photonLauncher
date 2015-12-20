#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Translates raw timestamp files into something human-readable.

This is (supposed to be) a python clone of translate.c

The timestamp entries are 64 bit long. After reading in the file two 32-bit values are obtained by spliting the 64-bit entry.
The names cv= coarse value and dv= fine value are inherited from the timestamp documentaion and translate.c

We use the read command to read a 32kbyte buffer at a time.

Default output format: 
time (units of 125ps), pattern, phase pattern, delay (from prev step, units of 125ps), delay (in us)

note the pattern variable: 
pattern = 1 => input 1 
pattern = 2 => input 2
pattern = 4 => input 3 
pattern = 8 => input 4
pattern = 3 => inputs 1 and 2 fired simultaneously
"""

import sys
import numpy as np
import argparse
import struct

READSIZE=8 #8 bytes = 64 bits
INBUFSIZE=4096 #choose 32kbyte inbuffer

parser = argparse.ArgumentParser(description='Translates raw timestamp files into something human-readable.')
parser.add_argument('-i', '--infilename', default='')
parser.add_argument('-o', '--outfilename', default='')
args=parser.parse_args()

if not args.infilename:
    infile = sys.stdin
else:
    infile = open(args.infilename, 'rb')
    fd=infile.fileno()

if not args.outfilename:
    outfile = sys.stdout
else:
    outfile = open(args.outfilename, 'wb')

infile.read(READSIZE*10) #discard first few entries 

oldt1=0
delay=0
rollovercorrection= 0 
tr_cnt=0
t_cnt=0

while True:
    inbuf=infile.read(READSIZE*INBUFSIZE) #try to read 32kB buffer. is this buffering necessary/optimal?
    if not inbuf: break #EOF. hopefully.

    for index in xrange(len(inbuf)/8): #loop over no. of bytes actually read (unlike in C, fread doesn't return no. of bytes read...)
        retval=inbuf[index*8:(index+1)*8]
        cv,dv=struct.unpack('II',retval)

        t1 =  ( cv << 17 ) + ( dv >> 15 ) + rollovercorrection # time stamp of event
        pattern = dv & 0xf # which detector-information; 
        ppat = ( dv & 0x1ff0 )>>4 # some phase pattern shit; don't know the meaning

        # for the rollover detection:
        UPPERMASK  = 0x1fff000000000 #mask for identifying the 13 most significant bits in a 49 bit timing word
        # rollover every 19.5 hours: UPPERMASK * 125ps
        if(t1<oldt1):
            if (((t1 & UPPERMASK)==0) and ((oldt1 & UPPERMASK)==UPPERMASK)):
                # correct rollover */
                rollovercorrection = rollovercorrection + (1<<49)
                t1 = t1 + (1<<49); # correct also current event */
                print("rollover!! new rollover: " + str(rollovercorrection) )
            else:
                print( "time reversal!! current event t1: " + str(t1) + ", previous event oldt1: " + str(t_old) )
                trcnt += 1

        delay = t1 - oldt1 # time separation between events
        oldt1 = t1
        t_cnt += 1

        outfile.write('{:d} {:d} {:d} {:d} {:d}\n'.format(t1,pattern,ppat,delay,int(delay*125/1000000)))

outfile.write('Total Events = {:d}, Time Reversal Events = {:d}\n'.format(t_cnt,tr_cnt))
infile.close()
outfile.close()

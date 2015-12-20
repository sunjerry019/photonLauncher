#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is an attempt to create a 'clean' python version of the g2 script. 
It takes raw timestamp files and calculates the g2 between two channels.

Note the this program searches for correlationa in one direction, i.e. the channel 2 clicks after channel 1, and not vice versa. Justification: The timestamp has a deadtime of ~200ns or so. Thus even for simulataneous events, one channel is typically delayed by a few 100 ns with respect for the other, and the delay is also typically larger than the timespan during which any interesting correlations are expected.
"""

import sys
import numpy as np
import argparse
import struct
#import matplotlib.pyplot as plt
from math import *

READSIZE=8 #8 bytes = 64 bits
INBUFSIZE=4096 #choose 32kbyte inbuffer

parser = argparse.ArgumentParser(description='Performs g2 measurement from raw timestamp file.')
parser.add_argument('-i', '--infilename', default='')
parser.add_argument('-o', '--outfilename', default='')
parser.add_argument('-t', '--binwidth', default=8, help='units of 1/8 ns')
parser.add_argument('-m', '--maxbins', default=500, help='max no. of bins')
parser.add_argument('-c', '--channels', nargs=2, default=[1,2], help='specify the two patterns (e.g. -c 1 2). chan1=1,chan2=2,chan3=4,chan4=8')
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

binwidth=int(args.binwidth)
maxbins=int(args.maxbins)
chan1=int(args.channels[0])
chan2=int(args.channels[1])
maxdelay=binwidth*maxbins

infile.read(READSIZE*10) #discard first few entries 

oldt1=0
delay=0
rollovercorrection= 0 
tr_cnt=0
t_cnt=0
cnt1=0
cnt2=0
list1=[]
histo=[0]*maxbins #this stores the g2 histogram

while True:
    inbuf=infile.read(READSIZE*INBUFSIZE) #try to read 32kB buffer. is this buffering necessary/optimal?
    if not inbuf: break #EOF. hopefully.

    for index in range(len(inbuf)//8): #loop over no. of bytes actually read (unlike in C, fread doesn't return no. of bytes read...)
        retval=inbuf[index*8:(index+1)*8]
        cv,dv=struct.unpack('II',retval)

        t1 =  ( cv << 17 ) + ( dv >> 15 ) + rollovercorrection # time stamp of event
        pattern = dv & 0xf # timestamp input channel 
        ppat = ( dv & 0x1ff0 )>>4 # some phase pattern thing

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

        if (pattern==chan1): #just store
            cnt1 += 1
            list1.append(t1)

        if (pattern==chan2): #for strict g2, no need to store. just iterate through list1 and perform g2
            cnt2 += 1
            while list1:
                if (t1-list1[0]>=maxdelay): 
                    list1.pop(0) #remove entries that are too old
                else: break
            for chan1time in list1:
                delay=t1-chan1time
                histo[delay//binwidth] += 1

#Output histo
for i in range(maxbins):
    center=(i+0.5)*binwidth*0.125
    outfile.write('{:d} {:g} {:d} {:g} {:g} {:g}\n'.format(i,center,histo[i],sqrt(histo[i]),histo[i]/(cnt1+cnt2),sqrt(histo[i]/(cnt1+cnt2))))


outfile.write('#Cnt1 = {:d}, Cnt2 = {:d}, Cnt1+Cnt2 = {:d} \n'.format(cnt1,cnt2,cnt1+cnt2))
outfile.write('#Total Events = {:d}, Time Reversal Events = {:d}\n'.format(t_cnt,tr_cnt))
infile.close()
outfile.close()

#!/bin/sh

# script to mesaure amplitudes vs coarse time

GT=../gettrace
TARGETDIR=20141204-01/data
TB=$TARGETDIR/u_m1_

# create target data dir
mkdir $TARGETDIR

# go through coarse delays for normal phase
for ((i=0; i<64; i++))
do
    $GT -m 1 -n 150 -s $i >${TB}t$i
done

# go through coarse delays for inverted phase
for ((i=0; i<64; i++))
do
    $GT -m 1 -n 150 -s $i -i >${TB}i$i
done

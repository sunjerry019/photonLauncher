#!/bin/sh
# short script to display a trace

./osci2 >dataplot
gnuplot show.gnu
xv plot.png

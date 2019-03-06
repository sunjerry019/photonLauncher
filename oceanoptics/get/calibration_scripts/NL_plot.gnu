#!/usr/bin/gnuplot

# plot "data.dat" using 1:2:3 with errorbars, "data.dat" using 1:4:5 with errorbars, "data.dat" using 1:6:7 with errorbars, "data.dat" using 1:8:9 with errorbars

set term eps enhanced size 12,6
set output "plot.eps"

set title "Non-linearity of CCD"

set xlabel "Integration Time (ms)"
set ylabel "Intensity (A. U.)"

# arrays are 1-indexed
array wv[4] = [ 730.0, 674.06, 666.05, 741.90 ]

plot for [c=1:4] 'data.dat' using 1:c*2:c*2+1 with errorbars title sprintf("Wavelength = %d nm", wv[c])

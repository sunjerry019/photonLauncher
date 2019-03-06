#!/usr/bin/gnuplot

plot "data.dat" using 1:2:3 with errorbars, "data.dat" using 1:4:5 with errorbars, "data.dat" using 1:6:7 with errorbars, "data.dat" using 1:8:9 with errorbars

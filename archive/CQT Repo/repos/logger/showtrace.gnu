# script to display the power consumption. This thing generates a plot from
# data in logfiles. The result gets generated as a png file, and the script
# is intended to be invoked from a higher level perl script which generates 
# a dynamical web page, containing this image.

# Definition of core file, number of points, sampling, source directory,
# target directory etc. These parameters get set via some direct input of the
# calling script to adapt for things which should not be static in the
# gnuplot script. For testing, uncomment the appropriate lines below.
# core="AHU2"; outfilename="AHU2_1500.png"
# num=1500; evr=1; ofmt= "%m/%d\n%H:%M";
# num=10800; evr=10; ofmt= "%a\n%m/%d\n%H:%M";
# num=46000; evr=30; ofmt= "%m/%d"
# num=120000; evr=120; ofmt= "%b/%y";

# Some directory paths
# logdir="/home/chris/construction/BTUmetering/log"
# imgdir="/home/chris/construction/BTUmetering/web/img"

outfilename="last2000.eps"
srcfile="<tail -n 2000 /home/chris/log/templog"

t(x)=(x/100.0-1)/0.00390802 

# Define the output format and size of the resulting graphic
# set terminal png  medium size 640,400
set terminal postscript eps enhanced color size 20cm,16cm font "Helvetica,24"
set output outfilename

# define time format for input
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"

set multiplot
set size 1,0.9
set origin 0,0.1

# date text on this plot
# set format x ofmt
set ylabel 'Resistance'
set grid xtics ytics

# Do the actual plot
plot srcfile using 1:(t($3)) w l notitle

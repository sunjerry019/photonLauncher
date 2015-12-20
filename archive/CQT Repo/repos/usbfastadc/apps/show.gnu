# gnuplot file to print oscilloscope data

set terminal png
set output "plot.png"

plot "dataplot" using 1:2 w l notitle

set origin 0.05,0.05
set tics font ",18"
set xtics 100
set size 0.9,0.9

set xrange [400:1000]

set xlabel 'Wavelength/nm'
set ylabel 'Arbitrary Intensity /unit'

plot ".temp" u 1:2 w p ps 0.2 pt 7 lc rgb '#212121' notitle
pause 1
reread

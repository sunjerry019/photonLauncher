set term epscairo enhanced truecolor font "Helvetica,14" size 8.6cm,6cm

set output outfile

set multiplot title titletext

set style line 1 lc rgb "red" pt 7 ps 0.2
set style line 2 lc rgb "blue" pt 7 ps 0.2
set style line 3 lc rgb "black" pt 7 ps 0.2

#set xl "Time/s"
set yl "Temperature/{/Symbol \260}C"

set xl offset 0,0.3 font ",10"
set yl offset 1.2,0 font ",10"

set xtics font ",8"
set ytics font ",8"

set size 1,0.5
set origin 0,0.45

plot filename u 1:2 ls 1 notitle, filename u 1:4 ls 2 notitle

set size 1,0.5
set origin 0,0
set xl "Time/s"
set yl "Relative Humidity/%"
plot filename u 1:3 ls 3 notitle

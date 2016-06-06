file_notempty(file) = system("[ -s '".file."' ] && echo '1' || echo '0'") + 0

if( file_notempty(".temp") ) {
    set xrange [400:1000]
    set yrange [0:600000]
    set xlabel 'Wavelength/nm'
    set ylabel 'Arbitrary Intensity /unit'
    pause 0.5
    replot
    reread
} else {
    pause 0.5
    reread
}

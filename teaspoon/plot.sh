#!/bin/bash

gnuplot -e "filename='$1';outfile='$2'; titletext = '$3'" plot.gnu

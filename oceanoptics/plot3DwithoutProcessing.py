#!/bin/python3
import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar = 'f', help ="Data file to plot")
    parser.add_argument('title', metavar = 't', help = "Title of plot")
    args = parser.parse_args()

    plot(args.filename, args.title)

def plot(filename, title):
    g = Gnuplot.Gnuplot()
    g("set dgrid3d 30,30")
    g("set hidden3d")
    g("set term epscairo size 10, 7.5")
    g('set output "{}.eps"'.format(filename))
    g('set title "{}"'.format(title))
    g('set xlabel "Wavelength (nm)"')
    g('set ylabel "Time (s)"')
    g('set zlabel "Intensity (Arbitrary Units)"')
    g('plot "{}" u 1:2:3 with lines'.format(filename))

main()

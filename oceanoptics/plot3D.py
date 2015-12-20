#!/bin/python3

import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import os
import argparse
import datetime
import sys
import re
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', metavar = 'd', help ="Folder of files to be processed and plotted")
    parser.add_argument('title', metavar = 't', help = "Title of plot")
    parser.add_argument('-c', dest = 'concatOnly', action = 'store_true', help = 'Use this flag to only concat data')
    args = parser.parse_args()

    p = plot3D(args.dir, args.title, args.concatOnly)

class plot3D():
    def __init__(self, d, title, concatOnly = False):
        self.d = d
        self.title = title
        self.concat()

        if not concatOnly:
            self.plot()

    def concat(self):
        for root, dirs, files in os.walk(self.d):
            self.patt = re.compile('.txt$', re.IGNORECASE)
            sortedFiles = sorted(filter(self.patt.search, files))
            self.process(os.path.join(root, sortedFiles[0]), True)
            sortedFiles.pop(0)
            for f in sortedFiles:
                self.process(os.path.join(root, f))
            self.outFile.close()

    def process(self, datei, first = False):
        print(datei)
        with open(datei) as infile:
            start_read = None
            dt = None
            for line in infile:
                if start_read and line[:2] == ">>":
                    start_read = False
                if start_read:
                    try:
                        x = line.rstrip().split("\t")
                        x = [float(i) for i in x]
                        self.outFile.write("{}\t{}\t{}\n".format(x[0], dt.total_seconds(), x[1])) #x y z
                    except:
                        print(datei, line, x)
                if line[:5] == "Date:":
                    t = time.strptime(line.rstrip()[6:], "%a %b %d %H:%M:%S %Z %Y")
                    zeit = datetime.datetime(*t[:6])

                    if first:
                        self.firstTimestamp = zeit
                        self.outFilename = "{}_{}.dat".format(zeit.__str__(), self.title)
                        self.outFile = open(self.outFilename, "w")
                        self.outFile.write("# X\t  Y\t  Z\n")

                    dt = zeit - self.firstTimestamp
                if line[:2] == ">>":
                    start_read = True
    def plot(self):
        g = Gnuplot.Gnuplot()
        g("set term epscairo size 10, 7.5")
        g("set dgrid3d 30,30")
        g("set hidden3d")
        g('set output "{}.eps"'.format(self.outFilename[:-4]))
        g('set xlabel "Wavelength (nm)"')
        g('set ylabel "Time (s)"')
        g('set zlabel "Intensity (Arbitrary Units)"')
        g('set title "{}"'.format(self.title))
        g('splot "{}" u 1:2:3 with lines'.format(self.outFilename))
main()

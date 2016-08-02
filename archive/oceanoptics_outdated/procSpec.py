#!/bash/bin/python2
"""
Usage:

python procSpec.py [path to folder containing data files] [title of plot]

e.g. python procSpec.py greenlaser/18nov2015 "green laser"

Output: eps file inside the folder that datafiles are in, plots with error bars being the standard deviation for that data point.

This script does not plot over time, merely the spectra. The peak tracking functionality over time will be implemented in a separate script.

zy
18 Nov 2015
"""

from __future__ import division
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import argparse
import time
import os
import math

def checkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', metavar = 'd', nargs = '+', help ="Folder of files to be processed and plotted")
    parser.add_argument('title', metavar = 't', nargs = '+', help="Title of plot")
    args = parser.parse_args()
    p = procSpec(args.dir[0], args.title[0])
class procSpec():
    def __init__(self, dir, t):
        self.data = {}
        self.stats = {}
        self.yerrorbars = {}
        self.data_dir = dir
        self.title = t

        self.n = 0
        for fn in sorted(os.listdir(self.data_dir)):
            if not fn == "spectrumplot.eps":
                self.parseFile(fn)
        self.procSpec()
        self.plotSpec()
    def parseFile(self, fn):
        fp = os.path.join(self.data_dir, fn)
        with open(fp, 'rb+') as f:
            start_read = None

            for line in f:
                if start_read and line[:2] == ">>":
                    self.n += 1
                    start_read = False
                if start_read:
                    try:
                        x = line.rstrip().split("\t")
                        #print x
                        x = map(lambda z: float(z), x)
                        if not x[0] in self.stats:
                            #print "First time"
                            self.stats[x[0]] = {}
                            self.stats[x[0]]['mean'] = x[1]
                            self.stats[x[0]]['var'] = x[1] ** 2
                        else:
                            #print "\n"
                            self.stats[x[0]]['mean'] += x[1]
                            self.stats[x[0]]['var'] += x[1] ** 2
                    except:
                        print x
                if line[:2] == ">>":
                    start_read = True


    def procSpec(self):
        print "n:{}".format(self.n)
        for k in self.stats:
            try:
                self.stats[k]['mean'] /= self.n
                self.stats[k]['var'] /= self.n
                self.stats[k]['var'] -= self.stats[k]['mean']**2
                self.stats[k]['std'] = math.sqrt(self.stats[k]['var'])
            except KeyError:
                print k
        #print self.stats
    def plotSpec(self):
        tempf = '.temp'
        with open(tempf, 'wb+') as f:
            for k in self.stats:
                f.write("{}\t{}\t{}\n".format(k, self.stats[k]['mean'], self.stats[k]['std']))
        g = Gnuplot.Gnuplot()
        g('set term epscairo size 10, 7.5')
        g('set xlabel "Wavelength (nm)"')
        g('set ylabel "Arbitrary intensity"')
        g('set title "{}"'.format(self.title))
        g('set output "{}.eps"'.format(os.path.join(self.data_dir, "spectrumplot")))
        g('plot ".temp" u 1:2:3 with yerrorbars pt 7 ps 0.2 smooth unique')
        time.sleep(1)
        os.remove(tempf)

main()

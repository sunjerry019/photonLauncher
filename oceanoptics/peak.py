#!/bin/python3

"""
peak.py

Given a folder of background counts and spectrum measurements, process, for each wavelength, the mean and standard deviation. (Assumes each data point is gaussian)
Plots and then fits a given section of the spectrum to a gaussian.

~yd
2016-01-04
"""

import argparse
import numpy as np
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import os, sys
import re

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bgdir', metavar = 'bd', help ="Folder containing the bg counts")
    parser.add_argument('datadir', metavar = 'dd', help ="Folder containing interested counts")
    parser.add_argument('title', metavar = 't', help = "Title of plot")
    parser.add_argument('--start', metavar = 'ps', help = "Start of range to plot")
    parser.add_argument('--end', metavar = 'pe', help = "End of range to plot")
    args = parser.parse_args()

    if args.start is not None and args.end is not None:
        try:
            args.start = float(args.start)
            args.end = float(args.end)
        except:
            print("Error parsing the start and end wavelengths")
            sys.exit(1)
    elif args.start is not None or args.end is not None:
        print("If you provided either the start, or the end, you must provide the other wavelength too.")
        sys.exit(1)
    else:
        print("No start and end wavelength specified, script will skip plotting and fitting.")

    s = spectrum(args.bgdir, args.datadir, args.title, args.start, args.end)

class spectrum():
    def __init__(self, bgdir, datadir, title, start = None, end = None):
        self.dataraw = {}
        self.dataprocessed = {}
        self.bgdir = bgdir
        self.datadir = datadir
        self.start = min(end, start)
        self.end = max(end, start)
        self.title = title
        patt = re.compile(ur'\s+')
        self.esctitle = re.sub(patt, '_', self.title)
        self.ofname = 'collated_{}'.format(self.esctitle)
        self.ofname_cut = 'collated_{}.cut'.format(self.esctitle)

        try:
            self.bgfl = [x for x in os.listdir(self.bgdir) if x.endswith(".txt")]
            self.datfl = [x for x in os.listdir(self.datadir) if x.endswith(".txt")]
        except:
            print("Error reading from directories");
            sys.exit(1)

        print("Parsing BG")
        self.traverse("bg")
        print("Parsing readings")
        self.traverse("readings")

        self.calc()

        if self.start is not None:
            self.sieve()
            self.plot()

    def traverse(self, typ):
        if typ == "bg":
            dirpath = self.bgdir
            flist = self.bgfl
        else:
            dirpath = self.datadir
            flist = self.datfl

        for datei in flist:
            self.parse(typ, os.path.join(dirpath, datei))

    def parse(self, typ, fname):
        #typ: 0 = bg, 1 = readings
        typ = 0 if (typ == "bg") else 1

        with open(fname, 'r') as f:
            start_read = None
            for line in f:
                if start_read and line[:2] == ">>":
                    start_read = False
                if start_read:
                    try:
                        x = line.rstrip().split("\t")
                        x = [float(i) for i in x]
                        if x[0] not in self.dataraw:
                            self.dataraw[x[0]] = [[],[]]
                        self.dataraw[x[0]][typ].append(x[1])
                    except:
                        print("ignoring error in parsing: ", fname, line)
                if line[:2] == ">>":
                    start_read = True

    def calc(self):
        with open(self.ofname, 'w') as outfile:
            for wavelength in self.dataraw:
                bg = np.array(self.dataraw[wavelength][0])
                bg_e = np.std(bg, dtype=np.float64)
                bg_m = np.mean(bg, dtype=np.float64)

                cn = np.array(self.dataraw[wavelength][1])
                cn_e = np.std(cn, dtype=np.float64)
                cn_m = np.mean(cn, dtype=np.float64)

                t_m = cn_m - bg_m
                t_e = np.sqrt(bg_e**2 + cn_e**2)

                self.dataprocessed[wavelength] = [t_m, t_e]
                outfile.write("{}\t{}\t{}\n".format(wavelength, t_m, t_e))

    def sieve(self):
        #feels inefficient
        with open(self.ofname_cut, 'w') as outfile:
            for wavelength in self.dataprocessed:
                if wavelength <= self.end and wavelength >= self.start:
                    dtpt = self.dataprocessed[wavelength]
                    outfile.write("{}\t{}\t{}\n".format(wavelength, dtpt[0], dtpt[1]))

    def plot(self):
        maxWL = keywithmaxval(self.dataprocessed)
        initialGuess = {
            'amp' : self.dataprocessed[maxWL][0],
            'sigma': (self.end - self.start) / 4, #Purely arbituary 4 is selected here
            'mu' : maxWL,
            'gamma': 1
        }

        self.g = Gnuplot.Gnuplot()
        self.g("set term eps enhanced color")
        self.g("set output '{}.eps'".format(self.title))
        self.g('set title "{}"'.format(self.title))
        self.g('set xlabel "Wavelength (nm)"')
        self.g('set ylabel "Intensity (Arbitrary Units)"')
        self.g('set fit logfile "{}.fitlog"'.format(self.ofname_cut))
        self.g('set fit maxiter 1000')
        self.g('set fit limit 1e-4')
        self.g('amp={}; sigma={}; mu={}; gamma={}'.format(initialGuess['amp'], initialGuess['sigma'], initialGuess['mu'], initialGuess['gamma']))
        self.g('skewedGauss(x) = ((amp/(sigma*sqrt(2*pi))) * exp((-((x-mu)**2))/(2*(sigma**2)))) * (1 + erf((gamma*(x-mu))/(sigma*sqrt(2))))')
        self.g('fit skewedGauss(x) "{}" using 1:2:3 yerrors via amp, sigma, mu, gamma'.format(self.ofname_cut))
        self.g('plot "{}" using 1:2:3 with yerrorbars, skewedGauss(x)'.format(self.ofname_cut))

main()

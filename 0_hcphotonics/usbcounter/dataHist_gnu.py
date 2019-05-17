#This can be run in python 2 or 3
import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np
import math
import matplotlib.pyplot as plt
import os
import scipy as sp

try: input = raw_input
except NameError: pass

def main():
    parser = argparse.ArgumentParser(description="dataHist.py: Processes the data from the 2 APDs and plots the histogram with Gnuplot")
    parser.add_argument('datafile', metavar='f', help="The data file to read from ")
    parser.add_argument('title', metavar = 'title', help = "Title to be included in plot.")
    parser.add_argument('--d', metavar='detector', type=int, default=-1, help='Only plot one of the detectors (Takes values 0 or 1, defaults to -1 for both)')
    args = parser.parse_args()

    if args.d < -1 or args.d > 1:
        print("Error: Invalid detector number");
        sys.exit(1)

    h = dataHist(args.datafile, args.title, args.d)
    h.plot()

def iqr(x):
    # used to find box width.
    # Freedman-Diaconis Thumb of Rule
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 2 * iqr * len(x) ** (float(-1)/float(3))

class dataHist():
    def __init__(self, fname, title, detector):
        # init plotting stuff, get data from datafile
        self.data = [[],[]]
        self.title = title
        self.detector = detector
        self.fname = fname
        self.formatt = "eps enhanced color"
        self.xlabel = "Photon Counts"
        self.ylabel = "Frequency"
        try:
            with open(fname) as df:
                for line in df:
                    if line.strip()[0] != "#":
                        l = line.rstrip().split("\t")
                        if self.detector == -1 or self.detector == 0:
                            self.data[0].append(int(float(l[1])))
                        if self.detector == -1 or self.detector == 1:
                            self.data[1].append(int(float(l[2])))
            print("File read successfully")
        except IOError:
            print("Unable to read from file. Either file does not exist or I have no read permissions")

    def plot(self):
        self.generateFittedHist()

    def generateFittedHist(self):
        self.initPlot()
        self.bins = {}
        self.hist = {}
        self.binedges = {}
        self.plotHist = {}
        self.bin_c = {}
        self.initGuess = {}
        self.start = {}
        self.end = {}

        if self.detector == -1 or self.detector == 0:
            print("Generating Histogram for detector 0...")
            self.histogram(0)
        if self.detector == -1 or self.detector == 1:
            print("Generating Histogram for detector 1...")
            self.histogram(1)

    def histogram(self, detector):
        self.bins[detector] = int(math.ceil(math.fabs(max(self.data[detector]) - min(self.data[detector]))/float(iqr(self.data[detector]))))
        self.hist[detector], self.binedges[detector] = np.histogram(self.data[detector], self.bins[detector])
        self.plotHist[detector] = []

        try:
            for i in xrange(len(self.hist[detector])):
                c = self.binedges[detector][i] + (self.bins[detector]/2)
                self.plotHist[detector].append([c, self.hist[detector][i]])
        except NameError:
            for i in range(len(self.hist[detector])):
                c = self.binedges[detector][i] + (self.bins[detector]/2)
                self.plotHist[detector].append([c, self.hist[detector][i]])

        self.bin_c[detector] = (self.binedges[detector][:-1] + self.binedges[detector][1:])/2

        plt.plot(self.bin_c[detector], self.hist[detector])
        plt.show()
        params = input("Guess for fitting parameters (amplitude, center, sigma) and separated by spaces. \n>>").strip().split(' ')
        params = [float(i) for i in params]
        self.initGuess[detector] = {
            "amp": params[0],
            "mu": params[1],
            #"gamma": params[3],
            "sigma": params[2]
        }
        params = input("Guess for range (start, end) and separated by spaces. \n>>").strip().split(' ')
        params = [float(i) for i in params]
        self.start[detector] = min(params[0], params[1])
        self.end[detector] = max(params[0], params[1])

        self.fitplotDet(detector, self.initGuess[detector], self.start[detector], self.end[detector], self.bins[detector], self.plotHist[detector])

    def initPlot(self):
        # init gnuplot
        self.g = Gnuplot.Gnuplot()
        self.g('set term {}'.format(self.formatt))
        self.g('set xlabel "{}"'.format(self.xlabel))
        self.g('set ylabel "{}"'.format(self.ylabel))
        self.g('set style data boxes')
        self.g('set style fill transparent solid 0.5 noborder')

    def fitplotDet(self, detector, initialGuess, start, end, binwidth, hist):
        # write to file
        dataFile = "{}_det{}.histdat".format(self.fname, detector)
        with open(dataFile, 'w') as f:
            try:
                for binno in xrange(len(hist)):
                    if hist[binno][1] > 0 and hist[binno][0] < end and hist[binno][0] > start:
                        f.write("{}\t{}\t{}\n".format(hist[binno][0], hist[binno][1], math.sqrt(float(hist[binno][1]))))
            except NameError:
                for binno in range(len(hist)):
                    if hist[binno][1] > 0 and hist[binno][0] < end and hist[binno][0] > start:
                        f.write("{}\t{}\t{}\n".format(hist[binno][0], hist[binno][1], math.sqrt(float(hist[binno][1]))))

        # fit
        self.g('set fit logfile "{}_det{}.fitlog"'.format(self.fname, detector))
        self.g('set fit maxiter 1000')
        self.g('set fit limit 1e-4')
        #self.g('amp={}; sigma={}; mu={}; gamma={}'.format(initialGuess['amp'], initialGuess['sigma'], initialGuess['mu'], initialGuess['gamma']))
        #self.g('skewedGauss(x) = ((amp/(sigma*sqrt(2*pi))) * exp((-((x-mu)**2))/(2*(sigma**2)))) * (1 + erf((gamma*(x-mu))/(sigma*sqrt(2))))')
        #self.g('fit skewedGauss(x) "{}" using 1:2:3 yerrors via amp, sigma, mu, gamma'.format(dataFile))
        self.g('amp={}; sigma={}; mu={}'.format(initialGuess['amp'], initialGuess['sigma'], initialGuess['mu']))
        self.g('gauss(x) = ((amp/(sigma*sqrt(2*pi))) * exp((-((x-mu)**2))/(2*(sigma**2))))')
        self.g('fit gauss(x) "{}" using 1:2:3 yerrors via amp, sigma, mu'.format(dataFile))

        # plot
        self.g('set title "{}, detector {}"'.format(self.title, detector))
        self.g('set output "{}_det{}.eps"'.format(self.fname, detector))
        #self.g('set boxwidth {}'.format(binwidth))
        self.g('set boxwidth 0.95 relative')
        self.g('plot "{}" using 1:2:3 with boxerrorbars lc rgb"blue", gauss(x)'.format(dataFile))

main()

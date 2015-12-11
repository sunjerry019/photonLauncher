import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np
import math

def main():
    parser = argparse.ArgumentParser(description="dataHist.py: Processes the data from the 2 APDs and plots the histogram with Gnuplot")
    parser.add_argument('datafile', metavar='f', help="The data file to read from ")
    parser.add_argument('title', metavar = 'title', help = "Title to be included in plot.")
    args = parser.parse_args()
    h = dataHist(args.datafile, args.title)
    h.plot()

def iqr(x):
    # used to find box width.
    # Freedman-Diaconis rule
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 2 * iqr * len(x) ** (float(-1)/float(3))

class dataHist():
    def __init__(self, fname, title):
        # init plotting stuff, get data from datafile
        self.data = [[],[]]
        self.title = title
        self.fname = fname
        self.formatt = "eps enhanced color"
        self.xlabel = "Photon Counts"
        self.ylabel = "Frequency"
        try:
            with open(fname) as df:
                for line in df:
                    l = line.split("\n")[0].split("\t")
                    self.data[0].append(int(float(l[1])))
                    self.data[1].append(int(float(l[2])))
            print "File read successfully."
        except IOError:
            print("Unable to read from file. Either file does not exist or I have no read permissions")

    def plot(self):
        self.initPlot()
        self.generateHist()

    def generateHist(self):
        bin_n =  int(math.ceil(math.fabs(max(self.data[0]) - min(self.data[0]))/float(iqr(self.data[0]))))
        hist0, binedges0 = np.histogram(self.data[0], bin_n)
        plotHist0 = []
        for i in xrange(len(hist0)):
            plotHist0.append([binedges0[i], hist0[i]])

        bin_n =  int(math.ceil(math.fabs(max(self.data[1]) - min(self.data[1]))/float(iqr(self.data[1]))))
        hist1, binedges1 = np.histogram(self.data[1], bin_n)
        plotHist1 = []
        for i in xrange(len(hist1)):
            plotHist1.append([binedges1[i], hist1[i]])

        self.plotDet0(plotHist0)
        self.plotDet1(plotHist1)

    def initPlot(self):
        # init gnuplot
        self.g = Gnuplot.Gnuplot()
        self.g('set term {}'.format(self.formatt))
        self.g('set xlabel "{}"'.format(self.xlabel))
        self.g('set ylabel "{}"'.format(self.ylabel))
        self.g('set style data boxes')
    # there are two detectors. hard coded. :)

    def plotDet0(self, hist0):
        self.g('set title "{}, detector 0"'.format(self.title))
        self.g('set output "{}_0.eps"'.format(self.fname))
        self.g.plot(hist0)

    def plotDet1(self, hist1):
        self.g('set title "{}, detector 1"'.format(self.title))
        self.g('set output "{}_1.eps"'.format(self.fname))
        self.g.plot(hist1)

    def fit(self):
        self.g("set boxwidth binwidth")
        self.g("set table 'hist.temp'")

main()

import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np
import math
from lmfit.models import SkewedGaussianModel
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="dataHist.py: Processes the data from the 2 APDs and plots the histogram with Gnuplot")
    parser.add_argument('datafile', metavar='f', help="The data file to read from ")
    parser.add_argument('title', metavar = 'title', help = "Title to be included in plot.")
    args = parser.parse_args()
    h = dataHist(args.datafile, args.title)
    h.plot()

def iqr(x):
    # used to find box width.
    # Freedman-Diaconis Thumb of Rule
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 2 * iqr * len(x) ** (float(-1)/float(3))

def gauss(x, *p):
    A, mu, sigma, y0 = p
    #return (1./(sigma * math.sqrt(2 * math.pi))) * A *np.exp(-(x-mu)**2/(2.*sigma**2)) + y0
    return A *np.exp(-(x-mu)**2/(2.*sigma**2)) + y0


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
                    if line.strip()[0] != "#":
                        l = line.rstrip().split("\t")
                        self.data[0].append(int(float(l[1])))
                        self.data[1].append(int(float(l[2])))
            print "File read successfully."
        except IOError:
            print("Unable to read from file. Either file does not exist or I have no read permissions")

    def plot(self):
        self.generateFittedHist()

    def generateFittedHist(self):
        self.initPlot()
        bin_0 =  int(math.ceil(math.fabs(max(self.data[0]) - min(self.data[0]))/float(iqr(self.data[0]))))
        hist0, binedges0 = np.histogram(self.data[0], bin_0)
        plotHist0 = []
        for i in xrange(len(hist0)):
            plotHist0.append([binedges0[i], hist0[i]])

        bin_1 =  int(math.ceil(math.fabs(max(self.data[1]) - min(self.data[1]))/float(iqr(self.data[1]))))
        hist1, binedges1 = np.histogram(self.data[1], bin_1)
        plotHist1 = []
        for i in xrange(len(hist1)):
            plotHist1.append([binedges1[i], hist1[i]])

            f = open('.temp', 'wb+')

        self.plotDet0(plotHist0)
        self.plotDet1(plotHist1)

        bin_c0 = (binedges0[:-1] + binedges0[1:])/2
        bin_c1 = (binedges1[:-1] + binedges1[1:])/2

        for i in xrange(len(hist0)):
            f.write('{}\t{}\n'.format(bin_c0[i], hist0[i]))

        plt.plot(bin_c0, hist0)
        plt.show()
        params0 = raw_input("Guess for fitting parameters (amplitutde, center, sigma, gamma) separated by spaces. \n>>").strip().split(' ')
        model = SkewedGaussianModel()
        params = model.make_params(amplitude=params0[0], center=params0[1], sigma=params0[2], gamma=params0[3])
        result0 = model.fit(hist0, params, x=bin_c0)
        print result0.best_values
        print result0.fit_report()
        plt.plot(bin_c1, hist1)
        plt.show()
        params1 = raw_input("Guess for fitting parameters (amplitutde, center, sigma, gamma) separated by spaces. \n>>").strip().split(' ')
        model = SkewedGaussianModel()
        params = model.make_params(amplitude=params1[0], center=params1[1], sigma=params1[2], gamma=params1[3])
        result1 = model.fit(hist1, params, x=bin_c1)
        print result1.fit_report()
        f = open(os.path.join(self.fname, '..', "{}fitreport".format(self.fname)), 'w b+')
        f.write("det 0")
        for k,v in result0:
            f.write("{}:{}\n".format(k,v))
        f.write(result0.fit_report())
        f.write("det 1")
        for k,v in result1:
            f.write("{}:{}\n".format(k,v))
        f.write(result1.fit_report())

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

main()

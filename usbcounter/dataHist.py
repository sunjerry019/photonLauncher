import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np
import math
from scipy.optimize import curve_fit
from scipy.optimize import leastsq

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
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

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

        self.plotDet0(plotHist0)
        self.plotDet1(plotHist1)

        bin_c0 = (binedges0[:-1] + binedges0[1:])/2
        bin_c1 = (binedges1[:-1] + binedges1[1:])/2

        p0 = raw_input("Guesses for det 0 (look at the plot). A, mu and sigma. Space separated. \n >> ").strip().split(' ')
        p1 = raw_input("Guesses for det 1 (look at the plot). A, mu and sigma. Space separated. \n >> ").strip().split(' ')
        p0 = map(lambda x: int(x), p0)
        p1 = map(lambda x: int(x), p1)

        coeff_0, var_matrix_0 = curve_fit(gauss, bin_c0, hist0, p0 = p0)
        coeff_1, var_matrix_1 = curve_fit(gauss, bin_c1, hist1, p0 = p1)

        hist_fit_0 = gauss(bin_c0, *coeff_0)
        hist_fit_1 = gauss(bin_c1, *coeff_1)

        self.g('set title "{}, Fitted Gaussian for detector 0"'.format(self.title))
        self.g('set output "{}_fitted_0.eps"'.format(self.fname))
        self.g.plot(Gnuplot.Func('{0}*exp(-((x - {1})**2 )/(2 * {2}**2))'.format(coeff_0[0], coeff_0[1], coeff_0[2]),title = 'Fitted curve'), plotHist0)
        self.g('set title "{}, Fitted Gaussian for detector 1"'.format(self.title))
        self.g('set output "{}_fitted_1.eps"'.format(self.fname))
        self.g.plot(Gnuplot.Func('{0}*exp(-((x - {1})**2 )/(2 * {2}**2))'.format(coeff_1[0], coeff_1[1], coeff_1[2]),title = 'Fitted curve'), plotHist1)

        def residuals(a,x,y):
            return y - gauss(x, *a)
        p, cov, infodict, mesg, ier = leastsq(residuals, p0, full_output = True, args = (bin_c0, hist0))
        ssErr = (infodict['fvec']**2).sum()
        ssTot = ((hist0-hist0.mean())**2).sum()
        rsquared0 = 1-(ssErr/ssTot )

        p, cov, infodict, mesg, ier = leastsq(residuals, p1, full_output = True, args = (bin_c1, hist1))
        ssErr = (infodict['fvec']**2).sum()
        ssTot = ((hist0-hist0.mean())**2).sum()
        rsquared1 = 1-(ssErr/ssTot )

        with open(self.fname + '_fitlog', 'wb') as f:
            f.write("detector 0: \n")
            f.write("A: {} \nmu: {}\nsigma: {}\nR^2: {} \n\n".format(coeff_0[0], coeff_0[1], coeff_0[2], rsquared0))
            f.write("detector 1: \n")
            f.write("A: {} \nmu: {}\nsigma: {} \nR^2: {} ".format(coeff_1[0], coeff_1[1], coeff_1[2], rsquared1))

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

#This can be run in python 2 or 3
import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np
import math
import lmfit
from lmfit.models import SkewedGaussianModel
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

    def residual(self, pars, x, data=None, error=None):
        vals = pars.valuesdict()
        amp =  vals['amplitude']
        mu =  vals['center']
        sigma = vals['sigma']
        gamma = vals['gamma']

        model = ((amp/(sigma*sp.sqrt(2*np.pi))) * sp.exp((-((x-mu)**2))/(2*(sigma**2)))) * (1 + sp.special.erf((gamma*(x-mu))/(sigma*sp.sqrt(2))))

        if data is None:
            return model
        else:
            resids = model - data
            weighted = sp.sqrt(resids ** 2 / error ** 2)
            return weighted

    def generateFittedHist(self):
        self.initPlot()

        #f = open(os.path.join(self.fname, '..', "{}_fitreport".format(self.fname)), 'w b+')
        f = open("{}.fitreport".format(self.fname), 'w')

        """
        Useful links about error bars of histogram
         - http://suchideas.com/articles/maths/applied/histogram-errors/
         - http://www.science20.com/quantum_diaries_survivor/those_deceiving_error_bars-85735
         - http://arxiv.org/pdf/1112.2593v3.pdf

        These suggests that the error for the kth bin is sqrt(N_k) where N_k is the number of counts in the kth bin.

        Just to clarify, the standard deviation for a Poissonian distribution (Photon counting statistics uses Poissonian statistics) is the square root of the mean value for a bin.
        """

        if self.detector == -1 or self.detector == 0:
            bin_0 =  int(math.ceil(math.fabs(max(self.data[0]) - min(self.data[0]))/float(iqr(self.data[0]))))
            hist0, binedges0 = np.histogram(self.data[0], bin_0)
            plotHist0 = []
            try:
                for i in xrange(len(hist0)):
                    plotHist0.append([binedges0[i], hist0[i]])
            except NameError:
                for i in range(len(hist0)):
                    plotHist0.append([binedges0[i], hist0[i]])

            bin_c0 = (binedges0[:-1] + binedges0[1:])/2

            plt.plot(bin_c0, hist0)
            plt.show()
            params0 = input("Guess for fitting parameters (amplitude, center, sigma, gamma) separated by spaces. \n>>").strip().split(' ')
            params0 = [float(i) for i in params0]

            fit_params = lmfit.Parameters()
            fit_params.add('amplitude', value=params0[0])
            fit_params.add('center', value=params0[1])
            fit_params.add('sigma', value=params0[2])
            fit_params.add('gamma', value=params0[3])

            errors0 = np.array([sp.sqrt(i) for i in hist0])

            result0 = lmfit.minimize(self.residual, fit_params, args = (bin_c0, hist0, errors0))

            print("Bin size for histogram: {}\n\n".format(bin_0))
            print(lmfit.fit_report(result0))
            print(result0.success)
            print(result0.var_names)
            print(result0.covar)
            print(result0.errorbars)
            print(result0.redchi)
            print(result0.params)

            f.write("== det 0 ==\n\n")
            f.write("Bin size for histogram: {}\n\n".format(bin_0))
            for k in result0.params:
                f.write("{}:\t{}\n".format(k, result0.params[k].value))
            f.write('\n')
            f.write(lmfit.fit_report(result0))

            self.plotDet(0, plotHist0, result0.params)

        if self.detector == -1 or self.detector == 1:
            bin_1 =  int(math.ceil(math.fabs(max(self.data[1]) - min(self.data[1]))/float(iqr(self.data[1]))))
            hist1, binedges1 = np.histogram(self.data[1], bin_1)
            plotHist1 = []
            try:
                for i in xrange(len(hist1)):
                    plotHist1.append([binedges1[i], hist1[i]])
            except NameError:
                for i in range(len(hist1)):
                    plotHist1.append([binedges1[i], hist1[i]])

            bin_c1 = (binedges1[:-1] + binedges1[1:])/2

            plt.plot(bin_c1, hist1)
            plt.show()
            params1 = input("Guess for fitting parameters (amplitude, center, sigma, gamma) separated by spaces. \n>>").strip().split(' ')
            params1 = [float(i) for i in params1]

            fit_params = lmfit.Parameters()
            fit_params.add('amplitude', value=params1[0])
            fit_params.add('center', value=params1[1])
            fit_params.add('sigma', value=params1[2])
            fit_params.add('gamma', value=params1[3])

            errors1 = np.array([sp.sqrt(i) for i in hist1])

            result1 = lmfit.minimize(self.residual, fit_params, args = (bin_c1, hist1, errors1))

            print("Bin size for histogram: {}\n\n".format(bin_1))
            print(lmfit.fit_report(result1))
            print(result1.success)
            print(result1.var_names)
            print(result1.covar)
            print(result1.errorbars)
            print(result1.redchi)
            print(result1.params)

            f.write("== det 1 ==\n\n")
            f.write("Bin size for histogram: {}\n\n".format(bin_1))
            for k in result1.params:
                f.write("{}:\t{}\n".format(k, result1.params[k].value))
            f.write('\n')
            f.write(lmfit.fit_report(result1))

            self.plotDet(1, plotHist1, result1.params)

        f.close()

    def initPlot(self):
        # init gnuplot
        self.g = Gnuplot.Gnuplot()
        self.g('set term {}'.format(self.formatt))
        self.g('set xlabel "{}"'.format(self.xlabel))
        self.g('set ylabel "{}"'.format(self.ylabel))
        self.g('set style data boxes')

    def plotDet(self, detector, hist, fitresults):
        self.g('set title "{}, detector {}"'.format(self.title, detector))
	print fitresults['amplitude']
        self.g('fit_skewedgauss(x) = (({0}/({1}*sqrt(2*pi)))*exp((-((x-{2})**2))/(2*({1}**2))))*(1+erf(({3}*(x-{2}))/({1}*sqrt(2))))'.format(fitresults['amplitude'], fitresults['sigma'], fitresults['center'], fitresults['gamma']))
        self.g('set output "{}_{}.eps"'.format(self.fname, detector))
        self.g.plot(hist, "fit_skewedgauss(x)")

main()

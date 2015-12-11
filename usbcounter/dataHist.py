import argparse
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="dataHist.py: Processes the data from the 2 APDs and plots the histogram with Gnuplot")
    parser.add_argument('datafile', metavar='f', help="The data file to read from ")
    parser.add_argument('title', metavar = 'title', help = "Title to be included in plot.")
    args = parser.parse_args()
    h = dataHist(args.datafile. args.title)

def iqr(x):
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 2 * iqr * len(x) ** (float(-1)/float(3))

class dataHist():
    def __init__(self, fname, title):
        self.data = [[],[]]
        self.title = title
        self.fname = fname
        self.formatt = "eps enhanced color"
        self.xlabel = "Photon Counts"
        self.ylabel = "Frequency"
        try:
            with open(datafile) as df:
                for line in df:
                    l = line.split("\n")[0].split("\t")
                    self.data[0].append(int(l[1]))
                    self.data[1].append(int(l[2]))

        except IOError:
            print("Unable to read from file. Either file does not exist or I have no read permissions")

    def plot(self):
        self.initPlot()
        self.plotDet0()
        self.plotDet1()

    def initPlot(self):
        self.g = Gnuplot.Gnuplot()
        self.g('set term {}'.format(self.formatt))
        self.g('set xlabel "{}"'.format(self.xlabel))
        self.g('set ylabel "{}"'.format(self.ylabel))
        self.g('bin(x,width)=width*floor(x/width)')

    def plotDet0(self):
        self.g('set title "{}, detector 0"'.format(self.title))
        self.g('set output "{}_0.eps"'.format(self.fname))
        self.g('binwidth = {}'.format(iqr(self.data[0])))
        self.g('plot "{}" using (bin($1,binwidth)):(1.0) smooth freq with boxes'.format(self.fname))

    def plotDet1(self):
        self.g('set title "{}, detector 1"'.format(self.title))
        self.g('set output "{}_1.eps"'.format(self.fname))
        self.g('binwidth = {}'.format(iqr(self.data[1])))
        self.g('plot "{}" using (bin($2,binwidth)):(1.0) smooth freq with boxes'.format(self.fname))

    def fit(self):
        self.g("set boxwidth binwidth")
        self.g("set table 'hist.temp'")

main()

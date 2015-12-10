import Gnuplot
import time
import argparse
import os, sys
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import json
import random
import numpy as np

def main():
    parser = argparse.ArgumentParser(description = "Plots parsed json objects from usbcounter, arthur.py script. Plots a histogram of the counts by default. ")
    parser.add_argument('dir', metavar = 'timestamp', nargs = '+', help = "Timestamp of json file to be plotted")

    parser.add_argument('title', metavar = 'title', nargs = '+', help = "Title to be included in plot.")

    parser.add_argument('--verbose', dest='verbose', action='store_true', help = "Print error messages. Does not do so by default.")

    parser.set_defaults(verbose=False)

    args = parser.parse_args()
    a = arthurParse()
    a.load(args.dir[0], args.title[0], args.verbose)
    a.plot()
def iqr(x):
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 2 * iqr * len(x) ** (float(-1)/float(3))

class arthurParse():
    def __init__(self):
        self.cfg = {}
        with open('cfg/.arthurparse') as f:
            x = f.read()
            x = x.split('\n')
            for i in x:
                if len(i) > 0:
                    i = i.rstrip()
                    i = i.split('=')
                    self.cfg[i[0]] = i[1]
        print "\n warning: many components are hardcoded. may break easily. \n"
    def load(self, path, title, verbose):
        self.d1 = []
        self.d2 = []
        self.path = path
        self.title = title
        self.titlepath = ' '.join(path.split('_'))
        self.fpath = 'jsondata/' + path
        with open(self.fpath + '.json', 'rb+') as datafile:
            self.data = json.load(datafile)
        with open(self.fpath, 'wb+') as rawfile:
            for i in xrange(len(self.data['counts'])):
                try:
                    rawfile.write('{}\t{}\n'.format(self.data['counts'][i][1][0], self.data['counts'][i][1][1]))
                    self.d1.append(self.data['counts'][i][1][0])
                    self.d2.append(self.data['counts'][i][1][1])
                except IndexError:
                    if verbose:
                        print ('IndexError. Are you using the wrong datafile without timedata? If not, the usbcounter did not respond in time. Ignoring ')
                    else:
                        pass
    def plot(self):
        self.initPlot()
        self.plotDet0()
        self.plotDet1()

    def plotDet0(self):
        self.g('set title "{} {}, detector 0, duration {} intervals"'.format(self.titlepath, self.title, self.data['duration']))
        self.g('set output "{}_0.eps"'.format(self.fpath, self.cfg['format']))
        self.g('binwidth = {}'.format(iqr(self.d1)))
        self.g('plot "{}" using (bin($1,binwidth)):(1.0) smooth freq with boxes'.format(self.fpath))
    def plotDet1(self):
        self.g('set title "{} {}, detector 1, duration {} intervals"'.format(self.titlepath, self.title, self.data['duration']))
        self.g('set output "{}_1.eps"'.format(self.fpath, self.cfg['format']))
        self.g('binwidth = {}'.format(iqr(self.d2)))
        self.g('plot "{}" using (bin($2,binwidth)):(1.0) smooth freq with boxes'.format(self.fpath))
    def initPlot(self):
        self.g = Gnuplot.Gnuplot()
        self.g('set term {}'.format(self.cfg['format']))
        self.g('set xlabel "{}"'.format(self.cfg['xlabel']))
        self.g('set ylabel "{}"'.format(self.cfg['ylabel']))
        #self.g('set yrange [0:100]')
        self.g('bin(x,width)=width*floor(x/width)')
    def fit(self):


main()

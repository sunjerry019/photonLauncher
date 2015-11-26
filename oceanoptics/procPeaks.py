#!/bin/python2
"""
WIP

gets peak position and fwhm of peak for a certain wavelength range, for highest peak, tracks over time.

zy 18 Nov 2015
"""
from __future__ import division
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import argparse
import time
import os
import math
import re

def checkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', metavar = 'd', nargs = '+', help ="Folder of files to be processed and plotted")
    parser.add_argument('title', metavar = 't', nargs = '+', help = "Title of plot")
    parser.add_argument('--start', metavar = 'ps', help = "Start of range to scan peaks")
    parser.add_argument('--end', metavar = 'pe', help = "End of range to scan peaks")
    args = parser.parse_args()
    if not (args.start):
        p = procPeak(args.dir[0], args.title[0], False, False)
    else:
        p = procPeak(args.dir[0], args.title[0], args.start, args.end)

class procPeak():
    def __init__(self, direc, t, ps, pe):
        self.data = {}
        self.stats = []
        self.data_dir = direc
        self.title = t
        self.auto = False
        self.threshold = 3000

        if ps:
            self.prange = (ps, pe)
        else:
            self.auto = True

        self.n = 0

        #parses all .txt
        self.patt = re.compile(ur'.txt$', re.IGNORECASE)
        for fn in sorted(os.listdir(self.data_dir)):
            if len(re.findall(self.patt, fn)):
                self.parseFile(fn)

        if self.auto:
            arr = self.searchPeaks()
            dataPoints = self.getPoints(arr)
            for cwl in sorted(dataPoints):
                self.fitGauss(cwl, dataPoints[cwl])
        #else:
            #self.procSpec()
            #self.plotSpec()

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
                        #print x
                        self.data[x[0]] = x[1]

                    except:
                        print x
                if line[:2] == ">>":
                    start_read = True

    def procPeak(self):
        for k in self.data:
            if int(k) not in xrange(ps, pe):
                del self.data[k]
        #peak =

    def searchPeaks(self):
        peakwavelengths = {}
        prevpoint = -1
        prevwl = -1;
        minimum = 0
        wlAtMinimum = 0
        maximum = 0
        possiblePeakDetected = False

        for wl in sorted(self.data):
            if prevpoint != -1:
                dy = self.data[wl] - prevpoint

                if dy > 0 and possiblePeakDetected == False:
                    #if it detects a rise, it stores the turning pt into the peak
                    possiblePeakDetected = True
                    minimum = prevpoint
                    wlAtMinimum = prevwl
                    maximum = self.data[wl]
                elif dy > 0:
                    #updates the maximum
                    maximum = self.data[wl]
                    wlAtMaximum = wl
                elif dy < 0 and possiblePeakDetected == True:
                    #if it detects a drop after a rise, it checks the magnitude of the rise
                    magnitude = maximum - minimum
                    if magnitude >= self.threshold:
                        peakwavelengths[prevwl] = wlAtMinimum
                    possiblePeakDetected = False

            prevwl = wl
            prevpoint = self.data[wl]

        return peakwavelengths #returns in the form of CentralWavelength: Wavelength at minimum

    def getPoints(self, peakwls):
        """range of points start from 1.5nm before minWL and 1.5 after the symmetrical side of the minWL"""
        triggerWLs = []
        cwls = []
        for cwl in sorted(peakwls):
            mwl = peakwls[cwl]
            cwls.append(cwl)
            triggerWLs.append(mwl - 1.5)
            triggerWLs.append(cwl + (cwl - mwl) + 1.5)
        points = {}
        iterator = 0
        record = False
        for wl in sorted(self.data):
            if iterator < len(triggerWLs):
                if wl >= triggerWLs[iterator]:
                    record = False if record else True
                    iterator += 1
            if record:
                cwl = cwls[int(iterator/2)]
                if cwl not in points:
                    points[cwl] = {}
                points[cwl][wl] = self.data[wl]

        return points #cwl: dict of points

    def plotSpec(self):
        tempf = '.temp'
        with open(tempf, 'wb+') as f:
            for k in self.stats:
                f.write("{}\t{}\t{}\n".format(k, self.stats[k]['mean'], self.stats[k]['std']))
        g = Gnuplot.Gnuplot()
        g('set term epscairo size 10, 7.5')
        g('set xlabel "Wavelength (nm)"')
        g('set ylabel "Intensity (Arbitrary Units)"')
        g('set title "{}"'.format(self.title))
        g('set output "{}.eps"'.format(os.path.join(self.data_dir, "spectrumplot")))
        g('plot ".temp" u 1:2:3 with yerrorbars pt 7 ps 0.2 smooth unique')
        time.sleep(1)
        os.remove(tempf)

    def fitGauss(self, centralWl, arrPoints):
        tempf = '.temp'
        with open(tempf, 'wb+') as f:
            for key in arrPoints:
                f.write("{}\t{}\n".format(key, arrPoints[key]))\

        initialGuess = {
            'y0': arrPoints[min(arrPoints, key=arrPoints.get)],
            'w' : 1,
            'xc': centralWl,
            'A' : 1
        }

        g = Gnuplot.Gnuplot()
        g('set term epscairo size 10, 7.5')
        g('set xlabel "Wavelength (nm)"')
        g('set ylabel "Intensity (Arbitrary Units)"')
        g('set title "Spectrum at {} nm"'.format(centralWl))
        g('set output "{}.eps"'.format(os.path.join(self.data_dir, "spectrumplot_" + str(centralWl) + "nm")))
        g('set fit logfile "{}.log"'.format(os.path.join(self.data_dir, "spectrumplot_" + str(centralWl) + "nm")))
        g('set fit maxiter 1000')
        g('set fit limit 1e-4')
        g('PI={}; y0={}; w={}; xc={}; A={}'.format(math.pi, initialGuess['y0'], initialGuess['w'], initialGuess['xc'], initialGuess['A']))
        g('gauss(x) = y0+A*sqrt(2/PI)/w*exp(-2*((x-xc)/w)**2)')
        g('fit gauss(x) "{}" using 1:2 via y0, w, xc, A'.format(tempf))
        g('plot "{}" using 1:2, gauss(x)'.format(tempf))
        #os.remove(tempf)
main()

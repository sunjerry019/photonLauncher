#!/bin/python3

"""
points.py

Given a folder of background counts and spectrum measurements, parse and then concatenates each wavelength into a data over time

~yd
2016-01-04
"""

import argparse
import numpy as np
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import os, sys
import re
import datetime
import time

def check_dir(directory):
    if not os.path.exists(directory):
        print("Directory {} does not exist...creating...".format(directory))
        os.makedirs(directory)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bgdir', metavar = 'bd', help ="Folder containing the bg counts")
    parser.add_argument('datadir', metavar = 'dd', help ="Folder containing interested counts")
    parser.add_argument('outputdir', metavar = 'od', help = "Folder to output files")
    args = parser.parse_args()

    p = points(args.bgdir, args.datadir, args.outputdir)

class points():
    def __init__(self, bgdir, datadir, outputdir):
        self.data = {}
        self.bgdir = bgdir
        self.datadir = datadir
        self.outputdir = outputdir
        self.bgod = os.path.join(self.outputdir, "background_counts")
        self.sigod = os.path.join(self.outputdir, "signal_counts")
        self.firstTimestamp = -1;
        self.deltatimes = [[],[]]

        check_dir(self.outputdir)
        check_dir(self.bgod)
        check_dir(self.sigod)

        try:
            self.bgfl = sorted([x for x in os.listdir(self.bgdir) if x.endswith(".txt")])
            self.datfl = sorted([x for x in os.listdir(self.datadir) if x.endswith(".txt")])
        except:
            print("Error reading from directories");
            sys.exit(1)

        print("-> Parsing BG")
        self.traverse("bg")
        print("-> Parsing readings")
        self.traverse("readings")
        print("-> Collating...")
        self.collate()

        print("Done!")

    def traverse(self, typ):
        if typ == "bg" or typ == "readings":
            if typ == "bg":
                dirpath = self.bgdir
                flist = self.bgfl
            else:
                dirpath = self.datadir
                flist = self.datfl

            self.parse(typ, os.path.join(dirpath, flist[0]), True)
            flist.pop(0)

            cnt = 0
            tt = len(flist)

            for datei in sorted(flist):
                self.parse(typ, os.path.join(dirpath, datei))
                cnt += 1
                prog = round(((float(cnt)/float(tt)) * 100), 2)
                print("{}%".format(prog), end="\r")
            print('\n')

    def parse(self, typ, fname, first = False):
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
                        if x[0] not in self.data:
                            self.data[x[0]] = [[],[]]
                        self.data[x[0]][typ].append(x[1])
                    except:
                        print("ignoring error in parsing: ", fname, line)
                if line[:5] == "Date:":
                    t = time.strptime(line.rstrip()[6:], "%a %b %d %H:%M:%S %Z %Y")
                    zeit = datetime.datetime(*t[:6])

                    if first:
                        self.firstTimestamp = zeit
                        with open(os.path.join(self.outputdir, "meta.data"), 'w') as f:
                            f.write("starttime\t{}\n".format(zeit.__str__()))

                    dt = zeit - self.firstTimestamp
                    self.deltatimes[typ].append(dt.total_seconds())
                if line[:2] == ">>":
                    start_read = True

    def collate(self):
        cnt = 0
        tt = len(self.data)

        for wavelength in self.data:
            with open(os.path.join(self.bgod, str(wavelength)), 'w') as f:
                for i in range(len(self.deltatimes[0])):
                    f.write("{}\t{}\n".format(self.deltatimes[0][i], self.data[wavelength][0][i]))

            with open(os.path.join(self.sigod, str(wavelength)), 'w') as f:
                for i in range(len(self.deltatimes[1])):
                    f.write("{}\t{}\n".format(self.deltatimes[1][i], self.data[wavelength][1][i]))
            cnt += 1

            prog = round(((float(cnt)/float(tt)) * 100), 2)
            print("{}%".format(prog), end="\r")

        print('\n')
main()

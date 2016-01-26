import argparse
from os import listdir
from os.path import isfile, join
import sys, json
import numpy as np

""" main class takes a string of folder name, then returns a dictionary with the std dev (error bars). option to save json file."""

class spec():
    def __init__(self, foldername, output = None, basefilename = None, raw = None):
        self.fn = foldername
        self.base = basefilename
        self.files = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        #print self.f

        if basefilename == "":
            print "No base filename indicated, will use all files in directory {}".format(foldername)
        else:
            print "Base filename of {}.".format(basefilename)
            self.files = [x for x in self.files if basefilename == x[:-9]]

        #print self.f
        self.output = output
        self.raw = raw
        self.data = {}
    def traverse(self, i):
        with open(join(self.fn, i), 'rb') as f:
            start_read = False
            for line in f:
                if start_read and line[:2] == ">>":
                    start_read = False
                if start_read:
                    try:
                        x = line.rstrip().split("\t")
                        #print x
                        x = [float(i) for i in x]
                        if x[0] not in self.data.keys():
                            self.data[x[0]] = [x[1]]
                        else:
                            self.data[x[0]].append(x[1])
                    except:
                        print "Error parsing {}, {}".format(i, line)
                if line[:2] == ">>":
                    start_read = True
    def parse(self):
        for i in self.files:
            self.traverse(i) ; sys.stdout.write("\r{}".format(i))
        std = {}
        m = {}
        for wavelength in self.data:
            wavelengths = np.array(self.data[wavelength])
            std[wavelength] = np.std(wavelengths, dtype = np.float64)
            m[wavelength] = np.mean(wavelengths, dtype = np.float64)

        mdata = {"raw": self.data, "std": std, "mean": m}
        if self.raw:
            if self.base == None:
                rawpath = join(self.fn, "raw")
            else:
                rawpath = self.output
            with open(rawpath, 'w') as f:
                f.write("#x\ty\tyerror\n")
                for i in sorted(self.data, key=self.data.get):
                    f.write("{}\t{}\t{}\n".format(i, m[i], std[i]))

        return mdata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fn', type = str, help = "Folder of data files")
    parser.add_argument('-b', '--basename', type = str, help = "Base file name", default = None)
    parser.add_argument('-o', '--outputfolder', type = str, help = "Path to dump raw file.", default = None)
    parser.add_argument('-r', '--rawfile', action = 'store_true', help = "Use this flag to output raw, plottable ascii file", default = None)
    #parser.add_argument('-bg', '--backgroundfile', type = str, help = "Background readings to normalise the data", default = None)
    args = parser.parse_args()

    a = spec(args.fn, output = args.outputfolder, raw = args.rawfile, basefilename = args.basename)
    a.parse()
    print " == Parse complete == \n"

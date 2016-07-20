import argparse
from os import listdir
from os.path import isfile, join
import sys
import json
import numpy as np

# main class takes a string of folder name, then returns a dictionary with the std dev (error bars). option to save json file.

class spec():
    """Initialises the class with options."""
    def __init__(self, foldername, output = None, basefilename = None, raw = None, ):
        self.fn = foldername
        self.base = basefilename
        self.files = [f for f in listdir(foldername) if isfile(join(foldername, f))]

        # The SpectraSuite application dumps separate readings at certain time intervals in separate files
        # There's an option for a BASEFILENAME which helps to identify which measurement it is
        # The filenames look like "BASEFILENAMEXXX" where XXX refers to the index of the sample.

        if basefilename == "":
            print("No base filename indicated, will use all files in directory {}".format(foldername))
        else:
            print("Base filename of {}.".format(basefilename))
            self.files = [x for x in self.files if basefilename == x[:-9]]

        #print self.f
        self.output = output
        self.raw = raw
        self.data = {}
    def traverse(self, i):
        """ Read through data file (files inside directory FOLDERNAME with a BASEFILENAME) """
        with open(join(self.fn, i), 'rb') as f:
            for line in f:
                try:
                    x = line.rstrip().split("\t")
                    #print x
                    x = [float(i) for i in x]
                    if x[0] not in self.data.keys():
                        self.data[x[0]] = [x[1]]
                    else:
                        self.data[x[0]].append(x[1])
                except:
                    print("Error parsing {}, {}".format(i, line))

    def parse(self):
        """ Wrapper around traverse() and processes the files with statistics (mean and std)"""
        for i in self.files:
            self.traverse(i) ; sys.stdout.write("\rNow processing {}".format(i))
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
                print self.data
                _data = self.data.keys()
                _data.sort()
                for i in _data:
                    f.write("{}\t{}\t{}\n".format(i, m[i], std[i]))

        return mdata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fn', type = str, help = "Folder of data files")
    parser.add_argument('-b', '--basename', type = str, help = "Base file name", default = None)
    parser.add_argument('-o', '--outputpath', type = str, help = "File path of ascii output.", default = None)
    parser.add_argument('-r', '--rawfile', action = 'store_true', help = "Use this flag to output raw, plottable ascii file", default = None)
    #parser.add_argument('-t', '--type', type = str, help = "Set to home to not look for the >> that oceanoptics files have. Defaults to home.", default = "home")
    # parser.add_argument('-bg', '--backgroundfile', type = str, help = "Background readings to normalise the data", default = "home"")
    args = parser.parse_args()

    a = spec(args.fn, output = args.outputpath, raw = args.rawfile, basefilename = args.basename)
    a.parse()
    print(" == Parse complete == \n")

import argparse
from os import listdir
from os.path import isfile, join
import sys, json
import numpy as np

""" main class takes a string of folder name, then returns a dictionary with the std dev (error bars). option to save json file."""

class spec():
    def __init__(self, foldername, output = None, basefilename = "", raw = None):
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

    def parse(self):
        for i in self.files:
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
        std = {}
        m = {}
        for wavelength in self.data:
            wavelengths = np.array(self.data[wavelength])
            std[wavelength] = np.std(wavelengths, dtype = np.float64)
            m[wavelength] = np.mean(wavelengths, dtype = np.float64)

        mdata = {"raw": self.data, "std": std, "mean": m}
        if self.output:
            with open(join(self.output + ".json") ,'w') as f:
                json.dump(mdata, f)
        if self.raw:
            if self.base == "":
                rawpath = join(self.fn,"raw")
            else:
                rawpath = join(self.fn, self.base)
            with open(rawpath, 'w') as f:
                f.write("#x\ty\tyerror\n")
                for i in sorted(self.data, key=self.data.get):
                    f.write("{}\t{}\t{}\n".format(i, m[i], std[i]))

        return mdata

if __name__ == '__main__':
    s = spec("/home/zy/Documents/spectrum_data/glass_slide_measurement", basefilename = "led_base", raw = 1)
    print s.parse()

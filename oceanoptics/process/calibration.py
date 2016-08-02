from __future__ import division
import argparse
from os import listdir
from os.path import isfile, join, dirname, realpath, basename
import sys, json
import numpy as np
import math

class norm():
    def __init__(self, basefile, samplefile, referencefile, output = ''):
        base = []

        result = []
        base = self.parse_raw(basefile,base)
        sample = []
        sample = self.parse_raw(samplefile,sample)
        reference = []
        reference = self.parse_raw(referencefile,reference)
        _z = [i[1] for i in base]
        maxbase = max(_z)
        maxindex = _z.index(maxbase)
        normalise_range = (350, 1040)
        for i in xrange(len(base)):
            if not(base[i][0] >= normalise_range[0] and base[i][0] <= normalise_range[1]):
                continue
            # 0 is the index/ wavelength, 1 is for the counts at that wavelength, 2 is the yerror at the wavelength
            result.append([base[i][0], self.radiation(base[i][0]), self.getErrorOf(base[i][0],[base[i][1],base[i][2]],[sample[i][1],sample[i][2]],[reference[i][1],reference[i][2]])])

        if output != '':
            fp = output
        else:
            fp = "./normspectra{}".format(time.strftime("%Y%m%d_%H%M"))
        with open(fp, "w") as f:
            for i in result:
                f.write("{}\t{}\t{}\n".format(i[0], i[1], i[2]))

        print " == Normalisation Complete == \n"

    def parse_raw(self,_f, data_array):
        with open(_f) as f:
            for line in f:
                if line[:1] == "#":
                    continue
                line = line.strip().split('\t')
                line = [float(x) for x in line]
                data_array.append(line)
        return data_array

    def radiation(self, x):
    	return 1/(math.exp((6.62607004*10**(-34)*299792458)/(x*10**(-9)*1.38064852*10**(-23)*3100))-1)

    def getErrorOf(self, wavelength, base, sample, reference):
        # base = [mean value, error value]
        # z = sample/base
        return self.radiation(wavelength)*math.sqrt((sample[1]**2+base[1]**2)/(sample[0]-base[0])**2+(reference[1]**2+base[1]**2)/(reference[0]-base[0])**2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bn', type = str, help = "Path to base file")
    parser.add_argument('sn', type = str, help = "Path to of sample file")
    parser.add_argument('rn', type = str, help = "Path to of reference file")
    parser.add_argument('-o', '--outputfile', type = str, help = "Filepath to output. ")
    args = parser.parse_args()

    n = norm(args.bn, args.sn, args.rn, output = args.outputfile )

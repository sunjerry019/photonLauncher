from __future__ import division
import argparse
from os import listdir
from os.path import isfile, join, dirname, realpath, basename
import sys, json
import numpy as np
import math

class norm():
    def __init__(self, basefile, samplefile, ntype, output = ''):
        base = []

        result = []
        base = self.parse_raw(basefile,base)
        if not samplefile == "":
            sample = []
            sample = self.parse_raw(samplefile,sample)
        _z = [i[1] for i in base]
        maxbase = max(_z)
        maxindex = _z.index(maxbase)
        normalise_range = (350, 1040)
        for i in xrange(len(base)):
            if not(base[i][0] >= normalise_range[0] and base[i][0] <= normalise_range[1]):
                continue
            # 0 is the index/ wavelength, 1 is for the counts at that wavelength, 2 is the yerror at the wavelength
            if ntype == 'div':
                result.append([base[i][0], (sample[i][1] / base[i][1]),  self.getDivErrorOf([base[i][1], base[i][2]],[sample[i][1], sample[i][2]])])
            elif ntype == 'sub':
                result.append([base[i][0], (sample[i][1] - base[i][1]), self.getSubErrorOf([base[i][1], base[i][2]],[sample[i][1], sample[i][2]])])
            elif ntype == 'norm':
                result.append([base[i][0], (base[i][1]/maxbase), self.getDivErrorOf([base[i][1], base[i][2]], [base[maxindex][1], base[maxindex][2]])])


        if not output == "":
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

    def getDivErrorOf(self, base, sample):
        # base = [mean value, error value]
        # z = sample/base
        return math.sqrt((1/base[0] * sample[1])**2 + ((sample[0]/((base[0])**2)) * base[1])**2)
    def getSubErrorOf(self,base,sample):
        # z = sample - base
        return math.sqrt(( sample[1])**2 + (-1 * base[1])**2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bn', type = str, help = "Path to base file")
    parser.add_argument('-sn', '--samplefile', type = str, help = "Path to of sample file", default = "")
    parser.add_argument('ntype', type = str, help = "Normalise by division or subtraction. 'div' and 'sub' respectively. This operates by performing the function from the sample file to the base file. ")
    parser.add_argument('-o', '--outputfile', type = str, help = "Filepath to output. ")
    args = parser.parse_args()

    n = norm(args.bn, args.samplefile, args.ntype, output = args.outputfile )

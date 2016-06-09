from __future__ import division
import argparse
from os import listdir
from os.path import isfile, join, dirname, realpath, basename
import sys, json
import numpy as np
import math

class norm():
    def __init__(self, basefile, samplefile, ntype, raw = True, output = ''):
        base = []
        sample = []
        result = []
        base = self.parse_raw(basefile,base)
        sample = self.parse_raw(samplefile,sample)

        for i in xrange(len(base)):
            if ntype == 'div':
                result.append([base[i][0], (sample[i][1] / base[i][1]), self.getDivErrorOf([base[i][1], base[i][2]],[sample[i][1], sample[i][2]])])
            elif ntype == 'sub':
                result.append([base[i][0], (sample[i][1] - base[i][1]), self.getSubErrorOf([base[i][1], base[i][2]],[sample[i][1], sample[i][2]])])
        if raw:
            if not output == "":
                fp = output
            else:
                fp = "./normspectra{}".format(time.strftime("%Y%m%d_%H%M"))
            with open(fp, "w") as f:
                for i in result:
                    f.write("{}\t{}\t{}\n".format(i[0], i[1], i[2]))
        else:
            print result
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
        return math.sqrt((1/base[0] * sample[1])**2 + ((sample[0]/(base[0])**-2) * base[1])**2)
    def getSubErrorOf(self,base,sample):
        # z = sample - base
        return math.sqrt(( sample[1])**2 + (-1 * base[1])**2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bn', type = str, help = "Path to base file")
    parser.add_argument('sn', type = str, help = "Path to of sample file")
    parser.add_argument('ntype', type = str, help = "Normalise by division or subtraction. 'div' and 'sub' respectively")
    #parser.add_argument('-d', '--dataformat', type = str, help = "Defaults to raw, choose json to process.json files", default = "raw")
    parser.add_argument('-r', '--rawfile', action = 'store_true', help = "True to output raw, plottable ascii file", default = None)
    parser.add_argument('-o', '--outputfile', type = str, help = "Filepath to output. ", default = None)
    args = parser.parse_args()

    n = norm(args.bn, args.sn, args.ntype, raw = args.rawfile, output = args.outputfile )

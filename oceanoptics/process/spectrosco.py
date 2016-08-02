import argparse
from os import listdir
from os.path import isfile, join
import sys
import json
import numpy as np

# main class takes a string of folder name, then returns a dictionary with the std dev (error bars). option to save json file.

class spec():
    """Initialises the class with options."""
    def __init__(self, foldername, outputdir):

        files = [join(foldername,f) for f in listdir(foldername) if isfile(join(foldername, f))]

        # The SpectraSuite application dumps separate readings at certain time intervals in separate files
        # There's an option for a BASEFILENAME which helps to identify which measurement it is
        # The filenames look like "BASEFILENAMEXXX" where XXX refers to the indexs of the sample.

        self.parse(files, outputdir)

    def traverse(self, fn):
        with open(fn, 'rb') as f:
            _data = []
            for line in f:
                try:
                    x = line.strip().split("\t")
                    x = [float(i) for i in x]
                    _data.append((x[0], x[1]))
                except ZeroDivisionError:
                    print("Error parsing {}, {}".format(i, line))
        return _data

    def parse(self, files, outputdir):
        """ Wrapper around traverse() and processes the files with statistics (mean and std)"""
        data = {}
        for i in files:
            if i.split("/")[-1] == "meta.info": #fk u yudong
                continue
            x = self.traverse(i)
            sys.stdout.write("\rNow processing {}".format(i))
            for i in x:
                if not i[0] in data:
                    data[i[0]] = [i[1]]
                else:
                    data[i[0]].append(i[1])

        std = {}
        m = {}
        print data
        for wavelength in data:
            wavelengths = np.array(data[wavelength])
            std[wavelength] = np.std(wavelengths, dtype = np.float64)
            m[wavelength] = np.mean(wavelengths, dtype = np.float64)

        mdata = {"raw": data, "std": std, "mean": m}

        with open(outputdir, 'w') as f:
            f.write("#x\ty\tyerror\n")
            _data = data.keys()
            _data.sort()
            for i in _data:
                f.write("{}\t{}\t{}\n".format(i, m[i], std[i]))

        return mdata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fn', type = str, help = "Folder of data files")
    parser.add_argument('-o', '--outputpath', type = str, help = "File path of ascii output. Defaults to current directory. ", default = "spectrum_statsputput_{}".format("%y%m%d-%H%M"))

    args = parser.parse_args()

    a = spec(args.fn,args.outputpath)

    print(" == Parse complete == \n")

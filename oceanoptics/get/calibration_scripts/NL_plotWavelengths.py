#!/usr/bin/env python3

import numpy as np
from pathlib import Path
import pickle

class plotWavelengths():
    def __init__(self):
        self.wavelengths = { 730.0 : 1 , 674.06 : 1, 666.05 : 1, 741.99: 1 }
        self.dataDir = "./"
        self.plotDataFile = "./data.dat"
        self.rawData = {}
        self.data = {}
        # wavelength > intTime > intensities
        # for wv in self.wavelengths:
        #     self.rawData[wv] = dict()
        #     self.data[wv] = dict()

        self.parseData()
        # self.writeData()

    def setWavelengths(self, wavelengths):
        if wavelengths:
            self.wavelengths = wavelengths

    def setOutput(self, outputFile):
        if outputFile:
            self.plotDataFile = outputFile

    def writeData(self):
        dataPrintArr = ["{}\t{}"]*len(self.wavelengths) # wavelength <tab> std
        dataPrintStr = "\t".join(dataPrintArr)

        with open(self.plotDataFile, "w") as f:
            # Write Comment Desc
            _wvs = self.wavelengths.keys()
            l2 = ["Error"]*len(self.wavelengths)
            commentArr = [val for pair in zip(_wvs, l2) for val in pair]
            f.write("# intTime\t" + dataPrintStr.format(*commentArr) + "\n")

            for _intT in sorted(self.data[next(iter(self.wavelengths))]):
                # print(_intT)
                # intensity_1, error_1, ...
                outputArr = []
                for _wv in self.wavelengths:
                    outputArr += self.data[_wv][_intT]
                f.write("{}\t".format(_intT) + dataPrintStr.format(*outputArr) + "\n")

    def parseData(self):
        dirlist = Path(self.dataDir).glob('**/*.0')
        for dir in dirlist:
            # because path is object not string
            _intT = float(str(dir)) #intTime

            print("\033[KAggregating for IntTime = {:>5}".format(_intT), end="\r")

            filelist = Path("{}/{}".format(self.dataDir, _intT)).glob('**/data_*')

            for f in filelist:
                _f = str(f)
                with open(_f, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        a = line.split("\t")
                        _wv = float(a[0])
                        _in = float(a[1])
                        # if _wv in self.wavelengths:
                        #     if _intT not in self.rawData[_wv]:
                        #         self.rawData[_wv][_intT] =[]
                        #     self.rawData[_wv][_intT].append(_in)
                        if _wv not in self.rawData:
                            self.rawData[_wv] = dict()
                            self.data[_wv] = dict()
                        if _intT not in self.rawData[_wv]:
                            self.rawData[_wv][_intT] = []
                        self.rawData[_wv][_intT].append(_in)

            for _wv in self.rawData:
                _a = np.array(self.rawData[_wv][_intT])
                _e = np.mean(_a, dtype=np.float64)
                _s = np.std(_a, dtype=np.float64)
                self.rawData[_wv][_intT] = _a
                self.data[_wv][_intT] = [_e, _s]
            # print(self.data)

        print("\033[KWavelengths Aggregated")

if __name__ == '__main__':
    x = plotWavelengths()
    with open("model.pkl", 'wb') as handle:
        pickle.dump(x, handle)
    x.writeData()

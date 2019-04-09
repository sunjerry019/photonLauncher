#!/usr/bin/env python3

import numpy as np
import argparse
import os
from pathlib import Path

class Calibration():
    def __init__(self, _type, _coefficients):
        self.coefficients = _coefficients
        self.type = _type
        if self.type == "NL": self.coefficients.insert(0, 0)

        print(self)

    def calibrate(self, _value):
        corrFactor = 0
        for i in range(len(self.coefficients)):
            corrFactor += self.coefficients[i] * (_value**i)

        return corrFactor

    def __repr__(self):
        return "<Calibration for {}> Coefficients: {}".format(self.type, self.coefficients)


class SubtractDark():
    def __init__(self, _dark, _data, _output, _correctNL, _correctWV):
        # both meta.info will be combined and printed at the top of the file
        self.dataSource = { "data" : _data, "dark" : _dark }
        self.calibrations   = dict()
        self.rawData        = dict()
        # data = struct <typ: <wavelength : np.array(mean, std)>>
        self.data           = dict()
        self.darkSubtracted = dict()

        self.correctNL  = _correctNL
        self.correctWV  = _correctWV
        self.output     = _output


        # Parse the data
        for typ in self.dataSource:
            print("Parsing {} Calibrations".format(typ))
            self.parseCalibrations(typ)
            print("Parsing {}".format(typ))
            self.parseData(typ)

        self.subtractDark()
        self.outputToFile()

    def readCalibrationFile(self, _file):
        with open(_file, 'r') as f:
            # We ignore the first line
            _lines = [float(x.split('\t')[1].strip()) for x in f.readlines()[1:]]

        return _lines

    def parseCalibrations(self, typ):
        if typ not in self.calibrations:
            self.calibrations[typ] = dict()

        # Parse linearity
        if self.correctNL:
            corrType = "NL"
            _coeff = self.readCalibrationFile(os.path.join(self.dataSource[typ], "linearity.corr"))
            self.calibrations[typ][corrType] = Calibration(corrType, _coeff)

        # Parse wavelength
        if self.correctWV:
            corrType = "WV"
            _coeff = self.readCalibrationFile(os.path.join(self.dataSource[typ], "wavelength.corr"))
            self.calibrations[typ][corrType] = Calibration(corrType, _coeff)


    def parseData(self, typ):

        self.rawData[typ] = dict()
        self.data[typ] = dict()

        # https://stackoverflow.com/a/10378012
        pathlist = Path(self.dataSource[typ]).glob('**/data_*')
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            print("\033[K[{}] Parsing File = {}".format(typ, path_in_str), end="\r")
            with open(path_in_str, 'r') as f:
                lines = f.readlines()
                pxCount = -1
                for line in lines:
                    if line[:1] == "#":
                        continue
                    pxCount += 1
                    a = line.split('\t')
                    wavelength = float(a[0])
                    val = float(a[1])

                    # Calibration, where requested
                    if self.correctNL: val         = self.calibrations[typ]["NL"].calibrate(val)
                    if self.correctWV: wavelength  = self.calibrations[typ]["WV"].calibrate(pxCount)

                    if wavelength not in self.rawData[typ]:
                        self.rawData[typ][wavelength] = []
                    self.rawData[typ][wavelength].append(val)

        print("\033[K[{}] Files Parsed".format(typ))

        for wavelength in self.rawData[typ]:
            print("\033[K[{}] Aggregating Wavelength = {}".format(typ, wavelength), end="\r")
            _a = np.array(self.rawData[typ][wavelength])
            _e = np.mean(_a, dtype=np.float64)
            _s = np.std(_a, dtype=np.float64)

            self.rawData[typ][wavelength] = _a
            self.data[typ][wavelength] = [_e, _s]
        print("\033[K[{}] Wavelengths Aggregated".format(typ))

    def subtractDark(self):
        # Check if dark and data are from the same spectrometer
        assert sorted(self.data["dark"].keys()) == sorted(self.data["data"].keys()), "Wavelengths from dark and data don't match!"

        for wavelength in self.data["dark"]:
            # Check if number of data points match
            assert len(self.rawData["dark"][wavelength]) == len(self.rawData["data"][wavelength]), "Number of data points from dark and data for {}nm don't match!".format(wavelength)

            _meanX = self.data["data"][wavelength][0]
            _meanY = self.data["dark"][wavelength][0]
            _varX = self.data["data"][wavelength][1]**2
            _varY = self.data["dark"][wavelength][1]**2

            # Calculate the Var(X + Y) = Var(X) + Var(Y) +2*Cov(X, Y)
            # Calculate Cov
            #     cov(x, y) = \frac{\sum_i^n (x_i - mu_x)(y_i - mu_y)}{n-1}

            _covXY = np.sum((self.rawData["data"][wavelength] - _meanX)*(self.rawData["dark"][wavelength] - _meanY))/(len(self.rawData["dark"][wavelength]) - 1)
            # print("{}nm corr = {}".format(wavelength, _covXY/(self.data["tung"][wavelength][1] * self.data["dark"][wavelength][1])))
            # corr = _covXY / (_stdX * _stdY)

            _e = self.data["data"][wavelength][0] - self.data["dark"][wavelength][0]
            _s = np.sqrt(_varX + _varY + _covXY)
            self.darkSubtracted[wavelength] = [_e, _s]

    def outputToFile(self):
        with open(self.output, 'w') as f:
            for _wv in self.darkSubtracted:
                f.write('{}\t{}\t{}\n'.format(_wv, self.darkSubtracted[_wv][0], self.darkSubtracted[_wv][1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dark', type = str, help = "Folder containing the dark background data")
    parser.add_argument('data', type = str, help = "Folder containing the data")
    parser.add_argument('-o', '--output', type = str, help = "Filepath to output, defaults to ./output.dat", default = "./output.dat")
    parser.add_argument('-n', '--correctNL', action='store_true', help = "correct for Non-linearity of detector. Only enable if 'linearity.corr' exists!")
    parser.add_argument('-w', '--correctWV', action='store_true', help = "correct for incorrect Wavelength of detector. Only enable if 'wavelength.corr' exists!")
    args = parser.parse_args()

    s = SubtractDark(args.dark, args.data, args.output, args.correctNL, args.correctWV)

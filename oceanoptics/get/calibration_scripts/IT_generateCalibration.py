#!/usr/bin/env python3

import numpy as np
from pathlib import Path

class Calibrate():
    def __init__(self):
        self.dataSource = {
            "tung"  : "20190304_1711_Free Space Tungsten",
            "dark" : "20190304_1714_Free Space Tungsten Dark"
        }
        self.T = 2000
        self.rawData = dict()
        self.data = dict()
        self.darkSubtracted = dict()
        self.output = "./data.dat"
        # data = struct <typ: <wavelength : np.array(mean, std)>>

        # Parse the data
        print("Parsing Dark Data")
        self.parseData("dark")
        print("Parsing Tungsten Data")
        self.parseData("tung")

        self.subtractDark()
        # self.calibrateWavelengths()
        self.outputToFile()

    def outputToFile(self):
        with open(self.output, 'w') as f:
            for _wv in self.darkSubtracted:
                f.write('{}\t{}\t{}\n'.format(_wv, self.darkSubtracted[_wv][0], self.darkSubtracted[_wv][1]))

    def subtractDark(self):
        for wavelength in self.data["dark"]:
            _meanX = self.data["tung"][wavelength][0]
            _meanY = self.data["dark"][wavelength][0]
            _varX = self.data["tung"][wavelength][1]**2
            _varY = self.data["dark"][wavelength][1]**2

            # Calculate the Var(X + Y) = Var(X) + Var(Y) +2*Cov(X, Y)
            # Calculate Cov
            #     cov(x, y) = \frac{\sum_i^n (x_i - mu_x)(y_i - mu_y)}{n-1}

            _covXY = np.sum((self.rawData["tung"][wavelength] - _meanX)*(self.rawData["dark"][wavelength] - _meanY))/(len(self.rawData["dark"][wavelength]) - 1)
            # print("{}nm corr = {}".format(wavelength, _covXY/(self.data["tung"][wavelength][1] * self.data["dark"][wavelength][1])))
            # corr = _covXY / (_stdX * _stdY)

            _e = self.data["tung"][wavelength][0] - self.data["dark"][wavelength][0]
            _s = np.sqrt(_varX + _varY + _covXY)
            self.darkSubtracted[wavelength] = [_e, _s]

    def parseData(self, typ):
        # TODO: correct NL before aggregating

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
                for line in lines:
                    if line[:1] == "#":
                        continue
                    a = line.split('\t')
                    wavelength = float(a[0])
                    val = float(a[1])
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

Calibrate()

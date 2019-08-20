#!/usr/bin/env python3

"""
Script to get spectrum from OceanOptics Spectroscope over time

Things to modify before use:
- gid and uid of current user
"""
from __future__ import print_function

from builtins import str
from builtins import range
import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
import argparse
import os
import time
import numpy as np
import pwd
import grp

import datetime

def main(n, description, intTime, interval):
    c = 0
    foldername = "{}_Group".format(time.strftime("%Y%m%d_%H%M%S"))
    uid = pwd.getpwnam("sunyudong").pw_uid
    gid = grp.getgrnam("sunyudong").gr_gid

    # Sanity checking of inputs
    if interval < intTime:
        raise ValueError(f"interval = {interval}; intTime = {intTime}; Interval timing should be more than intTime.")

    if n < 1:
        raise ValueError(f"n = {n}; n must be at least 1.")

    os.mkdir(foldername)
    path = foldername
    os.chown(path, uid, gid)

    with open("{}/meta.info".format(foldername), 'w') as f:
        meta = "{}\tintTime = {} ms\tInterval = {}ms\t{}\n".format(foldername, intTime, interval, description)
        f.write(meta)
        print(meta)
    os.chown("{}/meta.info".format(foldername), uid, gid)

    with Icecube() as cube:
        # Write model information into meta.info
        with open("{}/meta.info".format(foldername), 'a') as f:
            f.write("Serial ({}) = {}\n".format(cube.type, cube.getSerial()))
            f.write("Autonulling Factor = {}".format(cube.autonulling))

        # Write some metadata about corrections
        with open("{}/linearity.corr".format(foldername), 'a') as f:
            f.write("Linearity Correction -> {}th Order Polynomial\n".format(cube.getSingleEEPROM(14)))
            for i in range(6, 14):
                f.write("{}\t{}\n".format(i - 6, cube.getSingleEEPROM(i)))
        os.chown("{}/linearity.corr".format(foldername), uid, gid)

        with open("{}/wavelength.corr".format(foldername), 'a') as f:
            f.write("Wavelength Correction\n")
            for i in range(1, 5):
                f.write("{}\t{}\n".format(i - 1, cube.getSingleEEPROM(i)))
        os.chown("{}/wavelength.corr".format(foldername), uid, gid)

        cube.setIntegrationTime(intTime)
        totalSet = False
        delta = datetime.timedelta(milliseconds = interval)

        while True:
            try:
                if n == 0:
                    print("\nAcquisition Complete")
                    break

                if not totalSet:
                    count = 0
                    total = n
                    digits = int(np.floor(np.log10(total)) + 1)
                    # http://www.kahfei.com/2011/03/11/print-without-newline-in-python/
                    printString = "[{:>10} degC] Acquiring [{:>"+ str(digits) +"}/{}] Left: {}\033[K\r"
                    totalSet = True

                now = datetime.datetime.now()

                if n == total or now >= prevStart + delta:
                    count += 1
                    # print(printString)
                    print(printString.format(str(cube.getTemp()), count, total, n - 1), end=' ')

                    prevStart = datetime.datetime.now()
                    spec = cube.getSpectra()

                    with open("{}/data_{}".format(foldername, n) , 'w') as f:
                        f.write("# {}".format(prevStart))
                        for i in spec:
                            f.write("{}\t{}\n".format(i[0], i[1]))
                    os.chown("{}/data_{}".format(foldername,n), uid, gid)
                    n -= 1

            except KeyboardInterrupt:
                cube.releaseInterface(0)
                cube.close()
                print("\n --- EXITING --- ")
                sys.exit()

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type = int, help = "no. of readings to take. Positive integers only")
    parser.add_argument('-d', '--description', type = str, help = "label each acquisition", default = None)
    parser.add_argument('-t', '--intTime', type = float, help = "milliseconds of integration time", default = 2)
    parser.add_argument('-i', '--interval', type = float, help = "Interval in milliseconds between start of acquisitions. Must be more than integration time.", default = 2)
    args = parser.parse_args()

    main(args.n, args.description, args.intTime, args.interval)
init()

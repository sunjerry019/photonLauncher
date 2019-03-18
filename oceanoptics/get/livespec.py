#!/usr/bin/env python2

"""
Script to get spectrum from OceanOptics Spectroscope

Things to modify before use:
- gid and uid of current user
"""

import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
import argparse
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pwd
import grp

def main(n, description,intTime, noPlot):
    c = 0
    foldername = time.strftime("%Y%m%d_%H%M%S")
    uid = pwd.getpwnam("sunyudong").pw_uid
    gid = grp.getgrnam("sunyudong").gr_gid
    if not n == -1:
        os.mkdir(foldername)
        path = foldername
        os.chown(path, uid, gid)
        if not description == None:
            z = open("spectra_log", "a")
            os.chown("spectra_log", uid, gid)
            z.write("{}\t{}\n".format(foldername, description))
        with open("{}/meta.info".format(foldername), 'w') as f:
            f.write("{}\tintTime = {} ms\t{}\n".format(foldername, intTime, description))

    with Icecube() as cube:
        cube.setIntegrationTime(intTime)
        totalSet = False
        while True:
            try:
                # sys.stdout.write("\r{}".format(n))
                if n == 0:
                    print "\nAcquisition Complete"
                    break
                elif n > 0:
                    # http://www.kahfei.com/2011/03/11/print-without-newline-in-python/
                    if not totalSet:
                        count = 0
                        total = n
                        digits = int(np.floor(np.log10(total)) + 1)
                        printString = "[{:>10} degC] Acquiring [{:>"+ str(digits) +"}/{}] Left: {}\033[K\r"
                        totalSet = True

                    count += 1
                    print printString.format(str(cube.getTemp()), count, total, n - 1),
                else:
                    print "[{:>10} degC] Live Plotting\033[K\r".format(str(cube.getTemp())),

                spec = cube.getSpectra()

                if not noPlot:
                    Y = [i[1] for i in spec]
                    if c == 0: #init
                        X = [i[0] for i in spec]
                        plt.ion()
                        with plt.style.context('fivethirtyeight'):
                            graph = plt.plot(X,Y)[0]
                            plt.xlabel("Wavelength/nm")
                            plt.ylabel("Pixel intensity")
                        c = 1
                    else:
                        graph.set_ydata(Y)
                        with plt.style.context('fivethirtyeight'):
                            plt.draw()
                            plt.pause(0.01)

                # sleep(0.05)

                if n > 0:
                    with open("{}/data_{}".format(foldername,n) , 'w') as f:
                        for i in spec:
                            f.write("{}\t{}\n".format(i[0], i[1]))
                    os.chown("{}/data_{}".format(foldername,n), uid, gid)
                    n -= 1
                    # print " now {} readings left".format(n)

            except KeyboardInterrupt:
                cube.releaseInterface(0)
                cube.close()
                print "\n --- EXITING --- "
                break

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type = int, help = "no. of readings to take. -1 for infinite")
    #parser.add_argument('-p','--plot', action = 'store_true', help = "flag to enable plotting")
    parser.add_argument('-d', '--description', type = str, help = "label each acquisition", default = None)
    parser.add_argument('-t', '--intTime', type = float, help = "milliseconds of integration time", default = 2)
    parser.add_argument('-p', '--noPlot', action='store_true')
    args = parser.parse_args()

    main(args.n, args.description, args.intTime, args.noPlot)
init()

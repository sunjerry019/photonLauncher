import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
import argparse
import os
import time
import matplotlib.pyplot as plt
import numpy as np

def main(n, description):
    c = 0
    foldername = time.strftime("%Y%m%d_%H%M")
    if not n == -1:
        os.mkdir(foldername)
        if not description == None:
            z = open("spectra_log", "a")
            z.write("{}\t{}\n".format(foldername, description))

    with Icecube() as cube:
        cube.setIntegrationTime(2)
        while True:
            try:
                sys.stdout.write("\r{}".format(n))
                spec = cube.getSpectra()
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

                sleep(0.05)

                n -= 1

                if n == 0:
                    break
                elif n > 0:
                    with open("{}/data_{}".format(foldername,n) , 'w') as f:
                        for i in spec:
                            f.write("{}\t{}\n".format(i[0], i[1]))

            except KeyboardInterrupt:
                print " --- EXITING --- "
                break


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type = int, help = "no. of readings to take. -1 for infinite")
    #parser.add_argument('-p','--plot', action = 'store_true', help = "flag to enable plotting")
    parser.add_argument('-d', '--description', type = str, help = "label each acquisition", default = None)
    parser.add_argument('-t', '--integrationTime', type = int, help = "milliseconds of integration time", default = 2)
    args = parser.parse_args()

    main(args.n, args.description, args.integrationTime)
init()

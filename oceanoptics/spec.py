#! /bin/python3

import seabreeze
seabreeze.use('pyseabreeze')
import seabreeze.spectrometers as sb
import datetime
import time
import csv
import os, sys
import Gnuplot, Gnuplot.funcutils
import argparse


#init
savetime = time.strftime('%Y%m%d_%H%M%S')
dirpath = "data"
fileName = os.path.join(dirpath, savetime)
defaultIntegrationTime = 100 #default integration time in ms

def getSpec(typ, intgTime, wl):
    devices = sb.list_devices()
    if not len(devices):
        print("Error: No OceanOptic Device found")
        sys.exit(1)
    for device in devices:
        print(device)

    print("getting spectrum")
    spec = sb.Spectrometer(devices[0])
    print("setting integration time to " + str(intgTime))
    spec.integration_time_micros(intgTime)
    """
    print("getting wavelengths")
    rawWavelengths = spec.wavelengths()
    print("getting intensities")
    rawIntensities = spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
    """
    spektrum = spec.spectrum()
    print("closing Spectroscope")
    spec.close()

    if typ == 0:
        writePlotSpec(spektrum, True)
    elif typ == 1:
        showWavelength(spektrum, wl)

def writePlotSpec(spek, plot):
    print("writing raw data to tsv: " + fileName)
    with open(fileName, "w") as record_file:
        writer = csv.writer(record_file, delimiter='\t')
        for i in range(len(spek[0])):
            writer.writerow([spek[0][i], spek[1][i]])
    if plot:
        plotSpec(fileName)

def showWavelength(spek, wl):
    for i in range(len(spek[0])):
        wellenlange = spek[0][i]
        if (round(wellenlange) == round(int(wl))) or (round(wellenlange) + 1 == round(int(wl))) or (round(wellenlange) - 1 == round(int(wl))):
            intensitat = spek[1][i]
            print(repr(wellenlange) + "\t" + repr(intensitat))


def plotSpec(fileName):
    g = Gnuplot.Gnuplot(debug=0)
    g('set term svg')
    g('set output "{}.svg"'.format(fileName))
    g('set yrange [1000:20000]')
    g('plot "{}" u 1:2 w p'.format(fileName))
    print("plotted at {}".format(fileName))


def main():
    parser = argparse.ArgumentParser(description = "spec: Script to obtain data from an OceanOptic Spectroscope")
    parser.add_argument('--time', metavar = 't', help = "Integration Time (in ms)")
    parser.add_argument('--wavelength', metavar = 'w', help = "Only retrieve wavelengths around a certain integer wavelength")
    args = parser.parse_args()

    if args.time:
        zeit = args.time
    else:
        zeit = defaultIntegrationTime

    #handle wavelength
    if args.wavelength:
        getSpec(1, zeit, args.wavelength)
    else:
        getSpec(0, zeit)

main()
sys.exit(0)

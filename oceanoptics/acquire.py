#! /bin/python3

import seabreeze
seabreeze.use('pyseabreeze')
import seabreeze.spectrometers as sb
import datetime
import time
import csv
import os, sys
import argparse


#init
savetime = time.strftime('%Y%m%d_%H%M%S')
dirpath = "data"
fileName = os.path.join(dirpath, savetime)
defaultIntegrationTime = 100 #default integration time in ms

def openSpec():
    devices = sb.list_devices()
    if not len(devices):
        print("Error: No OceanOptic Device found")
        sys.exit(1)
    for device in devices:
        print(device)

    spec = sb.Spectrometer(devices[0])
    return spec

def getSpec(spec, intgrTime):
    print("setting integration time to " + str(intgTime))
    spec.integration_time_micros(intgTime)
    spektrum = spec.spectrum()
    return spektrum

def writePlotSpec(spek, suffix, plot):
    name = fileName + "_" + suffix
    print("writing raw data to tsv: " + name)
    with open(name, "w") as record_file:
        writer = csv.writer(record_file, delimiter='\t')
        for i in range(len(spek[0])):
            writer.writerow([spek[0][i], spek[1][i]])
    if plot:
        plotSpec(fileName)

def main():
    parser = argparse.ArgumentParser(description = "spec: Script to obtain data from an OceanOptic Spectroscope")
    parser.add_argument('--time', metavar = 't', help = "Integration Time (in ms)")
    parser.add_argument('--duration', metavar = 'T', help = "Duration in minutes")
    args = parser.parse_args()

    if args.time:
        zeit = args.time
    else:
        zeit = defaultIntegrationTime

    spektrometer = openSpec()
    #get final time
    #while time < final time, get data
    spektrometer.close()


main()
sys.exit(0)

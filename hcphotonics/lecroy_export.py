#!/bin/python3
"""
Utility to export either histogram or waveform from Lecroy Oscilloscope to a file.
"""

import hcphotonics.lecroy as lecroy
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conf",  help="Path to config file", type = str)
    parser.add_argument("f", metavar = "exportFile", help="File path to save in", type = str)
    parser.add_argument("t", metavar = "type", type = str, help = "h for histogram, w for waveform")
    parser.add_argument("c", metavar = "channel", help = "1,2,3,4, A,B,C,D")
    args = parser.parse_args()

    scope = lecroy.Lecroy(args.conf)
    print("Stopping scope")
    scope.stop()
    if args.t.lower() == "h":
        print("Getting Histogram")
        (data,mdata) = scope.getHistogram(args.c)
    elif args.t.lower() == "w":
        print("Getting Waveform")
        (data, mdata) = scope.getWaveform(args.c)

    try:
        with open(args.f, "w") as f:
            for i in data:
                f.write('{}\t{}\n'.format(i[0],i[1]))
    except:
        print("Error saving file. Is the location writable?")

if __name__ == "__main__": main()

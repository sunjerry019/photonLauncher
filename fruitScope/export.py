import sys
sys.path.insert(0, '../helpers/')
import lecroy
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("f", metavar = "exportFile", help="File path to save in", type = str)
    parser.add_argument("t", metavar = "type", type = str, help = "h for histogram, w for waveform")
    parser.add_argument("c", metavar = "channel", help = "1,2,3,4, A,B,C,D")
    args = parser.parse_args()

    scope = lecroy.Lecroy()
    print "Stopping scope"
    scope.stop()
    if args.t == "h":
        print "Getting Histogram"
        (data,mdata) = scope.getHistogram(args.c)
    elif args.t == "w":
        print "Getting Waveform"
        (data, mdata) = scope.getWaveform(args.c)

    try:
        with open(args.f, "w") as f:
            for i in data:
                f.write('{}\t{}\n'.format(i[0],i[1]))
    except:
        print "Error saving file. Is the location writable?"
main()

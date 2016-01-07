import sys
sys.path.insert(0, '../helpers/')
import lecroy
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("f", metavar = "exportFile", help="File path to save in", type = str)
    parser.add_argument("c", metavar = "channel", help = "1,2,3,4, A,B,C,D")
    args = parser.parse_args()

    scope = lecroy.Lecroy()
    print "Stopping scope"
    scope.stop()
    print "Getting Histogram"
    (hist,mdata) = scope.getHistogram(args.c)

    try:
        with open(args.f, "w") as f:
            for i in hist:
                f.write('{}\t{}\n'.format(i[0],i[1]))
    except:
        print "Error saving file. Is the location writable?"
main()

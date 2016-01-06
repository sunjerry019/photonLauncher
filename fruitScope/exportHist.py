import sys
sys.path.insert(0, '../helpers/')
import lecroy
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("f", metavar = "exportFile", help="Name of exported file", type = str)
    args = parser.parse_args()

    scope = lecroy.Lecroy()
    print "Stopping scope"
    scope.stop()
    print "Getting Histogram"
    (hist,mdata) = scope.getHistogram()

    try:
        with open(args.f, "w") as f:
            json.dump(hist, f)
            print "Saved"
    except:
        print "Error saving file. Is the location writable?"
main()

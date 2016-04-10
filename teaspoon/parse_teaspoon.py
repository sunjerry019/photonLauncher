import sys
import argparse

sys.path.insert(0, '../helpers/')

from teaspoon import parse

def main(inputpath, outputpath, outputboolean, verbosity):
    """ Writes ASCII data to file. """
    if verbosity:
        print("TSP01 data parser. \n ============")
        print("Reading file from {}".format(inputpath))
        if outputboolean:
            print("File output suppressed, will print data and metadata")
    #print(inputpath)
    (data, metadata) = (parse(inputpath))
    if not outputpath == '.':
        op = outputpath
    else:
        op = inputpath.split('.')[0]
    if not outputboolean:
        with open(op, 'w') as f:
            for i in data:
                for j in range(len(i)):
                    i[j] = str(i[j])

                x = "\t".join(i) + "\n"
                f.write(x)
    else:
        print(data)
        print(metadata)

def init():
    """ Argument parsing for command line usage """
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", type = str, default = ".", help = "Path for input data file to be parsed.")
    parser.add_argument("-o", "--outputpath", type = str, default = ".",help = "Path for output plottable file.")
    parser.add_argument("-s", "--suppress_output", default = False, action = "store_true", help = "Use this flag to disable file output for debugging purposes.")
    parser.add_argument("-v", "--verbosity", default = False, action = "store_true", help = "Increase text output for debugging")
    args = parser.parse_args()
    main(args.inputpath, args.outputpath, args.suppress_output, args.verbosity)

if __name__ == '__main__':
    init()

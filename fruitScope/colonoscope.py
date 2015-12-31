import sys
sys.path.insert(0, '../helpers/')
import lecroy
import argparse
import threading

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("t", metavar = "duration", help="Duration of acquisition", type = int, nargs = '+')
    args = parser.parse_args()
    print args.t
    scope = lecroy.Lecroy()
    def stop():
        scope.stop()
        scope.getHistogram()
    scope.start()
    t = threading.Timer(args.t[0], stop)
    t.start()
main()

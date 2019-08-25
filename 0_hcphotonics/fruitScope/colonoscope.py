import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)
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

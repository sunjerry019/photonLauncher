import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
from threading import Thread
import subprocess
import argparse
import os
import time

def main(n, plot, description):
    def gen(n):
        foldername = time.strftime("%Y%m%d_%H%M")
        if not n == -1:
            os.mkdir(foldername)
            if not description == None:
                z = open("spectra_log", "a")
                z.write("{}\t{}\n".format(foldername, description))
        with Icecube() as cube:
            while True:
                try:
                    sys.stdout.write("\r{}".format(n))
                    spec = cube.getSpectra()

                    with open('.temp', 'w') as f:
                        for i in spec:
                            f.write("{}\t{}\n".format(i[0], i[1]))

                    sleep(0.1)
                    n -= 1

                    if n == 0:
                        break
                    elif n > 0:
                        with open("{}/data_{}".format(foldername,n) , 'w') as f:
                            for i in spec:
                                f.write("{}\t{}\n".format(i[0], i[1]))

                except KeyboardInterrupt:
                    break
                    print " --- EXITING ---"
                    cube.__exit__()
                    with open("{}.dat".format(time.strftime("%M%S"))) as g:
                        for _ in spec:
                            g.write("{}\t{}\n".format(_[0], _[1]))
    def plot():
        subprocess.call(["gnuplot", "loop.gnu"])


    #t = Thread(target=gen, args=(n,))
    #u = Thread(target=plot)
    gen(n)
    #t.start()
    #sleep(0.05)
    #if plot:
    #    u.start()

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type = int, help = "no. of readings to take. -1 for infinite")
    parser.add_argument('-p','--plot', action = 'store_true', help = "flag to enable plotting")
    parser.add_argument('-d', '--description', type = str, help = "label each acquisition", default = None)
    args = parser.parse_args()

    main(args.n, args.plot, args.description)
init()

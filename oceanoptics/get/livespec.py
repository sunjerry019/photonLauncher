import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
from threading import Thread
import subprocess
import argparse
import os
import time

def main(n, plot):
    def gen(n):
        foldername = time.strftime("%Y%m%d_%H%M")
        if not n == -1:
            os.mkdir(foldername)
        with cube as Icecube():
            while True:
                try:
                    spec = cube.getSpectra()

                    with open('.temp', 'w') as f:
                        for i in spec:
                            f.write("{}\t{}\n".format(i[0], i[1]))

                    sleep(1)
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

    
    t = Thread(target=gen, args=(n,))
    u = Thread(target=plot)

    t.start()
    sleep(0.05)
    if plot:
        u.start()

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type = int, help = "no. of readings to take. -1 for infinite")
    parser.add_argument('-p','--plot', action = 'store_true', help = "flag to enable plotting")
    args = parser.parse_args()

    main(args.n, args.plot)
init()

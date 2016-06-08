import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube
from time import sleep
from threading import Thread
import subprocess


def gen():
    with Icecube() as cube:
        cube.setIntegrationTime(10)
        while True:
            try:
                spec = cube.getSpectra()
                with open('.temp', 'w') as f:
                    for i in spec:
                        f.write("{}\t{}\n".format(i[0], i[1]))
                sleep(1)
            except KeyboardInterrupt:
                print " --- EXITING ---"
                cube.__exit__()
                with open("{}.dat".format(time.strftime("%M%S")) as g:
                    for _ in spec:
                        g.write("{}\t{}\n".format(_[0], _[1]))
def plot():
    subprocess.call(["gnuplot", "loop.gnu"])

t = Thread(target=gen)
u = Thread(target=plot)

t.start()
sleep(0.1)
u.start()

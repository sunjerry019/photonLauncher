import sys, os

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)

# sys.path.insert(0, '../helpers/')

from mjolnir import Mjolnir
import argparse
import time
m = Mjolnir()
#m.homeMotor()
def moveL(i, x):
    for _ in xrange(i):
        #time.sleep(2)
        m.moveLinMotor(x)
        print "{}: \t Moved by {}".format(_, x)

def moveR(x, s):
    # moves x degrees, uses min step sizes
    x = x * 3600
    x /= float(2.16)
    print x
    for _ in xrange(int(x)):
        m.moveRotMotor(s)

def main():
    parser = argparse.ArgumentParser(description = "Controls Thorlabs APT Motors")
    parser.add_argument('step', metavar = 's', nargs = '+')
    parser.add_argument('degree', metavar ='d', nargs = '+')
    args = parser.parse_args()
    moveR(args.degree[0], args.step[0])
    #print(arg.degree[0])

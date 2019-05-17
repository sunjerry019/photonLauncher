import sys, os, json
import time

sys.path.insert(0,'../helpers')

from mjolnir import Mjolnir

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('s', type = int)
args = parser.parse_args()

m = Mjolnir()
print args.s
#print "imagine that the motor moved a little"
m.moveRotMotor(args.s)

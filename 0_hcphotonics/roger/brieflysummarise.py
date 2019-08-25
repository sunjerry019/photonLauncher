from __future__ import division
import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)
from mjolnir import Mjolnir
import numpy as np
import time
import serial
import argparse

"""
move 0.050 micron for like, 200 times?
then take 10e4 readings
and then move again
"""

parser = argparse.ArgumentParser()
parser.add_argument("n_readings", type = int, help = "No. of readings to take")
parser.add_argument("n_steps", type = int, help = "No. of steps")
parser.add_argument("stepsize", type = int, help = "Size of step in mm")
#parser.add_argument("-fn", "--filename", type = str, help = "")

args = parser.parse_args()

def main(N_steps, stepsize, N_readings):

    motor = Mjolnir()
    light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)

    data = []

    f = open("data_{}".format(time.strftime("%Y%m%d_%H%M")),'w')

    for i in xrange(N):
        print "moving motor"
        motor.moveLinMotor(stepsize)
        j = []
        for _ in xrange(N_readings):
            x = light.readline()
            x = x.strip()
            #print(x)
            try:
                x = float(x)
                j.append(x)
            except:
                pass
    #        j.append(x)
        j = np.array(j)
        print(np.mean(j))
        z = (i, np.mean(j),np.std(j))
        f.write("{}\t{}\t{}\n".format(i, z[1], z[2]))

main(args.n_steps, args.stepsize, args.n_readings)

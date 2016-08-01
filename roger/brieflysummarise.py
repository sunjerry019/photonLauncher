from __future__ import division
import sys
sys.path.insert(0, "../helpers")
from mjolnir import Mjolnir
import numpy as np
import time
import serial
"""
move 0.050 micron for like, 200 times?
then take 10e4 readings
and then move again
"""

N = 500

motor = Mjolnir()
light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)

data = []

f = open("data_{}".format(time.strftime("%Y%m%d_%H%M")),'w')

for i in xrange(N):
    print "moving motor"
    motor.moveLinMotor(0.050)
    j = []
    for _ in xrange(1000000):
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

import sys
sys.path.insert(0, "../helpers")
from mjolnir import Mjolnir
import numpy as np
import time

"""
move 0.050 micron for like, 200 times?
then take 10e4 readings
and then move again
"""

N = 5

motor = Mjolnir()
light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)

data = []

f = open("data_{}".format(time.strftime("%Y%m%d_%H%M")),'w')

for i in xrange(N):
    motor.moveLinMotor(0.050)
    j = []
    for _ in xrange(10e4):
        x = light.readline()
        x = x.strip()
        x = float(x)
        j.append(x)
    z = (i, np.mean(j),np.std(j))
    f.write("{}\t{}\t{}\n".format(i, z[0], z[1]))

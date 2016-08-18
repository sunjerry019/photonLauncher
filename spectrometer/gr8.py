import sys
import serial
sys.path.insert(0, '../helpers')
from mjolnir import Mjolnir
import numpy as np
import time
kek = Mjolnir()

kek.moveRotMotor(5)
light = serial.Serial(port = '/dev/ttyACM0', baudrate=19200,parity='N',stopbits=1,bytesize=8)
data = []
fn = time.strftime("%Y%m%d_%H%M"))
f  = open("{}".format(fn, "w")
g = open("rawspec_{}".format(fn), "w")
for j in xrange(1000):
    try:
        kek.moveRotMotor(-0.01)
        zz = []
        for i in xrange(10000):
            x = light.readline()
            x = x.strip()
            try:
                x = float(x)
            except:
                print x
                continue
            zz.append(x)
        data.append(np.array(zz))

    except KeyboardInterrupt:
        break

print "writing to file"

c = 0
for i in data:
    f.write("{}\t{}\t{}\n".format(c, np.mean(i), np.std(i)))
    c += 1
c = 0
for j in data:
    g.write("{}\t".format(c))
    for k in j:
        g.write("{}\t".format(k))
    g.write("\n")
    c += 1
kek.moveRotMotor(5)

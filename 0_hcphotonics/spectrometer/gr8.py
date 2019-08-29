import sys, os
import serial
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)
from mjolnir import Mjolnir
import numpy as np
import time
kek = Mjolnir()
import shutil

kek.moveRotMotor(500)


window = [0] * 10

#N =
n_readings = 110

#dtheta = 2.0/N
a = 0.00890
b = 0.01

light = serial.Serial(port = '/dev/ttyACM0', baudrate=19200,parity='N',stopbits=1,bytesize=8)
data = []
fn = time.strftime("%Y%m%d_%H%M")
f  = open("{}".format(fn), "w")
g = open("rawspec_{}".format(fn), "w")
for j in xrange(int(1000)):
    print j
    try:
        kek.moveRotMotor(-1)
#        time.sleep(1)
        #kek.moveRotMotor(5)
        #time.sleep(5)
        zz = []
        for i in xrange(n_readings):
            x = light.readline()
            x = x.strip()
            try:

                x = float(x)
                print x
                x = a*x + b
            except:
                print x
                continue
            window.append(x)
            window.pop(0)
            if i > 10:
                zz.append(np.mean(window))
        data.append(np.array(zz))

    except:
        break

#print "writing to file"


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
kek.moveRotMotor(500)


f.close()
g.close()
#time.sleep(10)
dest = "/home/photon/Dropbox/flash"

shutil.copy(fn, dest)

print "copied file to dropbox"

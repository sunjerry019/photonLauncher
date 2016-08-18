import sys
import serial
sys.path.insert(0, '../helpers')
from mjolnir import Mjolnir
import numpy as np
import time
kek = Mjolnir()

#kek.homeMotor()

#kek.moveRotMotor(356.5)


#time.sleep(100)

kek.moveRotMotor(5)
#kek.moveRotMotor(-10)

#time.sleep(100)
light = serial.Serial(port = '/dev/ttyACM0', baudrate=19200,parity='N',stopbits=1,bytesize=8)
data = []
f  = open("{}".format(time.strftime("%Y%m%d_%H%M")), "w")
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
        #print "writing"
        #c = 0
        #for i in data:
        #    f.write("{}\t{}\t{}\n".format(c, np.mean(i), np.std(i)))
        #    c += 1
        break 
    #print i
#data = np.array(data)

#f = open("{}".format(time.strftime("%Y%m%d_%H%M")), 'w')
print "writing to file"

c = 0
for i in data:
    
    f.write("{}\t{}\t{}\n".format(c, np.mean(i), np.std(i)))
    c += 1

kek.moveRotMotor(5)

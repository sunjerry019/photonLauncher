import serial
import time
import sys

light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)
##light.open()

log = True

c = 10e5
if log:
    f = open("photometer_{}".format(time.strftime("%Y%m%d_%H%M")), 'w')

while True:
    try:
        x = light.readline()
        x = x.strip()
        x = float(x)/256
        sys.stdout.flush()        
        sys.stdout.write("\r{}".format(x))
        if log:
            f.write("{}\n".format(x))
#        time.sleep(0.05)
        if c == 0:
            break
        else:
            c-=1
    except KeyboardInterrupt:
        if log:
            f.close()
        break
    except ValueError:
        print(x)

import serial
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("n", type = int, help = "No. of readings to take")
parser.add_argument("-f", "--log", action = store_true, help = "Use this flag to enable logging to a file.")
args = parser.parse_args()



light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)
##light.open()

log = args.log

c = args.n

if log:
    f = open("photometer_{}".format(time.strftime("%Y%m%d_%H%M")), 'w')

while True:
    try:
        x = light.readline()
        x = x.strip()
        x = float(x)
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

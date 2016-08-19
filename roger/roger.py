import serial
import time
import sys
import argparse
from Tkinter import *

root = Tk()
root.resizable(width = False, height= False)

power = StringVar()
power.set('Arbitrary Power: {}'.format(0))

l = Label(root, textvariable=var, font("Helvetica", 16))
l.pack()


parser = argparse.ArgumentParser()
parser.add_argument("n", type = int, help = "No. of readings to take")
parser.add_argument("-f", "--log", action = 'store_true', help = "Use this flag to enable logging to a file.")
args = parser.parse_args()


light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)
##light.open()

log = args.log

c = args.n
#print c
if log:
    f = open("photometer_{}".format(time.strftime("%Y%m%d_%H%M")), 'w')

#prevtime = time.time()

while True:
    try:
        x = light.readline()
        x = x.strip()
        x = float(x)
        if c % 5000 == 0:
            power.set('Power: {}'.format(x))
            root.update_idletasks()
        if log:
            f.write("{}\n".format(x))

        if c < 0:
            break
        else:
            c-=1
    except KeyboardInterrupt:
        if log:
            f.close()
        break
    except ValueError:
        print(x)

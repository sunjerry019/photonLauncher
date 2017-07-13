import serial
import time
import sys
import argparse
from Tkinter import *
import numpy as np

"""root = Tk()
root.resizable(width = False, height= False)

power = StringVar()
power.set('Arbitrary Power: {}'.format(0))

l = Label(root, textvariable=power, font=("Helvetica", 64))
l.pack()
"""

parser = argparse.ArgumentParser()
parser.add_argument("n", type = int, help = "No. of readings to take")
parser.add_argument("-f", "--log", action = 'store_true', help = "Use this flag to enable logging to a file.")
parser.add_argument("-fn", "--filename", type = str, help = "Filename")
parser.add_argument("-d", "--desc", type = str, help = "Description of data reading inside meta.info")
args = parser.parse_args()

light = serial.Serial(port = '/dev/ttyACM0',baudrate = 19200,parity = 'N',stopbits = 1,bytesize = 8)
##light.open()

log = args.log

timestr = time.strftime("%Y%m%d_%H%M")
c = args.n
#print c
if log:
    f = open("photometer_{}".format(timestr), 'w')
    if not args.desc == None:
        detailer = open("meta.info", "a")
        detailer.write("{}\t{}\n".format(timestr, args.desc))
        detailer.close()

#prevtime = time.time()

window = [0] * 100

if c == -1:
    inf = True
else:
    inf = False

print "hi"

a = 0.00890
b = 0.01

while True:
    try:
        x = light.readline()
        x = x.strip()
        x = float(x)
        window.pop(0)

        x = a * x + b # photometer scaling

        window.append(x)
        if c % 10 == 0:
            #pass
            print np.mean(window)
            #power.set('Estimated power / mW \n +/- 2% \n{0:.4f}'.format(np.mean(window)))
            #root.update_idletasks()
        if log:
            f.write("{}\n".format(str(np.mean(window))[:5]))

        if c < 0 and inf:
            continue
        elif c < 0 and not inf:
            break
        else:
            c-=1
    except KeyboardInterrupt:
        if log:
            f.close()
        break
    except ValueError:
        print(x)

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)
from getTeaspoon import Teaspoon
import argparse
import time
import matplotlib.pyplot as plt
import numpy as np

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("d", metavar = "duration", type = int, help = "Duration of acquisition and measurement in seconds. Set to -1 for infinite loop.")
    parser.add_argument("t", metavar = "time interval", type = int, help = "Time interval between each acquisition in seconds.")
    parser.add_argument("-r",  default = False, action = "store_true", help = "Flag to log data.")
    args = parser.parse_args()
    total = args.d
    dt = args.t
    log = args.r
    main(total,dt, log)
def main(total, dt,log):
    if log:
        g = open("/mnt/photonics/climate/{}".format(time.strftime("%Y%m%d_%M%S")), "w")

    data =  {
    "tempboard": [0]*90,
    "tempprobe": [0]*90,
    "humidity": [0]*90,
    }

    X = np.linspace(0,89, num=90)
    teaspoon = Teaspoon()

    zz = total/dt

    print("Time\tOnboard Temp./C \t Ext Temp./C \t Onboard humidity\n")

    while not zz  == 0:
        x0 = teaspoon.getTemperatureOnboard()
        x1 = teaspoon.getTemperatureProbe()
        h = teaspoon.getHumidity()
        data["tempboard"].append(x0)
        data["tempprobe"].append(x1)
        data["humidity"].append(h)

        for i in data:
            data[i].pop(0)
        sys.stdout.flush()
        sys.stdout.write("\r{}\t{}\t{}\t{}".format(time.strftime("%m_%d_%H%M%S"), x0, x1, h))
        sys.stdout.flush()
        if log:
            g.write("{}\t{}\t{}\n".format(zz, x1, h))
        time.sleep(dt)
        zz -= 1

init()

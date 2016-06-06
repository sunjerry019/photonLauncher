import sys
sys.path.insert(0, '../helpers/')
from getTeaspoon import Teaspoon
import argparse
import time
from collections import deque

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
    data =  [0] * 90

    teaspoon = Teaspoon()

    for i in range(total/dt):
#        f = open("test","w")

#        x = (teaspoon.getTemperature())
#        h = float(teaspoon.getHumidity())

        x0 = teaspoon.getTemperatureOnboard()
        x1 = teaspoon.getTemperatureProbe()
        h = teaspoon.getHumidity()

	data.append(x1)
        data.pop(0)
        print("\r \n Onboard temperature: {} \n External probe temperature: {} \n Onboard humidity: {}".format(x0, x1, h))

        #print(data)
        f = open("test", "w")
        for i in data:
        	f.write("{}\n".format(i))

        f.close()
        if log:
            g.write("{}\t{}\t{}\n".format(x0, x1, h))
        time.sleep(dt)


init()

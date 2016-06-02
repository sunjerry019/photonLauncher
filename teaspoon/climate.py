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
    parser.add_argument("--r", metavar = "log data", type = bool, default = False, help = "Set to true to log data.")
    args = parser.parse_args()
    total = args.d
    dt = args.t

    main(total,dt)
def main(total, dt):
    data =  [0] * 90

    teaspoon = Teaspoon()

    for i in range(total/dt):
        f = open("test","w")

        x = (teaspoon.getTemperature())

        x[0] = float(x[0])
        x[1] = float(x[1])

	data.append(x[1])
        data.pop(0)
        print("\r \n Onboard temperature: {} \n External probe temperature: {} \n Onboard humidity: {}".format(x[0], x[1], float(teaspoon.getHumidity())))

        #print(data)
        for i in data:
        	f.write("{}\n".format(i))
        	
        f.close()
        time.sleep(dt)


init()

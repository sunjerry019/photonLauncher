import sys
sys.path.insert(0, '../helpers/')
#from getTeaspoon import Teaspoon
import argparse
import time

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
    teaspoon = Teaspoon()
    print(teaspoon.test() == "0")
    print len(teaspoon.test())
    f = open("test", "w")
    for i in range(total/dt):
         x = (teaspoon.getTemperature())
         f.write("".format(x[0], x[1], teaspoon.getHumidity()))
        time.sleep(dt)


init()

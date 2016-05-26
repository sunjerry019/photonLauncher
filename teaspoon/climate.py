import sys
sys.path.insert(0, '../helpers/')
#from getTeaspoon import Teaspoon
import argparse
import time

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("d", metavar = "duration", type = int, help = "Duration of acquisition and measurement in seconds. Set to -1 for infinite loop.")
    parser.add_argument("t", metavar = "time interval", type = int, help = "Time interval between each acquisition in seconds.")
    args = parser.parse_args()
    total = args.d
    dt = args.t

    main(total,dt)
def main(total, dt):
    teaspoon = Teaspoon()
    print(teaspoon.test() == "0")
    print len(teaspoon.test())
    for i in range(total/dt):
        # print(teaspoon.getTemperature())
        time.sleep(dt)


init()

import sys
sys.path.insert(0, '../helpers/')

import subprocess
import time
import argparse
import os
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import json
import random
from collections import deque
from rpiDBUploader import rpiDBUploader

def check_dir(directory):
    if not os.path.exists(directory):
        #print("Directory {} does not exist...creating...".format(directory))
        os.makedirs(directory)

def main():
    parser = argparse.ArgumentParser(description="arthur2.py: Calls getresponse to obtain the photon from the APDs for a specified timebin. Default is 100ms per timebin. ")
    #parser.add_argument('time', metavar='t', type=int, nargs='+', help="Duration in seconds for which to record photon counts from APDs. Set to -1 to keep running until Ctrl-C is pressed.")
    parser.add_argument('total', metavar='n', type=int, help="Number of readings to record photon counts from APDs. Set to -1 to keep running until Ctrl-C is pressed.")
    parser.add_argument('--t', metavar='intTime', type=int, default=100, help='Time per bin in ms')
    parser.add_argument('-p', dest = 'plot', action = 'store_true', help = 'Use this flag to enable live plotting')
    args = parser.parse_args()

    a = Arthur(args.t, args.total, args.plot)

class Arthur():
    def __init__(self, intTime, t, plot = False):
        self.togglePlot = plot
        self.timestamp = time.strftime('%Y%m%d_%H%M%S')
        self.start_t = time.time()
        self.duration = t
        self.raw_savefp = os.path.join('data', self.timestamp)
        self.savefp = os.path.join('data', self.timestamp+'.json')
        self.intTime = intTime

        p = subprocess.Popen(['./getresponse', '-n', 'TIME{}'.format(self.intTime)], stdout = subprocess.PIPE)
        print("Time per bin set to {} ms".format(self.intTime))

        self.d1 = deque([0] * 90)
        self.d2 = deque([0] * 90)
        self.monitor = False
        self.tempfp = '.temp'
        self.tempf = open(self.tempfp, 'wb+')

        self.c = t
        if self.c == -1:
            self.monitor = True
        else:
            check_dir("data")
            print("Saving JSON to: {}".format(self.savefp))
            print("Saving raw ASCII file to: {}".format(self.raw_savefp))

        if not self.monitor:
            self.jsonoutput = open(self.savefp, 'w')
            self.rawoutput = open(self.raw_savefp, 'w')

        if self.togglePlot:
            self.initPlot()
        try:
            self.collectionManager()
        except KeyboardInterrupt:
            print("[{}] Data from acquisition {} will be lost".format(time.strftime('%Y%m%d_%H%M'), self.timestamp))

    def initSaveFile(self):
        self.data = {}
        self.data['timestamp'] = self.timestamp
        #self.data['uid'] = _genName()
        self.data['counts'] = []
        self.data['timebinsize'] = self.dt
        self.data['timeperbin'] = self.intTime
        self.data['totaltargetcounts'] = self.duration
        if not self.monitor:
            json.dump(self.data, self.jsonoutput)
            self.rawoutput.write("# {} \n".format(json.dumps(self.data)))

    def initPlot(self):
        self.p = Gnuplot.Gnuplot(debug=0)
        self.p('set ytics font "Helvetica,18"')
        self.p('set style line 1 lw 10 lc rgb "red"')
        self.p('set style line 2 lw 10 lc rgb "blue"')
        self.p.title('counter')
        self.p('set xrange [0:90]')

    def updatePlot(self):
        self.p('plot "{0}" u 1:2 w l ls 1 , "{0}" u 1:3 w l ls 2'.format(self.tempfp))

    def collectionManager(self):
        if self.c == -1:
            while True:
                self.ping()
        else:
            while self.c > 0:
                self.ping()
            self.initSaveFile()
            self.saveManager()

    def plotManager(self,data):
        def addData():
            try:
                self.d1.appendleft(data[0])
                self.d2.appendleft(data[1])
                self.d1.pop()
                self.d2.pop()
            except:
                pass
        def writeData():
            self.tempf = open(self.tempfp, 'w+')
            for i in range(len(self.d1)):
                self.tempf.write('{}\t{}\t{}\n'.format(i,self.d1[i], self.d2[i]))
            self.updatePlot()
            self.tempf.close()
        addData()
        writeData()
        self.updatePlot()

    def saveManager(self):
        self.rawoutput.close()
        self.jsonoutput.close()

        print("Data saved!")
        print("Uploading to Dropbox...")
        ssh = rpiDBUploader("apddata", "common")
        ssh.uploadFromNFS()

    def ping(self):
        proc = subprocess.Popen(['./getresponse','COUNTS?'], stdout=subprocess.PIPE)
        output = str(proc.stdout.read())
        if output == "timeout while waiting for response":
            pass
        else:
            t = time.time() - self.start_t
            data = output.rstrip("\\r\\n'").split(' ')
            data.pop(0)
            if len(data) == 3:
                try:
                    #data = map(lambda x: float(x), data)
                    data = [float(x) for x in data]
                    _data = [t, data]
                    self.c -= 1
                    dtpt = _data
                    if not self.monitor:
                        self.rawoutput.write('{}\t{}\t{}\t{}\n'.format(dtpt[0], dtpt[1][0], dtpt[1][1], dtpt[1][2]))
                        #self.data['counts'].append(_data)
                except ValueError:
                    print("Error:", data)
                    pass
            else:
                print("Empty or Incomplete data:", data)
        if self.togglePlot:
            self.plotManager(data)
        data = list(map(lambda x: float(x), data))
        data.pop()
        print("\r{}:\t{}".format(self.c + 1, data))

main()
print("== Operation Ended ==\a")

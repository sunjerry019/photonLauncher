"""
floop.py
--------
Version 0.1.1

Makes a serial connection to the Lecroy Oscilloscope, and then parsing the data into a JSON file.

The data in question, is a histogram, and in our experiment is a histogram of two-photon coincidences.

Will soon be obsolete / rewritten due to lack of flexibility. 

-zy
26 Nov 2015
"""

import serial
import time
import datetime
import os, sys
import json
import random
import argparse

def _genName():
    def _genWord(fp):
        with open(fp,'r') as f:
            w = []
            for i in f:
                w.append(i.strip())
            return w[int(round((len(w) - 1) * random.random()))]
    x = ''
    x += _genWord('./cfg/adjectives').capitalize()
    x += _genWord('./cfg/adjectives').capitalize()
    x += _genWord('./cfg/animals')
    return x

def _isInt(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
def _parse(fp):
    s = ''
    c = 0
    f = open(fp, 'rb+')
    for line in f:
        if c < 2:
            pass
        else:
            s += line
        c += 1
    s = s.split('---')
    hist = s[0]
    desc = s[1]
    def parsehist(s):
		x = s.split('\n')
		x = ''.join(x)
		x = x.strip()
		x = x.split("  ")
		x = map(lambda i: float(i), x)
		return x
    def parsedesc(s):
        s = s.split('"')
        s = s[3]
        x = s.split('\n')
        c = 0
        desc = {}
        for i in x:
            if c == 0:
                pass
            else:
				j = i.split(':')
				if not len(j) == 2:
					continue
				desc[(j[0]).lower().strip()] = j[1].strip()
            c += 1
        return desc
    def getx(hist, desc):
        h_offset = float(desc['horiz_offset']) * 10 ** 9
        h_binsize = float(desc['horiz_interval']) * 10 ** 9
        s = []
        for i in xrange(len(hist)):
            s.append([(i * h_binsize) + h_offset, hist[i]])
        return s
    desc = parsedesc(desc)
    hist = parsehist(hist)
    hist = getx(hist,desc)
    return (desc, hist)

def main():
    parser = argparse.ArgumentParser(description = "fruitScope: An interface with the Lecroy Oscilloscope")
    parser.add_argument('--time', metavar = 't',  help = "Duration of acquisition.")
    #parser.add_argument("d","--desc", help="Additional comments about the experiment in case you're interested in looking for data later.")
    #parser.add_argument("f","--filepath", help="Save to a particular (folder) path.")
    args = parser.parse_args()
    if args.time:
        fruitscope = fruitScope(args.duration[0])
    else:
        frtuiscope = fruitScope()

class fruitScope():
    def __init__(self, t = -1):
        cfg = {}
        with open('./cfg/.floop', 'r') as f:
            # get the configuration settings, only the port for now
            x = f.read()
            x = x.split('\n')
            for i in x:
                s = i.rstrip().split('=')
                try:
                    cfg[s[0]] = s[1]
                    if _isInt(s[1]):
                        cfg[s[0]] = int(s[1])
                except IndexError:
                    pass
        print "Loaded configuration file at ./cfg/.floop"
        fp = 'rawdata'
        savetime = time.strftime('%Y%m%d_%H%M')

        self.savefp = os.path.join(fp,savetime)
        self.plotdata = os.path.join('parseddata', savetime)
        self.savef = open(self.savefp, 'w')
        self.data = {}
        self.data['time'] = savetime
        #self.data['desc'] = desc
        self.data['uid'] = _genName() #unique identifier
        self.data['timebinsize'] = 2.5*(10**-11)
        self.p_savefp = os.path.join('parseddata',savetime+'.json')
        print "Raw data saved to: \t {}".format(self.savefp)
        try:
            self.scope = serial.Serial()
            self.scope.port = cfg['port']
            self.scope.baudrate = cfg['baudrate']
            self.scope.parity = cfg['parity']
            self.scope.stopbits = cfg['stopbits']
            self.scope.bytesize = cfg['bytesize']
            self.scope.timeout = cfg['timeout']
            self.scope.open()
            self.savef = open(self.savefp, 'w')
            print "Initalised serial communication. Proceeding to acquisition of histogram data."
        except:
            print "Unable to establish serial communication. Please check port settings and change configuration file accordingly. For more help, consult the documention."
            sys.exit(0)
        self.start()
    def talk(self,cmd):
        self.scope.write(cmd + chr(13))
    	while True:
    		i = self.scope.readline()
    		if len(i) <= 1:
    			self.savef.write('--- \n')
    			break
    		else:
    			self.savef.write(i[:-2] + '\n')
        #self.savef.close()
    def start(self):
        self.talk('STOP')
        self.talk('C2:INSPECT? "SIMPLE"')
        self.talk('C2:INSPECT? "WAVEDESC"')
        self.savef.close()
        (desc, hist) = _parse(self.savefp)

        self.data['desc'] = desc
        self.data['hist'] = hist

        self.plotdata = os.path.join('parseddata', self.data['time'])

        with open(self.p_savefp, 'wb+') as f:
            json.dump(self.data,f)
        with open(self.plotdata, 'wb+') as f:
            for i in xrange(len(self.data['hist'])):
                f.write('{}\t{}\n'.format(self.data['hist'][i][0], self.data['hist'][i][1]))
        print "Parsed data saved to: \t {}".format(self.p_savefp)
main()

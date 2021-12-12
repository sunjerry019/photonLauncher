#!/bin/python3

import serial
import time
import os, sys

def isInt(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

class Lecroy():
    def __init__(self, config_path = ""):
        #default configuration
        cfg = {
            "port"      : "/dev/ttyUSB0",
            "baudrate"  : 19200,
            "parity"    : "N",
            "stopbits"  : 1,
            "bytesize"  : 8,
            "timeout"   : 2,
            "rawData"   :"/home/robin/Dropbox/hbar/GhostImaging/fruitScope/rawData", 
            "parsedData":"/home/robin/Dropbox/hbar/GhostImaging/fruitScope/parsedData"
        }

        #check whether there is a configuration file lecroy.conf

        # add cfg to the init part.... 

        try:
            if config_path:
                with open(config_path, 'r') as f:
                    # get the configuration settings, only the port for now
                    x = f.read()
                    x = x.split('\n')
                    for i in x:
                        s = i.rstrip().split('=')
                        try:
                            cfg[s[0]] = s[1]
                            if isInt(s[1]):
                                cfg[s[0]] = int(s[1])
                        except IndexError:
                            pass
                print("Loaded configuration file at {}".format(config_path))
        except IOError:
            if os.path.isfile('./lecroy.conf'):
                print("Unable to read file. Using default configuration...")
            else:
                print("No configuration file found. Using default configuration...")

        savetime = time.strftime('%Y%m%d_%H%M')

        try:
            self.scope = serial.Serial()
            self.scope.port = cfg['port']
            self.scope.baudrate = cfg['baudrate']
            self.scope.parity = cfg['parity']
            self.scope.stopbits = cfg['stopbits']
            self.scope.bytesize = cfg['bytesize']
            self.scope.timeout = cfg['timeout']
            self.scope.open()
            print("Initalised serial communication...")
        except:
            print("Unable to establish serial communication. Please check port settings and change configuration file accordingly. For more help, consult the documention.")
            sys.exit(0)

    def send(self, cmd):
        """ Writes cmd to the serial channel. Returns the data as a string, with \n characters to separate the lines"""
        self.scope.write(cmd + chr(13))
        data = ''
        while True:
            i = self.scope.readline()
            if len(i) == 0:
                break
            else:
                data += i + '\n'
        return data
    def getHistogram(self, channel = 'A'): # the use of the first math channel is implicit
        """ Gets the histogram from the Lecroy. Returns a tuple of a plottable histogram, and the metadata for storage"""
        hist = self.send('T{}:INSPECT? "SIMPLE"'.format(channel))
        metadata = self.send('T{}:INSPECT? "WAVEDESC"'.format(channel))
        parsed_metadata = self._parseWaveDesc(metadata)
        parsed_hist =  self._parseData(hist, parsed_metadata)
        return (parsed_hist, parsed_metadata)

    def getWaveform(self, channel):
        """ Gets the voltage data from the Lecroy. Returns a tuple of a plottable waveform, and the metadata for storage """
        waveform = self.send('C{}:INSPECT? "SIMPLE"'.format(channel))
        metadata = self.send('C{}:INSPECT? "WAVEDESC"'.format(channel))
        metadata = self.send('C{}:INSPECT? "WAVEDESC"'.format(channel))
        metadata = self.send('C{}:INSPECT? "WAVEDESC"'.format(channel))
        print(waveform)
        print(metadata)
        parsed_metadata = self._parseWaveDesc(metadata)
        parsed_waveform = self._parseData(waveform, parsed_metadata, datatype = "waveform")
        return (parsed_waveform, parsed_metadata)

    #do note that metadata contains the x-axis data, so any measurement would require knowing the wavedesc
    def _parseWaveDesc(self, raw_metadata): 
        """ metadata is the raw wavedesc, returns a parsed dictionary with relevant formatting"""
        m = raw_metadata.split('\n')
        metadata = {}
        m.pop() # the first line is always an echo of the command used. removing.
        m.pop() # the second line is equally unhelpful
        for i in m:
            x = i.split(':')
            if not len(x) == 2:
                continue
            x[0] = x[0].strip().lower()
            try:
                x[1] = float(x[1].strip())
            except:
                x[1] = x[1].strip()
            metadata[x[0]] = x[1]
        return metadata
    def _parseData(self, data, metadata, datatype = 'histogram'):
        """ metadata should be parsed already. contains x-axis data. returns the histogram that is plottable in a list of [x,y] values"""
        h = data.split('\n')
        h.pop(0)
        h.pop(0)

        data = [] # should contain both x and y axis data
        parsed_hist = []

        h = ''.join(h).strip()
        if datatype == "histogram":
            h = h.split("  ")
        elif datatype == "waveform":
            h = h.split(" ")
        h.pop(0)
        #print h
        for i in h:
            #print i.strip()
            try:
                parsed_hist.append(float(i.strip("\n\r \"")))
            except:
                print(i)
                pass

        h_offset = metadata['horiz_offset'] # scale up by a billion, units in nanoseconds easier to read
        h_binsize = metadata['horiz_interval']

        for i in range(len(parsed_hist)):
            data.append([(i * h_binsize) + h_offset, parsed_hist[i]])

        return data
    def start(self):
        self.send('TRMD NORM')
    def stop(self):
        self.send('STOP')
    def clear(self):
        self.send('CLSW')

if __name__ == '__main__':
    s = Lecroy()
    print(s.getHistogram())

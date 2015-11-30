#!/bin/python3

import serial
import time
import datetime
import os, sys
import json
import random
import argparse

class helper:
    @staticmethod
    def isInt(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

class Lecroy():
    def __init__(self, savefile):
        _ = helper()
        #default configuration
        cfg = {
            "port"      : "/dev/ttyUSB0",
            "baudrate"  : 19200,
            "parity"    : "N",
            "stopbits"  : 1,
            "bytesize"  : 8,
            "timeout"   : 2
        }

        #check whether there is a configuration file lecroy.conf
        try:
            with open('./lecroy.conf', 'r') as f:
                # get the configuration settings, only the port for now
                x = f.read()
                x = x.split('\n')
                for i in x:
                    s = i.rstrip().split('=')
                    try:
                        cfg[s[0]] = s[1]
                        if _.isInt(s[1]):
                            cfg[s[0]] = int(s[1])
                    except IndexError:
                        pass
            print("Loaded configuration file at lecroy.conf")
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
            print("Initalised serial communication....")
            try:
                self.savef = open(savefile, 'w')
                self.savef.write("Started {}\n".format(savetime))
            except IOError:
                print("Unable to open/write to {}".format(savefile))
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
    def getHistogram(self):
        """ Gets the histogram from the Lecroy. Returns a tuple of a plottable histogram, and the metadata for storage"""
        hist = self.scope.send('TA:INSPECT? "SIMPLE"') # the use of the first math channel is implicit
        metadata = self.scope.send('TA:INSPECT? "WAVEDESC"')
        parsed_metadata = _parseWaveDesc(metadata)
        parsed_hist =  _parseHistogram(hist, parsed_metadata)
        return (parsed_hist, parsed_metadata)
    def getWaveForm(self, channel = 2):
        """ Gets the voltage data from the Lecroy. Returns a tuple of a plottable waveform, and the metadata for storage """
        pass
    def _parseWaveDesc(self, raw_metadata): #do note that metadata contains the x-axis data, so any measurement would require knowing the wavedesc
        """ metadata is the raw wavedesc, returns a parsed dictionary with relevant formatting""" 
        m = raw_metadata.split('\n')
        metadata = {}
        m.pop() # the first line is always an echo of the command used. removing.
        m.pop() # the second line is equally unhelpful
        for i in m:
            x = i.split(':')
            if not len(x) == 2:
                continue
            x[0] = x.strip().lower()
            try:
                x[1] = float(x[1].strip())
            except:
                x[1] = x[1].strip()
            metadata[x[0]] = x[1]
        return metadata
    def _parseHistogram(self, hist, metadata):
        """ metadata should be parsed already. contains x-axis data. returns the histogram that is plottable in a list of [x,y] values"""
        h = hist.split('\n')
        h.pop()
        h.pop()
        
        data = [] # should contain both x and y axis data
        
        h = ''.join(h).strip()
        h = h.split("  ")
        parsed_hist = [float(i) for i in h]
        
        h_offset = metadata['horiz_offset'] * 10 ** 9 # scale up by a billion, units in nanoseconds easier to read
        h_binsize = metadata['horiz_interval'] * 10 ** 9
        
        for i in range(len(parsed_hist)):
            data.append([(i * h_binsize) + h_offset, parsed_hist[i]])
        
        return data
    def _parseWaveForm(self, waveform, raw_metadata):
        pass
#!/bin/python3

import serial
import time
import datetime
import os, sys
import json
import random
import argparse

class basicFuncs:
    @staticmethod
    def isInt(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

class Lecroy():
    def __init__(self, savefile):
        _ = basicFuncs()
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
        """ Gets the histogram from the Lecroy, assumes that the channel for histogram is the first one (TA) """
        hist = self.scope.send('TA:INSPECT? "SIMPLE"')
        metadata = self.scope.send('TA:INSPECT? "WAVEDESC"')
    def _parseWaveDesc(self, metadata):
        pass
    def _parseHistogram(self, hist):
        pass
    def _parseWaveForm(self, waveform):
        pass

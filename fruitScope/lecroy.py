#!/bin/python3

import serial
import time
import datetime
import os, sys
import json
import random
import argparse

class _:
    def isInt(self, x):
        try:
            float(x)
            return True
        except ValueError:
            return False

class lecroy():
    def __init__(self):
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

        fp = 'rawdata'
        savetime = time.strftime('%Y%m%d_%H%M')
        return self.start()

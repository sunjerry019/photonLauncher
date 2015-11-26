#!/bin/python3

import serial
import time
import datetime
import os, sys
import json
import random
import argparse

class lecroy():
    def __init__(self):
        cfg = {}
        with open('./cfg/', 'r') as f:
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
        return self.start()

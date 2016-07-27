"""
NOTE:
-----
Meant as an interface. Import the file, and write a wrapper to access the functions inside.

This is currently under development and it is highly unlikely that further development / extensions will be implemented after the basic movement controls, as that's all I actually need. Mjolnir.talk should be sufficient, if you have access to the comunications protocol by Thorlabs on the APT software and a lot of time.

Cheers
-zy
20151107
"""
#import serial
from __future__ import division
import serial

import time
import datetime
import os, sys
import json
import random
import argparse
import binascii
import struct


def main():
    #print Mjolnir.genHeader('\x04\x43', '21', '01')
    m = Mjolnir()
class Mjolnir():
    def __init__(self):
        self.initConstants()
        self.initSerial()
    def initConstants(self):
        # wasted my time typing this
        self.const = {}
        #self.const['HOST'] = '\x01'
        #self.const['MBOARD'] = '\x11'
        #self.const['MOTOR1'] = '\x21'
        #self.const['MOTOR2'] = '\x22'
        #self.const['ENCCNT'] = 34304

        self.const['LINSCALE'] = 34304
        #self.const['ROTSCALE'] = ((0.0006)**(-1))/3600
        self.const['ROTSCALE'] = 3600/2.16
    def initSerial(self):
        cfg = {}
        with open('./cfg/.mjolnir') as f:

            x = f.read()
            if (len(x) == 0):
                pass
            x = x.split('\n')
            for i in x:
                i = i.rstrip()
                if len(i) > 1:
                    print i
                    i = i.split('=')
                    cfg[i[0]] = i[1]
                else:
                    pass
        #print cfg
        self.s = serial.Serial()
        self.s.port = cfg['port']
        self.s.baudrate = int(cfg['baudrate'])
        self.s.parity = cfg['parity']
        self.s.stopbits = int(cfg['stopbits'])
        self.s.bytesize = int(cfg['bytesize'])
        self.s.timeout = int(cfg['timeout'])
        self.s.open()

    def talk(self,x):
        x = bytearray(x)
        # where x is a bytearray
        self.s.write(x)
        while True:
            i = self.s.readline()
            if len(i) <= 1:
                break
            with open('temp', 'wb+') as f:
                f.write(i)

    def homeMotor(self):
        print "Homing Motor.."
        x = ['\x43', '\x04', '\x01', '\x00', '\x21', '\x01']
        self.talk(x)
    def moveLinMotor(self, distance):
        # distance in mm, converts to mm using pscale
        d = struct.pack('<l', int(distance * self.const['LINSCALE']))
        x = ['\x48', '\x04', '\x06', '\x00', '\xA2', '\x01', '\x01', '\x00']
        for i in d:
            x.append(i)
        self.talk(x)
    def moveRotMotor(self, distance):
        distance *= self.const['ROTSCALE']
        distance = int(distance)
        print "Moving {}".format(distance)
        d = struct.pack('<l', distance)
        x = ['\x48', '\x04', '\x06', '\x00', '\xA2', '\x01', '\x01', '\x00']
        for i in d:
            x.append(i)
        self.talk(x)
    def blink(self):
        self.talk([23, 02, 00, 00, 21, 01])

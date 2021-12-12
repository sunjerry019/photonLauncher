#!/bin/python3
"""
Written to control Thorlabs TDC01 Controller Cube (CR1-Z7, MTS50-Z8)
"""

import serial
import struct

class ThorlabsApt():
    def __init__(self, config_path = "./thorlabs_apt.conf"):

        self.config_path = config_path
        self.initConstants()
        self.initSerial()
    def initConstants(self):

        self.const = {}
        self.const['LINSCALE'] = 34304
        self.const['ROTSCALE'] = 3600/2.16
    def initSerial(self):
        cfg = {}
        with open(self.config_path) as f:
            x = f.read()
            if (len(x) == 0):
                pass
            x = x.split('\n')
            for i in x:
                i = i.rstrip()
                if len(i) > 1:
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
        print("Homing Motor..")
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
        print("Moving {}".format(distance))
        d = struct.pack('<l', distance)
        x = ['\x48', '\x04', '\x06', '\x00', '\xA2', '\x01', '\x01', '\x00']
        for i in d:
            x.append(i)
        self.talk(x)
    def absRotMotor(self,distance):
        distance *= self.const['ROTSCALE']
        distance = int(distance)
        x = ['\x50','\x04','\x06','\x00','\xA2','\x01','\x01','\x00']
        d = struct.pack('<l', distance)
        for i in d:
            x.append(i)
        self.talk(x)
    def getAbs(self):
        x = ['\x51', '\x04', '\x01', '\x00','\xA2', '\x01']
        self.talk(x)
    
    def blink(self):
        # pretty sure this never worked
        self.talk(['\x23', '\x02', '\x00', '\x00', '\x21', '\x01'])

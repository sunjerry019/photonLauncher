#!/usr/bin/env python

"""
hp66XX.py is a general scripts containing the function
to control the HP/Agilent DC power supplies model 66XX

Most of the communication happens over GPIB
via the prologix USB to GPIB converter.

"""

import glob
import serial


class GPIB(serial.Serial):
    def __init__(self, device_path=''):
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*GPIB*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

    def getresponse(self, cmd):
        self.write(cmd+'\n')
        return self.readlines()


class Agilent66XX():
    def __init__(self, GPIB, channel):
        self.gpib = GPIB
        self.channel = channel
        self.r_channel = 0

    def write(self, cmd):
        self.gpib.write('++addr {0}\n'.format(self.channel).encode('ascii'))
        self.gpib.write(cmd+'\n')

    def read(self, cmd):
        self.gpib.write('++addr {0}\n'.format(self.channel).encode('ascii'))
        return self.gpib.getresponse(cmd)

    def outp_on(self):
        self.write('OUTP ON')

    def outp_off(self):
        self.write('OUTP OFF')

    def set_cc(self):
        self.write('CURRENT:PROTECTION:STATE OFF')

    def set_v(self, value):
        self.write('VOLT {0}'.format(value))

    def set_i(self, value):
        self.write('CURR {0}'.format(value))

    def get_v(self):
        return float(self.read('MEAS:VOLT?')[0])

    def get_i(self):
        return float(self.read('MEAS:CURR?')[0])

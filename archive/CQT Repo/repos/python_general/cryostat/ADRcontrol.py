#!/usr/bin/env python3

"""
ADRcontrol.py is a general scripts containing the function to access and control all the devices used to run the
Entropy ADR cryostat.

Most of the communication happens over GPIB via the prologix USB to GPIB converter.

Main tasks implemented:

Temperatures readouts (done)
Temperature stabilization (in progress)
Recharge automation (in progress)

Devices addressed:
picowatt AVS47-IB (resistance bridge)
agilent 6651 (current driver for the magnet)
heatswitch (in progress)

"""

import time
import glob

import serial
import scipy.interpolate as sp
from numpy import genfromtxt


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


class Picowatt():
    def __init__(self, GPIB, channel):
        self.gpib = GPIB
        self.channel = channel
        self.r_channel = 0

    def res_conv(self, table_file, resistance):
        table = genfromtxt(table_file)
        f1 = sp.interp1d(table[:, 1], table[:, 0], kind='linear')
        return '{:.3f}'.format(float(f1(resistance)))

    def init(self):
        [self.write(cmd) for cmd in ['REM1', 'INP1', 'EXC2', 'RAN5']]

    def mav(self):
        while self.gpib.getresponse('++spoll')[0].strip() == '0':
            pass

    def flush(self):
        if self.gpib.getresponse('++spoll')[0].strip() == '0':
            self.read_eoi()

    def write(self, cmd):
        self.gpib.write('++addr '+str(self.channel)+'\n')
        self.gpib.write(cmd+'\n')

    def read_eoi(self):
        self.gpib.write('++read eoi\n')
        return self.gpib.readlines()

    def conf_channel(self, r_channel, range, excitation):
        self.write('SCP{0};RAN{1};EXC{2}'.format(r_channel, range, excitation))

    def read_res(self, r_channel):
        if self.r_channel != r_channel:
            self.write('MUX {0}'.format(r_channel))
            time.sleep(1)
            self.r_channel = r_channel
        self.write('ADC')
        time.sleep(.5)
        self.write('RES?')
        self.mav()
        return float(self.read_eoi()[0].split()[1])

    def read_temp(self, r_channel):
        return self.res_conv('FAA_Temp_Calib.dat', self.read_res(r_channel))


class Agilent6651():
    def __init__(self, GPIB, channel):
        self.gpib = GPIB
        self.channel = channel
        self.r_channel = 0


class PID:
    """
    Discrete PID control
    """

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point-current_value

        self.P_value = self.Kp*self.error
        self.D_value = self.Kd*( self.error-self.Derivator)
        self.Derivator = self.error

        self.Integrator += self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        I_value = self.Integrator*self.Ki

        return self.P_value+I_value+self.D_value

    def setPoint(self, set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator = 0
        self.Derivator = 0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self, P):
        self.Kp = P

    def setKi(self, I):
        self.Ki = I

    def setKd(self, D):
        self.Kd = D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator
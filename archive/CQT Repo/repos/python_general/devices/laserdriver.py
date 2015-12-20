#!/usr/bin/env python

"""
Laser driver
http://qoptics.quantumlah.org/wiki/index.php/Laser_driver#Commands_and_requests

To Do:
- Documentation


Mathias Seidler, 2015.05.05
"""

import glob
import serial

mA = 1e-3

class LaserDriver(serial.Serial):
    """
    Laser driver class
    """

    def __init__(self, device_path=''):
        """
        It requires the full path to the serial device as arguments
        """
        if device_path == '':
            print('No device path given')
            return
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

	### Properties  
    @property
    def current(self):
    	"""
    	Returns laser diode current in Amps
    	"""
    	return float(self._getresponse('current?').strip())*mA

    @current.setter
    def current(self, current):
    	"""
    	Sets current in Amps
    	"""
        mA = 1e-3
        if current>150*mA:
            print("WARNING This might be too much for the diode: {} [mA]\nBut I'll still set it".format(current/mA))
        current = int(current/1e-6)
        self.write(b'current {}\n\n'.format(current))

    @property
    def temperature(self):
        return float(self._getresponse('temp?').strip())

    @temperature.setter
    def temperature(self, temp):
    	if temp <18:
    		print('WARNING Water condesation at the laser diode might happen')
    	temp = int(temp/0.001)
    	self.write('temp {}\n\n'.format(temp)) 
	######

    def _getresponse(self, command):
        """
        function to send commands and read the response of the device.

        :param command: string containing the command. Make sure that the command implies a reply, otherwise...
        :return: the reply of the device, only the first line and stripped of the decorations
        """
        self.write(command+b';\n')
        return self.readline().strip()

    @property
    def status(self):
        return int(self._getresponse('status?'))
    
    def off(self):
    	self.write(b'off\n\n')

    def on(self):
      	self.write(b'on\n\n')
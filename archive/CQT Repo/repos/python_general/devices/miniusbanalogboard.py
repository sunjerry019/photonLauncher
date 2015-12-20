"""
Author: Mathias Seidler
Created: 2015.01.24

Description:
Wrapper class for Mini USB Analog Baords
"""

import serial
import time


class MiniUSBAnalogBoard:

    def __init__(self, device_path):
        try:
            self.MIO = serial.Serial(device_path)
            self.MIO.timeout = 1
            self.MIO.write('on\n')
        except:
            print('Connection failed')

    def _getresponse(self, cmd):
        self.MIO.write(cmd + '\n')
        return self.MIO.readlines()

    def off(self):
        self.MIO.write('off\n')

    def on(self):
        self.MIO.write('on\n')

    def set_voltage(self, channel_out=0, voltage):
        """
        Sets the voltage on one of the output channels
        """
        self.MIO.write(
            'OUT {0} {1}\r\n'.format(int(channel_out), float(voltage)))
        time.sleep(.1)

    def get_voltage(self, channel_in=0, timeout=4):
        """
        Returns the voltage apllied to a channel
        """
        start = time.time()
        end = time.time()
        while end - start <= timeout:
            try:
                self.MIO.write('in? ' + str(channel_in) + '\n')
                text = self.MIO.readline()
                value = float(text.strip())
                return value
            except ValueError:
                end = time.time()
                pass
        print('Timeout, read out failed')

    def get_all_voltages(self, timeout=4):
        """
        Returns all voltages applied to the input
        """
        start = time.time()
        end = time.time()
        while end - start <= timeout:
            try:
                self.MIO.write('ALLIN?\n')
                line = self.MIO.readline()
                numbers = [float(x) for x in line.split()]
                return numbers
            except ValueError:
                end = time.time()
                pass
        print('Timeout, read out failed')

    def print_help(self):
        """
        Prints device help to the screen
        """
        txt = [x.strip() for x in self._getresponse('help')]
        for x in txt:
            print(x)

#!/usr/bin/env python

"""

"""

import serial
import time
import select
import sys
import glob


class USB_DAC(serial.Serial):
    """
    The usb analog board is seen as an object through this class, inherited from the generic serial one.
    """

    def __init__(self, device_path=''):
        """
        Function to initialize the dac device.
        It requires the full path to the serial device as arguments, otherwise it will
        initialize the first dac found in the system
        """
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*Analog_Mini*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')
        self.write(b'on\n')

    def write_read(self, command):
        """
        function to send commands and read the response of the device.
        it contains a workaroud for the 'Unknown command' problem.
        It is a recursive function, so things can go potentially very, very bad with it.
        Use wisely.

        :param command: string containing the command. Make sure that the command implies a reply, otherwise...
        :return: the reply of the device, only the first line and stripped of the decorations
        """
        self.flush()
        self.write(command+'\n'.encode('ascii'))
        while self.inWaiting() == 0:
            pass
        output = self.readline().strip()
        if output == 'Unknown command':
            return self.write_read(command)
        else:
            return output

    def set_output(self, channel, value):
        """
        Set the voltage output for the specified channel
        :param value: the new set voltage
        :param channel: the channel to use. an in between 0 and 2
        """
        try:
            self.write(('out {0} {1:.4f}\n'.format(int(channel), float(value)).encode('ascii')))
            self.output = value
        except:
            print('The indicated device cannot be found')

    @property
    def read_v(self):
        """
        Return the voltages read from the device buffer.

        :return: an array of four floats
        """
        return [float(x) for x in self.write_read('allin?').split()]
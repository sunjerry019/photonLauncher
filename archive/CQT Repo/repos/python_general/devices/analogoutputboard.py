#!/usr/bin/env python

"""
Collection of classes and functions to interact with the analog output board
The device is described in:
http://qoptics.quantumlah.org/wiki/index.php/Multiple_analog_output_board

Jan 2015

AC
"""

import glob

import serial


class DAC(serial.Serial):
    def __init__(self,  device_path=''):
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*Analog_Output*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=1)
        except:
            print('The indicated device cannot be found')

    def _getresponse(self, command):
        """
        function to send commands and read the response of the device.
        it contains a workaroud for the 'Unknown command' problem.
        It is a recursive function, so things can go potentially very,
        very bad with it.
        Use wisely.

        :param command: string containing the command.
                    Make sure that the command implies a reply, otherwise...
        :return: the reply of the device, only the first line and stripped
                of the decorations
        """
        self.flush()
        self.write(command+'\n'.encode('ascii'))
        while self.inWaiting() == 0:
            pass
        output = self.readline().strip()
        return output

    def set(self, channel, voltage):
        # check that the parameters are consistent
        if not 0 <= channel <= 7:
            print('channel exceeds range (0 to 7)')
            return
        if not -10 <= voltage <= 10:
            print('voltage exceeds range (-10 to 10 V)')
            return
        self.write('OUT {0} {1:.3f}\n'.format(int(channel),
                                              voltage).encode('ascii'))

    def ramp(self, channel, low_v, high_v, slope):
        """
        Function added with firmware svn-4: generate a ramp.
        Slope limited to a range of 0 to 100 V/s, updated at 10kHz
        """
        self.write('RAMP {0} {1} {2} {3}\n'.format(int(channel),
                                                   low_v, high_v,
                                                   slope).encode('ascii'))

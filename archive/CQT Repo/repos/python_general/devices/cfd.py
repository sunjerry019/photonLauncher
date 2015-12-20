#!/usr/bin/env python

"""
Collection of classes and functions to interact with the
slow CFD (Constant fraction discriminator).
The device is described in:
http://qoptics.quantumlah.org/wiki/index.php/Slow_CFD_unit

Jan 2015

AC
"""

import glob

import serial


class CFD(serial.Serial):

    """
    The CFD class creates a pythonic interface to control the slow CFD
    """

    def __init__(self, device_path=''):
        """ Initialization of the CFD using the Serial class.
        If no specific device is indicated, it looks for
        the first CFD it can find.

        :param device_path: path to the serial interface of the desired CFD
        """
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*CFD*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

    def set(self, channel, new_voltage):
        new_voltage = float(new_voltage)
        if -.5 <= new_voltage <= .5:
            self.write('TRESH {0} {1}\n'.format(channel,
                                                new_voltage).encode('ascii'))
        else:
            print(
                'The input value is outside of the allowed range'.encode('ascii'))

    @property
    def threshold(self):
        """
        Reads the current value of the threshold for channels 0 and 1
        and returns them in a two elements array

        :return:
        """
        if self.inWaiting():
            self.readlines()
        th = [0, 0]
        for ch in [0, 1]:
            self.write('TRESH? {0}\n'.format(ch).encode('ascii'))
            th[ch] = self.readline().strip()
        return th


if __name__ == '__main__':
    my_cfd = CFD()
    print(my_cfd.threshold)
    my_cfd.set(0, .5)
    my_cfd.set(1, -.1)
    print(my_cfd.threshold)

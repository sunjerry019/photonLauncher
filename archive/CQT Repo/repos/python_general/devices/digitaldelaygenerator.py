"""
Author: Mathias Seidler
Created: 2015.01.20

Description:
Controls Digital delay generator cards
"""

import glob

import serial


class DigitalDelayGenerator(serial.Serial):
    def __init__(self, device_path=''):
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*Digital_Delay_Generator*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

    def _getresponse(self, cmd):
        self.write(cmd+'\n')
        return self.readlines()

    def set_delay(self, channel, delay_ns):
        """
        Sets the delay in ns. Time resolution of 10ps
        """
        delay = float(delay_ns)
        delay = round(delay, 2)
        if delay > 10.23 or delay < 0.0:
            raise ValueError('Delay time out of range (max 10ns, min 0ns)\nGiven delay time: {0}'.format(delay))
        else:
            self.write('delay,{0},{1}\n'.format(channel, float(delay)))
            print('delay,{0},{1}\n'.format(channel, float(delay)))

    def get_delay(self, channel):
        """
        Returns delay of given channel in ns
        """
        response = self._getresponse('delay?,{0}'.format(channel))
        return int(response[0].split()[0], 16)*0.01

    def print_help(self):
        """
        Prints device help to the screen
        """
        help_str = self._getresponse('help')
        txt = [x.strip() for x in help_str]
        for x in txt:
            print(x)
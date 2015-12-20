#!/usr/bin/env python

"""
Collection of functions to simplify the integration of the USB counter in Python scripts.
The corresponding device is described here:
http://qoptics.quantumlah.org/wiki/index.php/USB_counter_unit

To Do:
- Improve the counting function for  'Unknown command' error handling

Jan 2015

AC
"""

import glob

import serial


class Counter(serial.Serial):

    """
    The usb counter is seen as an object through this class,
    inherited from the generic serial one.
    """

    def __init__(self, device_path='', int_time=1000):
        """
        Function to initialize the counter device.
        It requires the full path to the serial device as arguments, otherwise it will
        initialize the first counter found in the system
        """
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*Counter*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')
        self.write('ON\n'.encode('ascii'))
        self.write('NIM\n'.encode('ascii'))
        self.set_int_time(int_time)

    def _getresponse(self, command):
        """
        function to send commands and read the response of the device.
        it contains a workaroud for the 'Unknown command' problem.
        It is a recursive function, so things can go potentially very, very bad with it.
        Use wisely.

        :param command: string containing the command.
        Make sure that the command implies a reply, otherwise...
        :return: the reply of the device,
        only the first line and stripped of the decorations
        """
        self.flush()
        self.write(command + '\n'.encode('ascii'))
        while self.inWaiting() == 0:
            pass
        output = self.readline().strip()
        if output == 'Unknown command':
            return self._getresponse(command)
        else:
            return output

    def get_int_time(self):
        """
        Retrieves the integration time set in the counter

        :return: integration time in ms, int
        """
        return int(self._getresponse('TIME?').strip())

    def set_int_time(self, integration_time):
        """
        Set the integration time for the counter
        Time set in ms
        :param integration_time: new integration time expressed in msec
        """
        try:
            self.write(
                ('time {0}\n'.format(int(integration_time)).encode('ascii')))
        except:
            print('The indicated device cannot be found')

    int_time = property(get_int_time, set_int_time)

    @property
    def counts(self):
        """
        Return the actual number of count read from the device buffer.

        :return: a three-element array of int
        """
        return [int(x) for x in self._getresponse('counts?').split()]

    def read_counts(self):
        """
        Legacy function. it is better to use the counts property
        Return the actual number of count read from the device buffer.
        It tries to cope with some buggy counter devices that don't behave properly...
        :return: a three-element array
        """
        return self._getresponse('counts?')


# def continuous_counting(counter):
#     while True:
#         print(counter.read_counts())
#         i, o, e = select.select([sys.stdin], [], [], 1)
#         if i:
#             break


if __name__ == '__main__':
    # Counter_dev = " /dev/serial/by-id/usb-Centre_for_Quantum_Technologies_USB_Counter_Ucnt-QO07F-if00-port0"
    counter = Counter()
    counter.set_int_time(100)
    print(counter.read_counts())

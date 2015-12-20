import serial
import glob
import subprocess
import USB_counter


class CFD(serial.Serial):
    def __init__(self, device_path=''):
        if device_path == '':
            device_path = glob.glob('/dev/serial/by-id/*CFD*')[0]
        try:
            serial.Serial.__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')
        self.tresh = [0, 0]

    def set(self, channel, new_voltage):
        self.write('TRESH {0} {1}\n'.format(channel, new_voltage).encode('ascii'))
        self.tresh[channel] = new_voltage

    def read_th(self):
        return self.tresh


class DAC():

    def __init__(self):
        self.dac_set_exe = '/home/qitlab/programs/usbpatgendriver/testapps/usbdacset'

    def set(self, channel, new_voltage):
        """
        Set the voltage on the USB DAC

        :param channel: channel to address
        :param new_voltage: set voltage
        """
        try:
            subprocess.check_call([self.dac_set_exe, str(channel), str(new_voltage)], stderr=subprocess.STDOUT,
                                  stdout=subprocess.PIPE)
        except Exception:
            pass


def scan_CFD():
    counter = USB_counter.Counter()

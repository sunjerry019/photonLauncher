#!/usr/bin/env python
import subprocess


class DT302():

    """
    Wrapper class to interact with the ADC in the DT302 PCI board, based on the
    program written by Christian.
    Before using check that the original program work and that
    they point to the correct boards.
    """
    cmd = '/home/qitlab/programs/dt302/apps/readallchannels_dt302'
    cmd_write = '/home/qitlab/programs/dt302/apps/dacout_dt302'

    def __init__(self):
        pass

    @property
    def read_all(self):
        """
        returns an array of floats, each one corresponding to the value
        of a channel, in order
        """
        return [float(x)
                for x
                in subprocess.check_output(self.cmd).strip().split()]

    def read_ch(self, ch=0):
        """
        returns an array of floats, each one corresponding to the value
        of a channel, in order
        """
        if isinstance(ch, int):
            return self.read_all[ch]
        else:
            return [self.read_all[x] for x in ch]

    def set_ch(self, ch, value):
        """
        Set the voltage of the an output channel of the dt302 board
        to the desired value.
        The output voltage is limited to the range [-10,10]V.
        """
        if not abs(value) <= 10:
            print('Voltage value out of range')
            return -1

        return subprocess.call([self.cmd_write,
                                ' {0} {1:.3f}'.format(int(ch), value)])


if __name__ == '__main__':
    adc = DT302()
    voltages = adc.read_all
    print['Voltage for channel {0}: {1:.3f}\n'.format(idx, volt)
          for idx, volt
          in enumerate(voltages)]

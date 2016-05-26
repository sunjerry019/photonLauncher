# wrote this in python3 oops
# install pyusb from pip
# install python-usbtmc from their github
# write the udev rules
# test script

import usbtmc

class Teaspoon():
    def __init__(self):
        self.spoon = usbtmc.Instrument(0x1313, 0x80f8)

    def ping(self, x):
        self.spoon.ask(x)

    def test(self):
        print(self.ping("*IDN?"))
        print(self.ping("*TST?"))
        self.getTemperature()
        print(self.ping("READ?"))
        print(self.ping("MEAS:TEMP?"))
        print(self.ping("MEAS:HUM?"))
        print(self.ping("CONF?"))
    def getTemperature(self):
        print(self.ping("SENS1:TEMP1:DATA?"))
        print(self.ping("SENS:TEMP1:DATA?"))
        print(self.ping("SENS:HUM:DATA?"))


def main():
    tea = Teaspoon()
    tea.test()


main():

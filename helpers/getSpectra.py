import binascii
import struct
import usb1
import os
from collections import deque

class Icecube():

    def parseWavelengths(self, x):
        with open(x) as f:
            text = f.read()
        text = text.strip().split(",")
        wavelengths = [float(y) for y in text]
        return wavelengths

    def getEEPROM(self):
        # READ EEPROM
        """
            31 EEPROM values
            0  - Serial Number
            1  - 0th order Wavelength Calibration Coefficient
            2  - 1st order Wavelength Calibration Coefficient
            3  - 2nd order Wavelength Calibration Coefficient
            4  - 3rd order Wavelength Calibration Coefficient
            5  - Stray Light Constant
            6  - 0th order non-linearity correction coefficient
            7  - 1st order non-linearity correction coefficient
            8  - 2nd order non-linearity correction coefficient
            9  - 3rd order non-linearity correction coefficient
            10 - 4th order non-linearity correction coefficient
            11 - 5th order non-linearity correction coefficient
            12 - 6th order non-linearity correction coefficient
            13 - 7th order non-linearity correction coefficient
            14 - Polynomial order of non-linearity calibration
            15 - Optical Bench Configuration: gg ff sss
                gg  = Grating #
                fff = filter wavelengths
                sss = slit size
                https://oceanoptics.com/product-details/qe-pro-custom-configured-gratings-and-wavelength-range/
            16 - USB4000 configurations: AWL V
                A = Array coating Mfg
                W = Array wavelength (VIS, UV, OFLV)
                L = L2 Lens installed
                V = CPLD Version
            17 - Autonulling information
            18 - Power-up baud Rate Value
            19-30 - User-configured
        """
        _eeprom = list()
        for i in xrange(0, 31):
            # print "Reading Byte " + str(i)
            self.icecube.bulkWrite(1, '\x05' + chr(i))
            data = self.icecube.bulkRead(1, 17)
            # bytes = [data[i:i+2] for i in xrange(0, len(data), 2)]
            retCount = len(data)
            # unpacked = struct.unpack('<' + str(retCount) +'c', data)
            # if len(unpacked) >= 2: unpacked = unpacked[2:]
            # unpacked = deque(unpacked)                          # Change the format to deque to pop from front
            unpacked = deque(struct.unpack('<' + str(retCount) +'c', data))
            if len(unpacked) > 2: unpacked.popleft(); unpacked.popleft();      # We discard the \x05 and Byte Number
            _u = list()

            while unpacked and unpacked[0] != b'\x00':                         # Discard everything after \x00
                _u.append(unpacked.popleft())

            try:                                                               # Decode to ascii if possible
                _u = "".join(_u).decode('ascii')
                _u = float(_u)
            except (UnicodeDecodeError, ValueError), e:
                pass

            _eeprom.append(_u)

        return _eeprom


    def getTemp(self):
        self.icecube.bulkWrite(1, '\x6C')
        data = self.icecube.bulkRead(1, 3)
        startByte = struct.unpack('<c', data[0:1])[0]
        if startByte == b'\x08':
            # Read successful
            ADC = struct.unpack('<h', data[1:])[0]
            return 0.003906 * ADC
        else:
            raise Exception('ADC Read unsuccessful')

    """ integrationTime is in milliseconds for convenience """
    def setIntegrationTime(self, x):
        t = struct.pack('<I', x * 1000)
        self.icecube.bulkWrite(1, '\x02'+t)

    def getSpectra(self):
        data = []
        _data = []
        self.icecube.bulkWrite(1, '\x09')
        for _ in xrange(4):
        	data.append(self.icecube.bulkRead(134, 512))
        for _ in xrange(11):
        	data.append(self.icecube.bulkRead(130, 512))
        self.icecube.bulkRead(130, 1)

        for j in xrange(len(data)):
            for i in xrange(256):
                x = data[j][2*i:(i+1)*2]
                _data.append(struct.unpack('<h', x)[0])
        return [(self.wavelengths[i], _data[i]) for i in xrange(len(self.wavelengths))]

    def __enter__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wavelengths = self.parseWavelengths(dir_path + "/.oceanOpticsWavelength")
        context = usb1.USBContext()
        self.icecube = context.openByVendorIDAndProductID(0x2457, 0x1022, skip_on_error=True)
        self.icecube.claimInterface(0)
        self.icecube.bulkWrite(1, '\x01') # init message
        self.wavelengths = wavelengths
        return self

    def __exit__(self, type, value, traceback):
        self.icecube.releaseInterface(0)
        self.icecube.close()


if __name__ == '__main__':
    a = Icecube()
    #print a.getSpectra()
    #a.close()

import binascii
import struct
import usb1
import os

class Icecube():

    def parseWavelengths(self,x):
        with open(x) as f:
            text = f.read()
        text=text.strip().split(",")
        wavelengths = [float(y) for y in text]
        return wavelengths

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

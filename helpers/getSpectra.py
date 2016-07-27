import binascii
import struct
import usb1

class Icecube():

    def parseWavelengths(self,x):
        with open(x) as f:
            text = f.read()
        text=text.strip().split(",")
        wavelengths = [float(y) for y in text]
        return wavelengths

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
        wavelengths = self.parseWavelengths("/home/photon/.wavelength")
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

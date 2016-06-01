"""
uses usb1 from libusb1 which apparently works while pyusb does not

link to github
https://github.com/vpelletier/python-libusb1

with not so useful ish documentation but it is sufficient for getting the data we need

currently need to finish the proof of concept

then a parser

then a general library to handle everything


zy
4 apr 2016

"""

# run with sudo
import binascii
import struct
import usb1
context = usb1.USBContext()

#ep 2:0x82 --> 130
#ep 6:0x86 --> 134


#init
handle = context.openByVendorIDAndProductID(0x2457, 0x1022, skip_on_error=True)
if handle is None:
	print("try running with sudo")

handle.claimInterface(0) #default interface is 0, from lsusb.

#main stuff

print(handle.bulkWrite(1, '\x01')) #init message

integrationTime = 100000 # in microseconds
t_i = struct.pack('<I', integrationTime)

print("get basic info")
print(handle.bulkWrite(1, '\x05\x00')) # get id
print(handle.bulkRead(129, 512))

print(handle.bulkWrite(1, '\x05\x01')) # get 0th order wavelength coefficient
print(handle.bulkRead(129, 512))

print(handle.bulkWrite(1, '\x05\x16')) # get configuration
print(handle.bulkRead(129, 512))

print("set int time")
print(handle.bulkWrite(1, '\x02' + t_i))

print("get spectra:")
data = []
print(handle.bulkWrite(1, '\x09'))


for i in xrange(4):
	data.append(handle.bulkRead(134, 512))
for _ in xrange(11):
	data.append(handle.bulkRead(130, 512))
print("sync packet:\n")
print(handle.bulkRead(130, 1))


print(len(data))
for j in xrange(len(data)):
	for i in xrange(256):
		x = data[j][2*i:(i+1)*2]
#		print len(x)
#		print x
		print(struct.unpack('<h', x)[0])

#f = open('.temp', 'w')
handle.releaseInterface(0)
handle.close()
#handle.exit()

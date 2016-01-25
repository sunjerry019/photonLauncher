# run with sudo
import binascii
import struct
import usb1
context = usb1.USBContext()

#init
handle = context.openByVendorIDAndProductID(0x2457, 0x1022, skip_on_error=True)
if handle is None:
	print "try running with sudo"

handle.claimInterface(0) #default interface is 0, from lsusb.

#main stuff

print handle.bulkWrite(1, 1) #init message

integrationTime = 100000 # in microseconds
t_i = struct.pack('<I', integrationTime)

print "get basic info"
print handle.bulkWrite(1, '\x05\x00') # get id
print handle.bulkRead(129, 512)

print handle.bulkWrite(1, '\x05\x01') # get 0th order wavelength coefficient
print handle.bulkRead(129, 512)

print handle.bulkWrite(1, '\x05\x16') # get configuration
print handle.bulkRead(129, 512)

print "set int time"
print handle.bulkWrite(1, '\x02' + t_i)

print "get spectra:""
print handle.bulkWrite(1, '\x09')
print handle.bulkRead(134, 512)
print handle.bulkRead(130, 512)


handle.releaseInterface(0)
handle.close()

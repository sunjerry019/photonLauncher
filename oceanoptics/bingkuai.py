# run with sudo
import binascii
import usb1
context = usb1.USBContext()

handle = context.openByVendorIDAndProductID(0x2457, 0x1022, skip_on_error=True)
if handle is None:
	print "try running with sudo"

#context.freeDeviceList()
handle.claimInterface(0) #default interface is 0, from lsusb. 

print handle.bulkWrite(1, 1)
print handle.bulkWrite(1, '\x05\x00')
print handle.bulkRead(129, 512)


handle.releaseInterface(0)
handle.close()


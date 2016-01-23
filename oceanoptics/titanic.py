#!/usr/bin/python2

# pyUSB implementation in hopes (yes, hopes) of getting data directly from USB4000 spectrometer without explicitly depending on external libraries
# refers to http://oceanoptics.com//wp-content/uploads/USB4000-OEM-Data-Sheet.pdf as to what serial data to send
# highly WIP, don't expect it to work

# quoted from the pdf file:
# Only experienced USB  programmers should attempt to interface to the USB4000 via these methods
# ahahaha :D

# who needs a backend
# muahahahahha

# zy 17 Nov 2015

import usb.core
import usb.util
import struct
import binascii
import time


def main():
#print "started"
	v_id = 0x2457
	p_id = 0x1022
	a = Iceberg(v_id, p_id)

class Iceberg():
	def __init__(self, v_id, p_id):
		#print "help"
		self.dev = usb.core.find(idVendor=v_id, idProduct = p_id)
		if self.dev is None:
			raise ValueError("Device not found")
		self.dev.set_configuration()
		self.ep = self.initConstants()
		self.testInit()
		if self.dev.is_kernel_driver_active(0):
			self.dev.detach_kernel_driver(0)
			usb.util.claim_interface(self.dev, 0)
		
	def initConstants(self):
		ep = {}
		ep['talk'] = 0x01
		ep['listen'] = 0x81
		#ep['2in'] = 0x82
		#ep['6in'] = 0x86
		#cmd = {}
		#cmd['init'] = "\x01"
		#cmd['ingt'] = "\x02"
		return ep
	def testInit(self):
		# initalise usb4000
		self.talk(bytearray(['\x01']))
		# set integration time in microseconds
		ingTime = 16969 #integration time
		x = struct.pack('<I', ingTime)
		s = ['\x02']
		for i in x:
			s.append(i)
		self.talk(bytearray(x))

		# query serial number
		r = bytearray(['\x05','0'])
		self.talk(r)
		#print self.talk(r)
		print self.listen(self.ep['listen'], 512)
		t = bytearray(['\x6C'])
		self.talk(t)
		print self.listen(self.ep['listen'], 512)
	def talk(self, msg):
		print "talking {}".format(msg)
		self.dev.write(1, msg, 1000 )
	def listen(self, port, mlen):
		self.dev.read(port, mlen, 1000)
main()

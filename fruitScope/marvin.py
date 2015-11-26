import serial
import time
import datetime
import cPickle as pickle
import os
import json
import argparse
import responses

class Marvin():
	def __init__(self):
		self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize = serial.EIGHTBITS, timeout=2)
		self.table = responses.halp
		self.remarks = responses.snark
		self.saving = False
		self.loadargs = {
		'default_dir':'./.acquisition/user',
		'fn':None
		}
		print "marvin.py started."
		print "This script is a wrapper around more crude functions that talk to a Lecroy Oscilloscope."
		print "Type '/help' into the terminal input to view more information about commands."
		print "It may or may not make snarky remarks, seeing that the name of this script hails from the classic Hitchhiker's Guide to the Galaxy. \n\n"
		print "Press Ctrl-C to stop this script"

		time.sleep(2)
		print "\n" * 50
		print "-" * 78
		self.start()
	def start(self):
		while True:
			try:
				x = raw_input('>> ')
				if self.cmdparse(x):
					self.talk(x)
			except (KeyboardInterrupt,EOFError) as e:
				print "\nWrite loop stopped, quitting."
				self.ser.close()
				break
	def talk(self, cmd):
		self.ser.write(cmd + chr(13))
		while True:
			i = self.ser.readline()
			if len(i) <= 1:
				print " -- END -- "
				if self.saving:
					self.f.write('--- \n')
				break
			if self.saving:
				self.f.write(i[:-2] + '\n')
			else:
				print i[:-2]
		return 0
	def cmdparse(self, text):
		self.cmd = ['/help', '/log','/parse','/echo','/load','/acq_hist']
		self.args = text.split(' ')
		for i in self.cmd:
			if self.args[0] == i:
				self.cmdparser(text,i)
				return 0
		return 1

	def displaydocs(self, cmd):
		print '{}:\t\t\t{}'.format('Desc.', self.table[cmd]['desc'])
		print '{}:\t\t{}'.format('Details', self.table[cmd]['details'])
		print '{}:\t\t{}'.format('Arguments', self.table[cmd]['args'])
		print '{}:\t{}'.format('Optional Arguments', self.table[cmd]['desc'])
		print '{}:\t\t\t{}'.format('E.g.', self.table[cmd]['eg'])

	def cmdparser(self,text,i):
		try:
			if i == self.cmd[0]:
				if len(self.args) == 1:
					self.displaydocs('help')
					print "List of commands: {}".format(self.cmd)
				else:
					self.displaydocs(self.args[1])
			elif i ==  self.cmd[1]:
				if self.args[1] == '1':
					if self.saving:
						print "Logging already turned on."
					else:
						self.fp = os.path.join('.','saves', time.strftime('%Y%m%d_%H%M'))
						self.f = open(self.fp, 'w')
						self.saving = True
						print "Saving to location {}".format(self.fp)
				elif self.args[1] == '0':
					if not self.saving:
						print "Logging already turned off."
					else:
						self.saving = False
						print "Stopped saving to location {}".format(self.fp)
						self.f.close()
				elif self.args[1] == 'list':
					for fn in sorted(os.listdir('./saves'), reverse = True):
						print fn
			elif i == self.cmd[2]:
				if self.args[1] == 'auto':
					print "Parse after writing automatically."
				else:
					hog.heart(self.fp)
			elif i == self.cmd[3]:
				if self.args[1] == 'on':
					self.ser.write(chr(27) + ']' + chr(13))
					print "Echoing of commands ON"
				elif self.args[1] == 'off':
					self.ser.write(chr(27) + '[' + chr(13))
					print "Echoing of commands OFF"
			elif i == self.cmd[4]:
				print "Loading file {}".format(self.args[1])
			elif i == self.cmd[5]:
				self.fp = os.path.join('.', '.acquisition','saves', time.strftime('%Y%m%d_%H%M'))
				self.f = open(self.fp, 'w')
				self.saving = True
				print "Saving to location {}".format(self.fp)
				self.talk('TA:INSPECT? "SIMPLE"')
				self.talk('TA:INSPECT? "WAVEDESC"')
		except IndexError:
			print "Command incomplete. Please refer to the help manual if unsure."

def main():
	acquire = Marvin()

main()

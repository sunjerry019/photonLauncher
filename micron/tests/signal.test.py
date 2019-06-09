#!/usr/bin/env python3

import signal
import sys
import time
import threading

class Hi():
	def __init__(self):
		signal.signal(signal.SIGINT, self.signal_handler)

		assert False

		for i in range(5000):
			print("Sleeping {}".format(i), end="\r")
			time.sleep(i)

	def signal_handler(self, signal, frame):
	    print('You pressed Ctrl+C!')
	    sys.exit(1)

try:
	x = Hi()
except Exception as e:
	 # Good this does not catch keyboardInterrupt
	print("Caught me!")
	sys.exit(0)
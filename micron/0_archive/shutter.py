#!/usr/bin/env python3
# hashbang but it's meant to be run on windows ._.

# Python Helper to control an optical shutter
# Change code here if the optical shutter set up has changed

# Current setup involves sending an audio signal from the left (or right) channel to control a microservo
# The other mono channel is left for playing a sound when rastering is almost done (NotImplemented/TODO)
# Power source = Modified USB Cable

# Made 2019, Sun Yudong, Wu Mingsong
# sunyudong [at] outlook [dot] sg, mingsongwu [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher

# Currently, playing a sound is blocking
# Need to implement option to make it non-blocking (i.e. play 2 differnet sounds at once)

import winsound

class Shutter():
	def __init__(self):
		self.close()
		self.isOpen = False

	def close(self):
		winsound.PlaySound('sounds/OFF.wav', winsound.SND_FILENAME)
		self.isOpen = False
		return True

	def open(self):
		winsound.PlaySound('sounds/ON.wav', winsound.SND_FILENAME)
		self.isOpen = True
		return True

	def __enter__(self):
		return self

	def __exit__(self, e_type, e_val, traceback):
		self.close()

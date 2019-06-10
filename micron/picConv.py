#!/usr/bin/env python3

# Script to print pictures using the NanoLab Microcontroller
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Sun Yudong
# sunyudong [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher

from PIL import Image
# Pillow reqs https://pillow.readthedocs.io/en/5.1.x/installation.html
# We use Pillow instead of OpenCV to reduce installation overhead
# This comes at the price of speed

# import micron
import numpy as np
import argparse
import os

from matplotlib import cm # For coloring of the cutting lines

import pickle


class PicConv():
	def __init__(self, filename, scale = 1, cut = 0, allowDiagonals = False, prioritizeLeft = False, frames = False, simulate = False):
		self.filename = filename
		self.scale = scale

		assert cut in (0, 1), "Invalid cut value (0 or 1)"
		self.cut = cut
		self.dontcut = self.cut ^ 1

		self.allowDiagonals = allowDiagonals
		self.prioritizeLeft = prioritizeLeft

		self.frames = frames if not simulate else True
		self.simulate = simulate

		print("Using '{}' at scale {}".format(self.filename, self.scale))
		print("Cutting {} parts".format(["Black", "White"][self.cut]))
		if self.allowDiagonals:
			print("Allow Diagonals")

	def convert(self):
		self.image = Image.open(self.filename)

		# Sanity Checks
		assert self.image.mode == '1', "Your image has mode {}. Please use a 1-bit indexed image, see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#bands".format(self.image.mode)
		# Check if size is within limits if talking directly stage
		# TODO

		self.imageArray = np.array(self.image, dtype=int)
		# self.visited = np.zeros_like(self.imageArray)
		# index as such self.visited[y, x]

		# 1 = White
		# 0 = Black

		# Main algorithm part
		# We have a function that finds the next point to cut
		# From that point, we start crawling around for neighbours based on some settings (self.directions)
		# If a right block was found, the right diagonals will be prioritized, and vice versa for the left
		# Prioritize left searches from left to right instead of right to left, helping with diagonals that points Southwest (SW)
		# Origin is top left corner

		RIGHT = (  0,  1)
		LEFT  = (  0, -1)
		UP    = ( -1,  0)
		DOWN  = (  1,  0)
		DIRSE = (  1,  1)
		DIRSW = (  1, -1)
		DIRNE = ( -1,  1)
		DIRNW = ( -1, -1)

		# Var defs
		self.shape = np.shape(self.imageArray) # (y, x)
		self.lines = []

		# These are the directions we prioritize
		if self.prioritizeLeft:
			self.directions = [LEFT, RIGHT, DOWN, DIRSW, DIRNW, UP, DIRSE, DIRNE] if self.allowDiagonals else [LEFT, RIGHT, DOWN, UP]
		else:
			self.directions = [RIGHT, LEFT, DOWN, DIRSE, DIRNE, UP, DIRSW, DIRNW] if self.allowDiagonals else [RIGHT, LEFT, DOWN, UP]

		self.output = np.zeros_like(self.imageArray)

		# Func defs
		def find_next(self, point):
			y, x = point

			if self.prioritizeLeft:
				while y < self.shape[0]:
					x = self.shape[1] - 1
					while x >= 0:
						if self.imageArray[y, x] == self.cut:
							return (y, x)
						x -= 1
					y += 1
			else:
				while y < self.shape[0]:
					x = 0
					while x < self.shape[1]:
						if self.imageArray[y, x] == self.cut:
							return (y, x)
						x += 1
					y += 1

			return None

		def find_neighbour(self, point):
			y, x = point
			for tup in self.directions:
				coord = (y + tup[0], x + tup[1])
				# print("At {}, Looking at {} = {}".format(point, tup, self.imageArray[coord]))
				try:
					if self.imageArray[coord] == self.cut:
						if self.allowDiagonals:
							if self.prioritizeLeft:
								if tup in (LEFT, DIRSW, DIRNW):
									self.directions = [LEFT, RIGHT, DOWN, DIRSW, DIRNW, UP, DIRSE, DIRNE]
								elif tup in (RIGHT, DIRSE, DIRNE):
									self.directions = [LEFT, RIGHT, DOWN, DIRSE, DIRNE, UP, DIRSW, DIRNW]
							else:
								if tup in (LEFT, DIRSW, DIRNW):
									self.directions = [RIGHT, LEFT, DOWN, DIRSW, DIRNW, UP, DIRSE, DIRNE]
								elif tup in (RIGHT, DIRSE, DIRNE):
									self.directions = [RIGHT, LEFT, DOWN, DIRSE, DIRNE, UP, DIRSW, DIRNW]
						return coord
				except IndexError:
					pass

			return None

		if self.frames:
			self.resultCount = 0
			os.system("rm results/*")
			def print_result(self, final = False):
				# normalize the output
				# np.savetxt('test.csv', self.output, delimiter=',')
				_max = np.max(self.output)
				_output = self.output / _max if _max != 0 else self.output

				_im = Image.fromarray(np.uint8(cm.gist_ncar(_output)*255))
				if not final:
					_im.save("results/test-{}.png".format(self.resultCount))
				else:
					_im.save("test.png")
				# https://stackoverflow.com/questions/10965417/how-to-convert-numpy-array-to-pil-image-applying-matplotlib-colormap

				self.resultCount += 1
		else:
			def print_result(self, final):
				# final is there just to eat up the parameter passed in
				# normalize the output
				# np.savetxt('test.csv', self.output, delimiter=',')
				_max = np.max(self.output)
				_output = self.output / _max if _max != 0 else self.output

				_im = Image.fromarray(np.uint8(cm.gist_ncar(_output)*255))
				_im.save("test.png")
				# https://stackoverflow.com/questions/10965417/how-to-convert-numpy-array-to-pil-image-applying-matplotlib-colormap


		startPt = (0, 0) if not self.prioritizeLeft else (0, self.shape[1] - 1)
		lineNo  = 0
		currLine = []

		while True:
			if len(currLine):
				self.lines.append(currLine)
				currLine = []
			
			lineNo  += 1
			
			nextPt = find_next(self, startPt)
			if nextPt is None:
				break
			startPt  = nextPt

			print("At point ({1:>3}:{0:>3})".format(*nextPt), end='\r')

			# We first set the cell as visited
			self.imageArray[startPt] = self.dontcut
			self.output[startPt] = lineNo
			currLine.append()
			
			# We start to crawl from this pixel
			# For each pixel, we find the closest neighbour in order of priority
			# and mark as cut
			while True:
				print("At point ({:>3}:{:>3})".format(*nextPt), end='\r')
				nextPt = find_neighbour(self, nextPt)
				if nextPt is None:
					break

				self.imageArray[nextPt] = self.dontcut
				self.output[nextPt] = lineNo
				currLine.append(nextPt)
				if self.frames: 
					print_result(self)

		print_result(self, final = True)
		# self.image.format, self.image.size, self.image.mode
		# print(self.imageArray)
		print("\nDone")

		if self.simulate: 
			os.system("./generateMovie.sh")

	def print(self):
		import micron

		# Do printing here
		# Check limits
		pass

	def save(self, outputFile, protocol = pickle.HIGHEST_PROTOCOL):
		# save self.lines into a pickle file

		with open(outputFile, 'rb') as f:
			# we use the highest protocol for better compression
			# for better compatability, you may want to specify a different protocol
			# https://docs.python.org/3/library/pickle.html#pickle-protocols
			# Last version supported by Py3.4 is protocol 4

			pickle.dump(self.lines, f, protocol)

	def load(self, pickleFile):
		# Load self.lines from a pickleFile
		# We don't have to specify the protocol as it can be automatically determined

		with open(pickleFile, 'rb') as f:
			self.lines = pickle.load(f)

	def parseLines(self):
		# TODO
		pass

	def estimateTime(self, velocity):
		# You can run self.load to load any pickle files first
		
		self.velocity = velocity






def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', type = str, help = "Filename of the image")
    parser.add_argument('-s', '--scale', type = float, help = "Scale factor: 1px = how many um", default = 1)
    parser.add_argument('-c', '--cut', type = int, help = "Which color to cut: 0 = Cut Black, 1 = Cut White", default = 0)
    parser.add_argument('-d', '--allowDiagonals', help="Allow Diagonals when searching", action='store_true')
    parser.add_argument('-l', '--prioritizeLeft', help="Prioritize LTR instead of RTL searching", action='store_true')
    parser.add_argument('-f', '--frames', help="Simulate the rastering into frame. Output stored at results/test-N.png", action='store_true')
    parser.add_argument('-m', '--simulate', help="Simulate the rastering into frames and video. Output stored at results/test-N.png and videos/test.mp4. Requires ffpmeg.", action='store_true')
    args = parser.parse_args()

    x = PicConv(
    	filename = args.f, 
    	scale = args.scale, 
    	cut = args.cut, 
    	allowDiagonals = args.allowDiagonals, 
    	prioritizeLeft = args.prioritizeLeft,
    	frames = args.frames,
    	simulate = args.simulate
	)
    x.convert()

if __name__ == '__main__':
	_main()
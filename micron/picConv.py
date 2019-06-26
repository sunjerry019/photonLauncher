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
import os, sys

import micron

# from matplotlib import cm # For coloring of the cutting lines

import pickle

from extraFunctions import query_yes_no as qyn


class PicConv():
	def __init__(self, filename, scale = 1, cut = 0, allowDiagonals = False, prioritizeLeft = False, flipHorizontally = False, flipVertically = False ,frames = False, simulate = False, micronInstance = None):
		self.filename = filename
		self.scale = scale

		assert cut in (0, 1), "Invalid cut value (0 or 1)"
		self.cut = cut
		self.dontcut = self.cut ^ 1

		self.allowDiagonals = allowDiagonals
		self.prioritizeLeft = prioritizeLeft
		self.flipHorizontally = flipHorizontally
		self.flipVertically = flipVertically

		self.frames = frames if not simulate else True
		self.simulate = simulate

		self.controller = micronInstance

		print("Using '{}' at scale {}".format(self.filename, self.scale))
		print("Cutting {} parts".format(["Black", "White"][self.cut]))
		if self.allowDiagonals:
			print("Allow Diagonals")

	def convert(self):
		self.image = Image.open(self.filename)

		# Sanity Checks
		assert self.image.mode == '1', "Your image has mode {}. Please use a 1-bit indexed (mode 1) image, see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#bands. If using GIMP to convert picture to 1-bit index, ensure 'remove colour from palette' is unchecked".format(self.image.mode)
		# Check if size is within limits if talking directly stage
		# TODO

		self.imageArray = np.array(self.image, dtype=int)
		# We flip the image about the horizontal and vertical to match with stage position, if necessary
		if self.flipVertically:
			self.imageArray = np.flipud(self.imageArray)
		if self.flipHorizontally:
			self.imageArray = np.fliplr(self.imageArray)


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
			# Find the next starting point to cut
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
			# Find a neighbour of the current point to cut, if exists
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
				except IndexError as e:
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

				_im = Image.fromarray(np.uint8((_output)*255)) # cm.gist_ncar
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

				# _im = Image.fromarray(np.uint8(cm.gist_ncar(_output)*255))
				_im = Image.fromarray(np.uint8((_output)*255))
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
			startPt = nextPt

			print("At point ({1:>3}:{0:>3})".format(*nextPt), end='\r')

			# We first set the cell as visited
			self.imageArray[startPt] = self.dontcut
			self.output[startPt] = lineNo
			currLine.append(startPt)

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

	def draw(self, velocity, **kwargs):
		assert isinstance(velocity, (int, float)), "velocity must be int or float"

		if not isinstance(self.controller, micron.Micos):
			# initialize the stage
			self.controller = micron.Micos(**kwargs)

		self.controller.setvel(velocity)

		self.controller.shutter.close()

		xlim = abs(self.controller.stage.xlim[1] - self.controller.stage.xlim[0])
		ylim = abs(self.controller.stage.ylim[1] - self.controller.stage.ylim[0])

		try:
			assert self.shape[0] < ylim, "Image exceed y-limit"
			assert self.shape[1] < xlim, "Image exceed x-limit"
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			raise RuntimeError("Did you forget to load self.shape in form of y, x? Error: {}".format(e))

		# do a rmove to the (0,0) of the image and let the user move the sample to match the (0,0) point
		# checking if the image will exceed limits
		dy, dx = self.shape[0] / 2, self.shape[1] / 2
		self.controller.rmove(x = dx, y = dy)

		if not qyn("This is the (0,0) of the image. Confirm?"):
			print("Exiting...")
			sys.exit(1)

		# do a rmove to the first point of self.lines from (0,0) of the image
		dy, dx = self.lines[0][0][0], self.lines[0][0][1]
		self.controller.rmove(x = dx, y = dy)

		# then we print
		for cmd in self.commands:
			print(cmd)
			state  = cmd[0]
			rmoves = cmd[1]

			if state:
				self.controller.shutter.open()
			else:
				self.controller.setvel(400)

			for rmove in rmoves:
				self.controller.rmove(y = rmove[0], x = rmove[1])

			if state:
				self.controller.shutter.close()
			else:
				self.controller.setvel(velocity)

		self.controller.shutter.close()

	def save(self, variable, outputFile, protocol = pickle.HIGHEST_PROTOCOL):
		# save self.lines into a pickle file
		# variable can be self.lines

		with open(outputFile, 'rb') as f:
			# we use the highest protocol for better compression
			# for better compatability, you may want to specify a different protocol
			# https://docs.python.org/3/library/pickle.html#pickle-protocols
			# Last version supported by Py3.4 is protocol 4

			pickle.dump(variable, f, protocol)

	def load(self, pickleFile):
		# Load self.lines from a pickleFile
		# We don't have to specify the protocol as it can be automatically determined

		with open(pickleFile, 'rb') as f:
			return pickle.load(f)

	def parseLines(self):
		# All rmove commands
		# List of continuous lines, which are lists of commands in the format of
		# [bool , [(dy, dx), (dy, dx), ...]] where bool = laser on off state (0 = off, 1 = on)
		self.commands = []

		for i, line in enumerate(self.lines):
			# line = each segment that doesnt require laser to be closed
			# Points are in the format (y, x)

			# print(i, line)

			if i:
				# This is the 2nd line onwards
				# We need to move the laser from the previous point to the current point
				dy, dx = self.lines[i][0][0] - self.lines[i-1][-1][0], self.lines[i][0][1] - self.lines[i-1][-1][1]
				self.commands.append([0, [(dy, dx)]])

			# Greedy algorithm
			_l = [] # list of rmove commands (y, x)
			startPt = None
			prevPt = None

			lineLastCount = len(line) - 1
			for j, point in enumerate(line):
				if lineLastCount == 0:
					# There is only 1 point in the line
					_l.append([0, 0])

				if startPt is None:
					# No elements in list yet
					startPt = point
				else:
					dy, dx = point[0] - startPt[0], point[1] - startPt[1]
					if (dy != 0 and dx != 0) and (abs(dy) != abs(dx)):
						# This is no longer in a horizontal or straight line
						# This point is also not on a continous diagonal
						# We finish the line and append the rmove command:
						rdy, rdx = prevPt[0] - startPt[0], prevPt[1] - startPt[1]
						_l.append((rdy, rdx))

						# We set the end point of the previous move to the start point of the next move
						startPt = prevPt
						prevPt = point
					else:
						# It is the same line
						prevPt = point

				# Check if last point
				# print("j = ", j)
				if j == lineLastCount and j != 0:
					# We finish the line and append the rmove command:
					rdy, rdx = prevPt[0] - startPt[0], prevPt[1] - startPt[1]
					_l.append((rdy, rdx))

				# print(point, _l)

			self.commands.append([1, _l])


	def estimateTime(self, velocity):
		# You can run self.load to load any pickle files first
		# Set a different velocity when moving between points

		# close shutter and open shutter needs to wait clear

		self.velocity = velocity



def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', type = str, help = "Filename of the image")
    parser.add_argument('-s', '--scale', type = float, help = "Scale factor: 1px = how many um", default = 1)
    parser.add_argument('-c', '--cut', type = int, help = "Which color to cut: 0 = Cut Black, 1 = Cut White, Default 0", default = 0)
    parser.add_argument('-d', '--allowDiagonals', help="Allow Diagonals when searching", action='store_true')
    parser.add_argument('-H', '--flipHorizontally', help="Flip the image horizontally before converting", action='store_true')
    parser.add_argument('-V', '--flipVertically', help="Flip the image vertically before converting", action='store_true')
    parser.add_argument('-l', '--prioritizeLeft', help="Prioritize LTR instead of RTL searching. Please note that if image is horizontally flipped, LTR is really RTL.  ", action='store_true')
    parser.add_argument('-f', '--frames', help="Simulate the rastering into frame. Output stored at results/test-N.png", action='store_true')
    parser.add_argument('-m', '--simulate', help="Simulate the rastering into frames and video. Output stored at results/test-N.png and videos/test.mp4. Requires ffpmeg.", action='store_true')
    args = parser.parse_args()

    x = PicConv(
    	filename = args.f,
    	scale = args.scale,
    	cut = args.cut,
    	allowDiagonals = args.allowDiagonals,
    	prioritizeLeft = args.prioritizeLeft,
    	flipHorizontally = args.flipHorizontally,
    	flipVertically = args.flipVertically,
    	frames = args.frames,
    	simulate = args.simulate
	)
    x.convert()
    x.parseLines()

    print("\n\n x = PicConv()\n\n")

    import code; code.interact(local=locals())

if __name__ == '__main__':
	_main()

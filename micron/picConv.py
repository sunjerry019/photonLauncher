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

import platform

if platform.system() == "Linux":
	from matplotlib import cm # For coloring of the cutting lines

import pickle

from extraFunctions import query_yes_no as qyn

import datetime

# CUSTOM ERROR FOR PICCONV:
class ImageError(Exception):
    pass

class PicConv():
	def __init__(self, filename, xscale = 1, yscale = 1, cut = 0, allowDiagonals = False, prioritizeLeft = False, flipHorizontally = False, flipVertically = False ,frames = False, simulate = False, simulateDrawing = False, micronInstance = None, shutterTime = 800, GUI_Object = None, takeoverControl = False):
		# shutterTime in milliseconds
		# Set micronInstance to False instead of None to prevent using of micron

		self.filename = filename
		self.scale = {
			"x": xscale,
			"y": yscale
		}

		assert cut in (0, 1), "Invalid cut value (0 or 1)"
		self.cut = cut
		self.dontcut = self.cut ^ 1

		self.allowDiagonals = allowDiagonals
		self.prioritizeLeft = prioritizeLeft
		self.flipHorizontally = flipHorizontally
		self.flipVertically = flipVertically

		self.frames = frames if not simulate else True
		self.simulate = simulate # for frames
		self.simulateDrawing = simulateDrawing

		self.controller = micronInstance

		self.takeoverControl = takeoverControl

		print("Using '{}' at scale {}".format(self.filename, self.scale))
		print("Cutting {} parts".format(["Black", "White"][self.cut]))
		if self.allowDiagonals:
			print("Allow Diagonals")

		self.fast_velocity = 400
		self.estimatedTime = None
		self.estimatedVelocity = None
		self.shutterTime = shutterTime / 1000

		self.GUI_Object = GUI_Object

	def convert(self):
		self.image = Image.open(self.filename)

		# Sanity Checks
		assert self.image.mode == '1', "Your image has mode {}. Please use a 1-bit indexed (mode 1) image, see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#bands. If using GIMP to convert picture to 1-bit index, ensure 'remove colour from palette' is unchecked. ".format(self.image.mode)

		# Check if size is within limits if talking directly stage
		if isinstance(self.controller, micron.Micos):
			# We just check if its within stage limits
			shape = (self.image.size[0] * self.scale["x"], self.image.size[1] * self.scale["y"])

			if self.GUI_Object:
				if abs(shape[0]) > abs(self.controller.stage.xlim[1] - self.controller.stage.xlim[0]) or abs(shape[1]) > abs(self.controller.stage.ylim[1] - self.controller.stage.ylim[0]):

					self.GUI_Object.picConvWarn.emit("Image too big!", "Size ({}, {}) is bigger than stage limits\n\nX = [{}, {}],\nY = [{}, {}]".format(*shape, *self.controller.stage.xlim, *self.controller.stage.ylim))

					raise ImageError("Image too big! Size ({}, {}) is bigger than stage limits -- X = [{}, {}], Y = [{}, {}]".format(*shape, *self.controller.stage.xlim, *self.controller.stage.ylim))
			else:
				assert abs(shape[0]) <= abs(self.controller.stage.xlim[1] - self.controller.stage.xlim[0]) and abs(shape[1]) <= abs(self.controller.stage.ylim[1] - self.controller.stage.ylim[0]), "Image too big for stage."

		self.imageArray = np.array(self.image, dtype=int)
		self.GUI_Object.pDialog.setLabelText("Loaded image into array") if self.GUI_Object else None

		# We flip the image about the horizontal and vertical to match with stage position, if necessary
		if self.flipVertically:
			self.imageArray = np.flipud(self.imageArray)
			self.GUI_Object.pDialog.setLabelText("Flipped image vertically") if self.GUI_Object else None
		if self.flipHorizontally:
			self.imageArray = np.fliplr(self.imageArray)
			self.GUI_Object.pDialog.setLabelText("Flipped image horizontally") if self.GUI_Object else None


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
					while x > 0: 				# CANNOT USE >= 0
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

				if coord[0] < 0 or coord[1] < 0:
					continue # skip this one

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
						# We do not need to change otherwise
						return coord
				except IndexError as e:
					pass

			return None

		if self.frames:
			self.resultCount = 0
			if platform.system() == "Windows":
				os.system("del results/*")
			else:
				os.system("rm results/*")

			def print_result(self, final = False):
				# normalize the output
				# np.savetxt('test.csv', self.output, delimiter=',')
				_max = np.max(self.output)
				_output = self.output / _max if _max != 0 else self.output

				try:
					_im = Image.fromarray(np.uint8(cm.gist_ncar(_output)*255))
				except NameError as e:
					_im = Image.fromarray(np.uint8((_output)*255))


				if not final:
					_im.save("results/test-{}.png".format(self.resultCount))
				else:
					_im.save("picconv_test.png")
				# https://stackoverflow.com/questions/10965417/how-to-convert-numpy-array-to-pil-image-applying-matplotlib-colormap

				self.resultCount += 1
		else:
			def print_result(self, final):
				# final is there just to eat up the parameter passed in
				# normalize the output
				# np.savetxt('test.csv', self.output, delimiter=',')
				_max = np.max(self.output)
				_output = self.output / _max if _max != 0 else self.output

				try:
					_im = Image.fromarray(np.uint8(cm.gist_ncar(_output)*255))
				except NameError as e:
					_im = Image.fromarray(np.uint8((_output)*255))
				_im.save("picconv_test.png")
				# https://stackoverflow.com/questions/10965417/how-to-convert-numpy-array-to-pil-image-applying-matplotlib-colormap


		startPt = (0, 0) if not self.prioritizeLeft else (0, self.shape[1] - 1)
		lineNo  = 0
		currLine = []

		totalPtsToCrawl = np.sum(self.imageArray)
		if self.dontcut:
			# dontcut is 1 in the array
			totalPtsToCrawl = self.imageArray.size - totalPtsToCrawl

		crawledPts = 0

		while True:
			if len(currLine):
				self.lines.append(currLine)
				currLine = []

			lineNo  += 1

			nextPt = find_next(self, startPt)
			if nextPt is None:
				break
			startPt = nextPt

			self.GUI_Object.pDialog_setLabelText("At point ({1:>3}:{0:>3})".format(*nextPt)) if self.GUI_Object else None
			print("At point ({1:>3}:{0:>3})".format(*nextPt), end='\r')

			# We first set the cell as visited
			self.imageArray[startPt] = self.dontcut
			self.output[startPt] = lineNo
			currLine.append(startPt)
			crawledPts += 1
			ptg = (crawledPts/totalPtsToCrawl) * 100
			self.GUI_Object.pDialog_setValue(ptg / 2) if self.GUI_Object else None


			# We start to crawl from this pixel
			# For each pixel, we find the closest neighbour in order of priority
			# and mark as cut
			while True:
				print("At point ({:>3}:{:>3}) / ({:.1f}%)".format(*nextPt, ptg), end='\r')
				# if nextPt[0] < 0 or nextPt[1] < 0:
				# 	print("")
				# Used for catching erroronous pixels
				nextPt = find_neighbour(self, nextPt)
				if nextPt is None:
					break

				# print("{}/{}".format(crawledPts, totalPtsToCrawl))

				self.imageArray[nextPt] = self.dontcut
				self.output[nextPt] = lineNo
				currLine.append(nextPt)
				crawledPts += 1
				ptg = (crawledPts/totalPtsToCrawl) * 100
				self.GUI_Object.pDialog_setValue(ptg / 2) if self.GUI_Object else None

				# We print here because we prioritize the progress bar
				self.GUI_Object.pDialog_setLabelText("At point ({1:>3}:{0:>3})".format(*nextPt)) if self.GUI_Object else None

				if self.frames:
					print_result(self)

		print_result(self, final = True)
		# self.image.format, self.image.size, self.image.mode
		# print(self.imageArray)
		print("\nDone")

		if self.simulate and platform.system() == "Linux":
			os.system("./generateMovie.sh")

	def draw(self, velocity, **kwargs):
		assert isinstance(velocity, (int, float)), "velocity must be int or float"

		if not isinstance(self.controller, micron.Micos) and self.controller is not False:
			# initialize the stage
			self.controller = micron.Micos(**kwargs)

		gotController = isinstance(self.controller, micron.Micos)

		if gotController:
			if not self.GUI_Object or not self.takeoverControl:
				self.controller.setvel(self.fast_velocity)

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
				self.controller.rmove(x = dx * self.scale["x"], y = dy * self.scale["y"])

			# Estimate time if not yet estimated
			if self.estimatedTime is None or velocity != self.estimatedVelocity:
				self.estimateTime(velocity = velocity)

			deltaTime = datetime.timedelta(seconds = self.estimatedTime)
			if not self.GUI_Object or not self.takeoverControl:
				print("Given {} sec / shutter movement:\nEstimated time required  \t {}".format(self.shutterTime, deltaTime))
				if not qyn("This is the (0,0) of the image. Confirm?"):
					print("Exiting...")
					sys.exit(1)

			now = datetime.datetime.now()
			finish = now + deltaTime

			if self.GUI_Object:
				self.OP_Status = "Given {} sec / shutter movement:\nEstimated time required  \t {}, Est End = {}.".format(self.shutterTime, deltaTime, finish)
				self.GUI_Object.setOperationStatus(self.OP_Status)
			else:
				print("Printing starting now \t {}".format(now.strftime('%Y-%m-%d %H:%M:%S')))
				print("Given {} sec / shutter movement:\nEstimated time required  \t {}".format(self.shutterTime, deltaTime))
				print("Esimated to finish at \t {}".format(finish.strftime('%Y-%m-%d %H:%M:%S')))

		# SVGCODE
		svgLine = ["M 0,0"]
		svgMap = ["m", "l"] # 0 = off = m, 1 = on = l
		# / SVGCODE

		# do a rmove to the first point of self.lines from (0,0) of the image
		dy, dx = self.lines[0][0][0], self.lines[0][0][1]

		svgLine.append("m {},{}".format(dx * self.scale["x"], dy * self.scale["y"]))

		if gotController:
			self.controller.rmove(x = dx * self.scale["x"], y = dy * self.scale["y"])
			self.controller.setvel(velocity)

		# then we print
		totalLines = len(self.commands)
		for i, cmd in enumerate(self.commands):
			if not self.GUI_Object:
				print(cmd, "{}/{}".format(i + 1, totalLines))
			else:
				self.GUI_Object.setOperationStatus(self.OP_Status + "\nAt Segment {}/{}".format(i + 1, totalLines))

			state  = cmd[0] 	# laser on state
			rmoves = cmd[1]

			if gotController:
				if state:
					self.controller.shutter.open()
				else:
					self.controller.setvel(self.fast_velocity)

			for rmove in rmoves:
				# SVGCODE
				svgLine.append("{} {},{}".format(svgMap[state], rmove[1] * self.scale["x"], rmove[0] * self.scale["y"]))
				# / SVGCODE
				if gotController:
					self.controller.rmove(y = rmove[0] * self.scale["y"], x = rmove[1] * self.scale["x"])

			if gotController:
				if state:
					self.controller.shutter.close()
				else:
					self.controller.setvel(velocity)

		if gotController:
			self.controller.shutter.close()

		# SVGCODE
		# PRINT TO SVG
		if self.simulateDrawing:
			import svgwrite

			dl = " ".join(svgLine).strip()

			dwg = svgwrite.Drawing("test.svg", size=(str(self.shape[1]) + "px", str(self.shape[0]) + "px"))
			dwg.add(dwg.path(d=dl, stroke="#000", fill="none", stroke_width=0.5))
			dwg.save()


		# / SVGCODE

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

		totalLines = len(self.lines)

		for i, line in enumerate(self.lines):
			ptg = (i / totalLines) * 100
			self.GUI_Object.pDialog_setValue(50 + (ptg / 2)) if self.GUI_Object else None
			self.GUI_Object.pDialog_setLabelText("{} / {} Lines".format(i, totalLines)) if self.GUI_Object else None
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
			currLinePtCount = 0
			for j, point in enumerate(line):
				if lineLastCount == 0:
					# There is only 1 point in the line
					_l.append([0, 0])

				if startPt is None:
					# No elements in list yet
					startPt = point
				else:
					dy, dx = point[0] - startPt[0], point[1] - startPt[1]
					if (dy != 0 and dx != 0) and (not self.allowDiagonals or (abs(dy) != abs(dx) or abs(dy) != currLinePtCount + 1)):
						# currLinePtCount += 1 for startPt
						# This is no longer in a horizontal or straight line
						# This point is also not on a continous diagonal
						# We finish the line and append the rmove command:
						# print("RMOVE: ", startPt, prevPt, "POINT =", point)
						# print("CurrLinePtCount =", currLinePtCount)
						rdy, rdx = prevPt[0] - startPt[0], prevPt[1] - startPt[1]
						_l.append((rdy, rdx))
						currLinePtCount = 1

						# We set the end point of the previous move to the start point of the next move
						startPt = prevPt
						prevPt = point
					else:
						# It is the same line
						prevPt = point
						currLinePtCount += 1

				# Check if last point
				# print("j = ", j)
				if j == lineLastCount and j != 0:
					# We finish the line and append the rmove command:
					rdy, rdx = prevPt[0] - startPt[0], prevPt[1] - startPt[1]
					_l.append((rdy, rdx))

				# print(point, _l)

			self.commands.append([1, _l])

		self.GUI_Object.pDialog_setLabelText("Lines Parsed") if self.GUI_Object else None
		self.GUI_Object.pDialog_setValue(100) if self.GUI_Object else None
		# Set to 100% here to close the pDialog

	def estimateTime(self, velocity):
		# You can run self.load to load any pickle files first
		# Set a different velocity when moving between points

		# close shutter and open shutter needs to wait clear

		# parselines must be run first
		# WARNING: DOES NOT TAKE INTO ACCOUNT REAL TIME TO OPEN/CLOSE SHUTTER
		# WARNING: Shutter time estimated to be 1 second

		# Calculate time from the (0, 0) of the image

		assert isinstance(velocity, (int, float)), "velocity must be int or float"

		# Obtain shuttertime if running in GUI mode
		if self.GUI_Object:
			self.shutterTime = self.GUI_Object.stageControl.controller.shutter.duration / 1000

		totalTIme = 0

		# do a rmove to the first point of self.lines from (0,0) of the image
		dy, dx = self.lines[0][0][0], self.lines[0][0][1]
		totalTIme += micron.Micos.getDeltaTime(x = dx * self.scale["x"], y = dy * self.scale["y"], velocity = self.fast_velocity)

		# then we print
		prevState = None
		for cmd in self.commands:
			state  = cmd[0]
			rmoves = cmd[1]

			if state != prevState:
				totalTIme += self.shutterTime # for closing/opening shutter
				prevState = state

			for rmove in rmoves:
				vel = self.fast_velocity if not state else velocity
				totalTIme += micron.Micos.getDeltaTime(y = rmove[0] * self.scale["x"], x = rmove[1] * self.scale["y"], velocity = vel)

		self.estimatedTime = totalTIme
		self.estimatedVelocity = velocity

		return totalTIme



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

#!/usr/bin/env python3

# Script to laser cut raster squares using the Nanomaterials Lab Microcontrollers for research experiments (ie the important stuff)
# Because WMS is not very good at coding, he will proceed to define the needed functions here until yudong comes, communicates, and cleans the shit up together.
# Module to provide for raster shapes, sizes, in situ auto laser power adjustments and regular arrays of cut regions
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Wu Mingsong
# mingsongwu [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher


import micron
import playsound
import numpy as np
import math
import time
import argparse as arg

from extraFunctions import query_yes_no as qyn

# raster machine should have multiple cutting modes:
# Mode 1: default, horizontal array of squares. Parameters = number of squares, size of squares, raster speed increments, inter-square gap size, raster direction preference (sideways vs up-down).
# Mode 2:

class Raster():

    def __init__(self, kwargs, mode = 1, ):
		self.controller = micron.Micos(**kwargs)

		# Generate filename based on the serial number of the model
		self.serial = self.controller.getSerial()
		self.fn = self.generateFilename(self.serial)

	def finish(self):
		# Play sound to let user know that the action is completed
		# playsound.playsound(self.fn)
		pass


	def raster(self, velocity, xDist, yDist, rasterSettings, returnToOrigin = False):
		# Raster in a rectangle
		# rasterSettings = {
		# 	"direction": "x" || "y" || "xy", 		# Order matters here xy vs yx
		# 	"step": 1								# If set to xy, step is not necessary
		# }

		# xy/yx = Draw a rectangle with sides xDist and yDist
		# x = horizontal lines will be drawn while scanning down/up
		# y = vertical lines will be drawn while scanning right/left
		# Negative distance to raster in the opposite direction
		# Step must be positive

		# We check if everything is valid
		try:
			assert isinstance(velocity, (int, float)) , "Velocity must be integer or float"
			assert isinstance(xDist, (int, float))    , "xDist must be integer or float"
			assert isinstance(yDist, (int, float))    , "yDist must be integer or float"
			assert isinstance(rasterSettings, dict)   , "rasterSettings must be a dictionary"
			assert "direction" in rasterSettings      , "Raster direction must be in rasterSettings"
			assert isinstance(rasterSettings["direction"], str), "Invalid raster direction: {}".format(rasterSettings["direction"])

			# rastering x or y
			if len(rasterSettings["direction"]) == 1:
				assert rasterSettings["direction"] in self.controller.axes, "Invalid raster direction: {}".format(rasterSettings["direction"])
				assert "step" in rasterSettings       , "Raster step must be in rasterSettings"
				assert rasterSettings["step"] > 0     , "Step size must be positive"
			else:
				assert len(rasterSettings["direction"]) == 2 and (set(rasterSettings["direction"]) == set(self.controller.axes)), "Invalid raster direction {}".format(rasterSettings["direction"])

			# Check stage limits
			assert self.controller.stage.xlim[0] <= self.controller.stage.x + xDist <= self.controller.stage.xlim[1], "x not within limits"
			assert self.controller.stage.ylim[0] <= self.controller.stage.y + yDist <= self.controller.stage.ylim[1], "y not within limits"
		except AssertionError as e:
			raise InputError(e)


		# ACTUAL FUNCTION
		self.controller.setvel(velocity)

		# Get the current position of the stage
		oX, oY = self.controller.stage.x, self.controller.stage.y

		# Get index of the first direction to raster
		# We change to axes A and B because it could be xy or yx
		a = self.controller.axes.index(rasterSettings["direction"][0])
		b = a ^ 1
		distances = [xDist, yDist]

		# Check the raster step
		if len(rasterSettings["direction"]) > 1:
			# Rastering a square

			# Relative moves are blocking, so we can flood the FIFO stack after we are sure all commands have been cleared
			self.controller.waitClear()
			self.controller.shutter.open()
			self.controller.rmove(**{
				self.controller.axes[a]: distances[a],
				self.controller.axes[b]: 0
			})
			self.controller.rmove(**{
				self.controller.axes[a]: 0,
				self.controller.axes[b]: distances[b]
			})
			self.controller.rmove(**{
				self.controller.axes[a]: -distances[a],
				self.controller.axes[b]: 0
			})
			self.controller.rmove(**{
				self.controller.axes[a]: 0,
				self.controller.axes[b]: -distances[b]
			})
			self.controller.waitClear()
			self.controller.shutter.close()
		else:
			import datetime
			# Normal rastering
			# Since python range doesn't allow for float step sizes, we find the number of times to go raster a line
			# DO NOTE THAT THIS PROBABLY WILL CAUSE ROUNDING ERRORS
			# Floats are ROUNDED UP!

			_lines = math.ceil(abs(distances[b] / rasterSettings["step"]))
			_bDirTime = rasterSettings["step"] / velocity
			_timeperline = abs(distances[a]) / velocity + _bDirTime
			_totaltime = _lines * _timeperline - _bDirTime
			print("Total Time = ", _totaltime)
			# _sleepTime = _timeperline - 1 if _timeperline > 1 else _timeperline
			# _sleepTime = 0.85 * _timeperline # Arbitrary, will be a problem if/when the difference adds up to 1 full command

			print("Lines = ", _lines)
			print("Time/line = ", _timeperline)

			_step = -rasterSettings["step"] if distances[b] < 0 else rasterSettings["step"]

			self.controller.shutter.open()
			t0 = datetime.datetime.now()
			for i in range(_lines):
				print("Rastering line ", i)
				# If its not the first one, move B-Axis
				if i:
					self.controller.rmove(**{
						self.controller.axes[a]: 0,
						self.controller.axes[b]: _step
					})

				_q = i % 2 # switch directions for rastering every time

				self.controller.rmove(**{
					# First one moves right
					self.controller.axes[a]: distances[a] if not _q else -distances[a],
					self.controller.axes[b]: 0
				})
				# self.controller.waitClear()
				# time.sleep(_sleepTime if not i else _sleepTime - _bDirTime)
				# MOVED SLEEP TO RMOVE

			t1 = datetime.datetime.now()
			self.controller.waitClear()
			t2 = datetime.datetime.now()

			print("\nTimes = {}, {}".format(t1 - t0, t2 - t0))
			print("\nSTATUS = ",self.controller.getStatus(),"\n")
			self.controller.shutter.close()

		if returnToOrigin:
			# we /could/ use self.controller.move() but I don't really trust it
			# so...relative move
			cX, cY = self.controller.stage.x, self.controller.stage.y
			self.controller.rmove(x = oX - cX, y = oY - cY)

		self.finish()

	def drawElipse(self, x0, y0, h, k):
		# 1 = (x-x0)^2 / h^2 + (y-y0)^2 / k^2
		# Implement this somehow...?

		pass








        #

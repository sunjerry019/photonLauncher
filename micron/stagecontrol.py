#!/usr/bin/env python3

# Unless absolutely necessary, do not use self.controller.send(...)
# Implement the method in micron.py and call that instead
# Abstraction yo

# Advanced level functions combining multiple basic functions are to be implemented here
# Methods involving multiple functions in this script should generally be implemented 
# in a separate script and not implemented here, unless it is a very common function

# stage-control to interact with the NanoLab Microcontroller
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Sun Yudong
# sunyudong [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher

import micron
import playsound

class InputError(Exception):
	# Error in user input -> To be caught and flagged accordingly
	pass

class StageControl():
	def __init__(self):
		self.controller = micron.Micos()

		# Generate filename based on the serial number of the model
		self.serial = self.controller.getSerial()
		self.fn = self.generateFilename(self.serial)

	def generateFilename(self, cereal):
		# TODO!

		return "sounds/completed/raster.wav"

	def finish(self):
		# Play sound to let user know that the action is completed
		playsound.playsound(self.fn)

	def raster(self, velocity, xDist, yDist, rasterSettings):
		# Raster in a rectangle
		# rasterSettings = {
		# 	"direction": "x" || "y" || "xy", 		# Order matters here xy vs yx
		# 	"step": 1								# If set to xy, step is not necessary
		# }

		# xy/yx = Draw a rectangle with sides xDist and yDist
		# x = horizontal lines will be drawn while scanning down
		# y = vertical lines will be drawn while scanning 
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
			assert self.controller.stage.xlim[1] <= self.controller.stage.x + xDist <= self.controller.stage.xlim[1], "x not within limits"
			assert self.controller.stage.ylim[1] <= self.controller.stage.y + yDist <= self.controller.stage.ylim[1], "y not within limits"
		except AssertionError as e:
			raise InputError(e)


		# ACTUAL FUNCTION
		self.controller.setvel(velocity)

		# Check the raster step
		if len(rasterSettings["direction"]) > 1:
			# Rastering a square
			# Get index of the first direction to raster
			a = self.controller.axes.index(rasterSettings["direction"][0])
			b = a ^ 1
			distances = [xDist, yDist]

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
			self.controller.shutter.close()
		else:
			# Normal rastering
			pass

		self.finish()
		
		
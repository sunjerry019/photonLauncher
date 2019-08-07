#!/usr/bin/env python3

# tertiary Helper
# Unless absolutely necessary, do not use self.controller.send(...)
# Implement the method in micron.py and call that instead
# Abstraction yo

# Advanced level functions combining multiple basic functions are to be implemented here
# Methods involving multiple functions in this script should generally be implemented in a separate script and not implemented here, unless it is a very common function

# stage-control to interact with the NanoLab Microcontroller
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Sun Yudong, Wu Mingsong
# sunyudong [at] outlook [dot] sg, mingonsgwu [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher

# Change code here if for e.g. sounds needs to be played BEFORE the completion of the raster

import micron
import playsound
import numpy as np
import math
import time


class InputError(Exception):
	# Error in user input -> To be caught and flagged accordingly
	pass

class StageControl():
	def __init__(self, noinvertx = 1, noinverty = 1, GUI_Object = None, **kwargs):
		self.controller = micron.Micos(GUI_Object = GUI_Object, **kwargs)
		self.GUI_Object = GUI_Object
		self.noinvertx = noinvertx
		self.noinverty = noinverty
		# Generate filename based on the serial number of the model
		self.serial = self.controller.getSerial()

		# define contants
		self.UP, self.RIGHT, self.DOWN, self.LEFT = 0, 1, 2, 3

	def finishTone(self):
		#Play sound to let user know that the action is completed
		import jukebox

		j = jukebox.JukeBox()


	# implement cardinal direction movement definitions, the input cases arent actually necessary once we have buttons paired to commands on guimicro
	def rcardinal(self, direction, distance):
		if (direction == self.LEFT):
			return self.controller.rmove(x = distance * self.noinvertx, y = 0)

		elif (direction == self.RIGHT):
			return self.controller.rmove(x = -distance * self.noinvertx, y = 0)

		elif (direction == self.UP):
			return self.controller.rmove(y = distance * self.noinverty, x = 0)

		elif (direction == self.DOWN):
			return self.controller.rmove(y = -distance * self.noinverty, x = 0)
		else:
			return False

	def rdiagonal(self, distance):
		# implement drawing of diagonals
		# implement button for relative move directly
		distance /= 1.414213562373095
		self.controller.rmove(x = distance * self.invertx, y = distance * self.inverty)
		pass

	# most basic, single rectangle cut rastering
	def singleraster(self, velocity, xDist, yDist, rasterSettings, returnToOrigin = False):
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
			# Floats are ROUNDED DOWN!

			_lines = math.floor(abs(distances[b] / rasterSettings["step"]))
			_bDirTime = rasterSettings["step"] / velocity
			_timeperline = abs(distances[a]) / velocity + _bDirTime
			_totaltime = _lines * _timeperline - _bDirTime
			self.logconsole("Total Time = ", _totaltime)
			# _sleepTime = _timeperline - 1 if _timeperline > 1 else _timeperline
			# _sleepTime = 0.85 * _timeperline # Arbitrary, will be a problem if/when the difference adds up to 1 full command

			self.logconsole("Lines = ", _lines)
			self.logconsole("Time/line = ", _timeperline)

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

			self.logconsole("\nTimes = {}, {}".format(t1 - t0, t2 - t0))
			print("\nSTATUS = ",self.controller.getStatus(),"\n")
			self.controller.shutter.close()

		if returnToOrigin:
			self.controller.shutter.close()

			# we /could/ use self.controller.move() but I don't really trust it
			# so...relative move
			cX, cY = self.controller.stage.x, self.controller.stage.y
			self.controller.setvel(1000)
			self.controller.rmove(x = oX - cX, y = oY - cY)
			self.controller.setvel(velocity)

		self.finishTone()

	# overpowered, omni-potent rastering solution for both laser power and velocity
	def arrayraster(self, inivel, inipower, xcombo, ncols, xincrement, xGap, ycombo, nrows, yincrement, ygap, xDist, yDist, rasterSettings, returnToOrigin = True):

		# building parameter mother-of-all-lists (MOAL) to parse through when cutting every individual raster. Raster array will be numbered left to right top to bottom
		# info structure: <primary list> <raster1> (initial position tuple1), [velocity, power]</raster1> <raster2> (initial position tuple2), [velocity, power]</raster2> .... </primary list>

		xone = self.controller.stage.x
		yone = self.controller.stage.y

		moal = []
		nthsquare = []
		a = 0
		for b in range(1, ncols * nrows + 1):
			a += 1 if b % ncols == 0 else 0
			axe = xone + (b % ncols) * (xDist + xGap)
			why = yone + a * (yDist + yGap)

			# gui combobox setting: velocity is True, power is False
			if xcombo and ycombo:
				speed = (inivel + a * yincrement) + xincrement * (b % ncols)
				powa = inipower

			elif xcombo and not ycombo:
				speed = inivel + xincrement * (b % ncols)
				powa = inipower + yincrement * a

			elif not xcombo and not ycombo:
				speed = inivel
				powa = (inivel + a * yincrement) + xincrement * (b % ncols)

			elif not xcombo and ycombo:
				speed = inivel + yincrement * a
				powa = inipower + xincrement * (b % ncols)

			startpos = (axe , why)
			speedpowa = [speed, powa]
			nthsquare.append(startpos)
			nthsquare.append(speedpowa)
			moal.append(nthsquare)

		#TODO! have a countdown for all rastering and run timer in separate thread
		# Estimate time


		# actual rastering
		for i in range(nrows):
			for u in range(ncols):
				self.controller.Power.powerstep(moal[u + i*ncols][1][1])
				self.singleraster(velocity = moal[u + i*ncols][1][0], xDist = xDist, yDist = yDist, rasterSettings = rasterSettings, returnToOrigin = returnToOrigin)
				self.controller.setvel(500)
				self.controller.rmove(x = xGap + xDist, y = 0)

				self.logconsole('(',i,',',u,') raster completed! :D')

			self.controller.rmove(x = -ncols * (xGap + xDist), y = yDist + yGap)


		if self.GUI_Object is not None:
			self.GUI_Object.setOperationStatus("Raster Finished. Have a g8 day. Ready.")
		else:
			print('raster compeleted, have a gr8 day. Self-destruct sequence initiated (T-10).')

		self.finishTone()

	def logconsole(self, msg, printToTerm = True, **printArgs):
		if self.GUI_Object is not None:
			self.GUI_Object.setOperationStatus(msg, printToTerm, **printArgs)
		else:
			print(msg, **printArgs)


	def __enter__(self):
		return self

	def __exit__(self, e_type, e_val, traceback):
		self.controller.dev.close()

# for WMS's benefit: this allows for interactive interface for this script alone
if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--unit', type = str, help = "Unit, microstep, um, mm, cm, m, in, mil")
	parser.add_argument('-c', '--noCtrlCHandler', help="No Ctrl C Handler", action='store_true')
	parser.add_argument('-H', '--noHome', help="noHome", action='store_true')
	args = parser.parse_args()


	with StageControl(noCtrlCHandler = args.noCtrlCHandler, unit = args.unit, noHome = args.noHome) as s:
		print("\n\ns = StageControl(); s.controller for controller movements\n\n")
		# import pdb; pdb.set_trace()
		import code; code.interact(local=locals())

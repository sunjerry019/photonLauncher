#!/usr/bin/env python3
# hashbang but it's meant to be run on windows ._.

# Python primary Helper to interact with the NanoLab Microcontroller
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Sun Yudong
# sunyudong [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher

# IMPT: THIS IS A HELPER FILE
# RUNNING IT DIRECTLY YIELDS INTERACTIVE TERMINAL

# Errors to be caught: RuntimeError, NotImplementedError, AssertionError

# You can use python-sphinx to generate docs for this, but I mildly no time
# You can just get a brief idea by opening this in a modern text-editor and minimizing all the functions
# by clicking the small triangle/arrow at the side

import serial
import sys, os
import time
import signal
import json
import warnings

import traceback

import platform  	# for auto windows/linux detection

# hashtag homemade
import servos

import math

class Stage():
	DEFAULT_XLIM = [-20000, 0]
	DEFAULT_YLIM = [-20000, 0]

	def __init__(self, stageAsDict = None):
		# WARNING: THIS IS A STATIC OBJECT THAT DOES NOT DO ANY STAGE MANIPULATION
		# MEANT TO STORE LIMITS AND POSITIONING DATA OF STAGE
		# IF EXCEPTIONS INVOLVING THE STAGE MUST BE HANDLED, PLEASE HANDLE BEFORE PASSING TO THIS

		# set some default values
		# we assume stage is initialized (homed)

		# currently only supports 2-axis. To extend to 3 axis, adjust where appropriate

		# stageAsDict = property -> value
		# e.g.  { "xlim" : [-5,5] } etc.

		# Set xlim and ylim to be 2 identical value for it to automatically find the range (USE WITH CAUTION)

		self.xlim = self.DEFAULT_XLIM
		self.ylim = self.DEFAULT_YLIM
		self.x    = 0
		self.y    = 0

		if stageAsDict:
			self.update(stageAsDict)

	def __repr__(self):
		return "Stage <x [{},{}], y [{},{}]>".format(self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1])

	@property
	def position(self):
		return (self.x, self.y)

	def update(self, stageAsDict):
		if isinstance(stageAsDict, dict):
			for k, v in stageAsDict.items():
				if k.endswith("lim") and type(v) is not list:
					raise TypeError("Limit must be a list [lower, upper]")
				setattr(self, k, v)
		else:
			warnings.warn("Non-dictionary supplied to stage. Skipped: {}".format(stageAsDict))

	def setpos(self, x, y):
		# We keep track of our own coordinates
		# Coordinates replied from the stage is not very consistent

		# Check if x and y are within range and refuse to move if outside range
		assert self.xlim[0] <= x <= self.xlim[1], "Outside xrange"
		assert self.ylim[0] <= x <= self.ylim[1], "Outside yrange"

		self.x = x
		self.y = y

class Micos():
	def __init__(self,
			devConfig = None, stageConfig = None, noCtrlCHandler = False, unit = "um",
			noHome = False, shutterAbsolute = False, shutter_channel = servos.Servo.LEFTCH,
			powerAbsolute = False, GUI_Object = None, devMode = False
		):
		# stageConfig and devConfig can be a dictionary or a json filename
		# devConfig can just contain any values that differ from the default values
		# See self.help for documentation

		self.devMode = devMode

		cfg = {
			"port"      : "COM1",
			"baudrate"  : 9600, #19200,
			"parity"    : serial.PARITY_NONE,
			"stopbits"  : serial.STOPBITS_ONE,
			"bytesize"  : serial.EIGHTBITS,
			"timeout"   : 2
		}

		# https://stackoverflow.com/a/1857/3211506
		# Windows = Windows, Linux = Linux, Mac = Darwin
		if platform.system() == "Linux":
			cfg["port"] = '/dev/ttyUSB0'


		# We try to load device configuration if provided
		if devConfig:
			if type(devConfig) is str:
				with open(devConfig, 'r') as f:
					devConfig = json.load(f)

			if isinstance(devConfig, dict):
				cfg.update(devConfig)
			else:
				warnings.warn("Non-dictionary devConfig. Skipped: {}".format(devConfig))
		else:
			# We attempt to load the config from a default "config.local.json" if it exists
			base_dir = os.path.dirname(os.path.realpath(__file__))
			local_conf = os.path.join(base_dir, "config.local.json")

			if os.path.isfile(local_conf):
				try:
					with open(local_conf, 'r') as f:
						devConfig = json.load(f)
				except json.decoder.JSONDecodeError as e:
					if devMode:
						warnings.warn("Invalid local config file, not loaded!\n\nError: {}\n\n".format(e))
					else:
						raise RuntimeError("Invalid config.local.json found! Delete or correct errors!\n\nError: {}".format(e))
				else:
					# We are guaranteed its a dict
					cfg.update(devConfig)


		self.ENTER = b'\x0D' #chr(13)  # CR

		self.stage = Stage()
		if stageConfig:
			if type(stageConfig) is str:
				with open(stageConfig, 'r') as f:
					stageConfig = json.load(f)

			self.stage.update(stageConfig)

		self.units = { "microstep": 0,  "um": 1, "mm": 2, "cm": 3, "m": 4, "in": 5, "mil": 6 }
		self.axes  = ['x', 'y'] 		# Dictionaries are only ordered from python 3.6 onwards

		if not self.devMode:
			try:
				# BEGIN SERIAL SETUP
				self.dev = serial.Serial(
						port 		= cfg['port'],
						baudrate 	= cfg['baudrate'],
						parity 		= cfg['parity'],
						stopbits    = cfg['stopbits'],
						bytesize    = cfg['bytesize'],
						timeout     = cfg['timeout']
					)
				if self.dev.isOpen():
					self.dev.close()
					self.dev.open()

				time.sleep(2)
				print("Initalised serial communication")
				# END SERIAL SETUP

			except Exception as e:
				print(e)
				raise RuntimeError("Unable to establish serial communication. Please check port settings and change configuration file accordingly. For more help, consult the documention.\n\nConfig: {}\n\n{}: {}\n\n{}".format(cfg, type(e).__name__ , e, traceback.format_exc()))
				# sys.exit(0)
		else:
			warnings.warn("devmode -- No serial device will be used")

		if not noCtrlCHandler: self.startInterruptHandler()
		self.shutter = servos.Shutter(absoluteMode = shutterAbsolute, GUI_Object = GUI_Object, channel = shutter_channel)
		self.shutter.close()

		self.powerServo = servos.Power(absoluteMode = powerAbsolute, channel = shutter_channel * (-1))

		# BEGIN INITIALIZATION
		print("Stage Initialization...", end="\r")
		self.setunits(unit)
		self.setvel(200)
		self.homed = False

		if noHome:
			xl = abs(self.stage.xlim[1] - self.stage.xlim[0])
			yl = abs(self.stage.ylim[1] - self.stage.ylim[0])

			dx = max(self.stage.xlim) - xl/2
			dy = max(self.stage.ylim) - yl/2
			
			self.waitClear() # To check if microcontroller is switched on on Windows

			self.stage.setpos(x = dx, y = dy)

			warnings.warn("Stage will not be homed. Proceed with caution., set to ({}, {})".format(dx, dy), RuntimeWarning)
		else:
			print("Homing stage")
			self.homeStage()

		print("Stage Initialization Finished")
		# END INITIALIZATION

	def startInterruptHandler(self):
		# https://stackoverflow.com/a/4205386/3211506
		signal.signal(signal.SIGINT, self.KeyboardInterruptHandler)

	def KeyboardInterruptHandler(self, signal, frame):
		print("^C Detected: Aborting the FIFO stack and closing port.")
		print("Shutter will be closed as part of the aborting process.")
		self.abort()
		if not self.devMode:
			self.dev.close()
		print("Exiting")
		sys.exit(1)
		# use os._exit(1) to avoid raising any SystemExit exception

	def homeStage(self):
		# return x.send("cal") 		# DO NOT USE CAL ON RUDOLPH => there are some physical/mechanical issues
		xl = abs(self.stage.xlim[1] - self.stage.xlim[0])
		yl = abs(self.stage.ylim[1] - self.stage.ylim[0])

		if xl > 0 and yl > 0:
			# we use faster speed to home the stage
			_oV = self.velocity
			self.setvel(2000)

			# Home the stage
			self.send("rm") 			# send to maximum
			self.waitClear()
			self.setpos(max(self.stage.xlim), max(self.stage.ylim))
			self.setlimits(self.stage.xlim[0], self.stage.ylim[0], self.stage.xlim[1], self.stage.ylim[1])
			self.rmove(x = -xl/2, y = -yl/2)
			self.waitClear()

			# we set the speed back
			self.setvel(_oV)
		else:
			raise NotImplementedError("Setting the limits to zero asks the script to find the limits of the stage, which is not implemented yet.")
			# UNTESTED CODE
			# self.send("cal")
			# self.setpos(0, 0)
			# self.send("rm")
			# q = self.getpos()

		self.homed = True

	def rmove(self, x, y, noWait = False, *args, **kwargs):
		print("Delta = ({}, {})".format(x, y))

		# Relative move
		# Always call self.stage.setpos first to check limits
		# *args and **kwargs to allow passing in of waitClear

		# assertion checks
		assert isinstance(x, (int, float)), "x must be integer or float"
		assert isinstance(y, (int, float)), "y must be integer or float"

		try:
			self.stage.setpos(self.stage.x + x, self.stage.y + y) # Note this is not Micos.setpos
			ret = self.send("{} {} r".format(x, y), *args, **kwargs)

			if not self.devMode and not noWait:
				time_req = self.getDeltaTime(x = x, y = y, velocity = self.velocity)

				print("Sleeping", time_req)
				time.sleep(time_req)

			return ret
		except Exception as e:
			raise RuntimeError(e)

	def move(self, x, y, *args, **kwargs):
		# Absolute move
		# Always call self.stage.setpos first to check limits
		# *args and **kwargs to allow passing in of waitClear

		# assertion checks
		assert isinstance(x, (int, float)), "x must be integer or float"
		assert isinstance(y, (int, float)), "y must be integer or float"

		try:
			warnings.warn("This function may not work as intended. Please use with caution.", RuntimeWarning)
			self.stage.setpos(x, y) # Note this is not Micos.setpos
			return self.send("{} {} m".format(x, y), *args, **kwargs)
		except Exception as e:
			pass

	def setpos(self, x, y):
		# assertion checks
		assert isinstance(x, (int, float)), "x must be integer or float"
		assert isinstance(y, (int, float)), "y must be integer or float"

		self.stage.setpos(x, y)
		return self.send("{} {} setpos".format(x, y))

	def getpos(self):
		# IMPT THIS DOES NOT UPDATE INTERNAL TRACKING COORDS
		# returns the position as reported by the stage in the form of [x, y]
		# Empty split will split by whitespace

		if self.devMode:
			return [0, 0]

		return self.send("p", waitClear = True).strip().split()

	def setlimits(self, xmin, ymin, xmax, ymax):
		# -A1, -A2, +A1, +A2
		# ' '.join("'{0}'".format(n) for n in limits)

		# assertion checks
		assert isinstance(xmin, (int, float)), "xmin must be integer or float"
		assert isinstance(ymin, (int, float)), "ymin must be integer or float"
		assert isinstance(xmax, (int, float)), "xmax must be integer or float"
		assert isinstance(ymax, (int, float)), "ymax must be integer or float"

		self.stage.update({
				"xlim": [xmin, xmax],
				"ylim": [ymin, ymax]
			})
		return self.send("{} {} {} {} setlimit".format(xmin, ymin, xmax, ymax))

	def setunits(self, unit = "um"):
		# 0 = microstep = 1 motor revolution / 40000 steps, 1 = set to um, 2 = mm, 3 = cm, 4 = m, 5 = in, 6 = mil = 1/1000in

		un = self.units.get(unit, 1) # default to um

		# Just in case it is an invalid unit
		# If not 1, it must have found an entry in the list
		self.unit = "um" if un == 1 else unit

		self.send("{} 1 setunit".format(un)) # x-axis
		self.send("{} 2 setunit".format(un)) # y-axis
		self.send("{} 0 setunit".format(un)) # velocity

		return self.send("ge")

	def setvel(self, velocity):
		# Set velocity
		assert isinstance(velocity, (int, float)) , "velocity must be integer or float"

		self.velocity = velocity
		return self.send("{} setvel".format(velocity))

	def send(self, cmd, waitClear = False, raw = False, waitTime = None):
		if self.devMode:
			return 0

		# Writes cmd to the serial channel, returns the data as a list
		cmd = cmd.encode("ascii") + self.ENTER if not raw else cmd

		if waitTime is not None:
			time.sleep(waitTime)

		if waitClear:
			self.waitClear()

		self.dev.write(cmd)

		return self.read()

	def read(self):
		time.sleep(0.05)

		out = b''
		while self.dev.inWaiting() > 0:
			out += self.dev.read(1)

		out = out.strip().split() if len(out) else ''

		out = out[0] if len(out) else [x.strip() for x in out]

		return out if len(out) else None

	def waitClear(self):
		# we wait until all commands are done running and the stack is empty
		timeoutCount = 0
		timeoutLimit = 5
		waitTime = 0
		waitTimeLimit = 0.3
		while True:
			x = self.getStatus(0, waitTime = waitTime)
			if x is not None and x == 0:
				# print(x, " X is not None")
				break

			if x is None:
				timeoutCount += 1
				if timeoutCount >= timeoutLimit:
					timeoutCount = 0
					waitTime += 0.1

				if waitTime >= waitTimeLimit:
					raise RuntimeError("waitClear timed out, this should not happen. Did you switch on the microcontroller?")

				# We try again but quit if 2nd time still none

			print("Waiting for stack to clear...", end="\r")
			time.sleep(0.1)
		print("Waiting for stack to clear...cleared")

		return True

	def getStatus(self, digit = None, waitTime = 0):
		# Get the status of the controller

		assert digit is None or (isinstance(digit, int) and 0 <= digit <= 8), "Invalid digit"

		y = self.send("st", waitTime = waitTime)

		# print("GETSTATUS READ = ", y)

		if isinstance(y, list):
			y = y[-1]

		try:
			x = int(y)
		except Exception as e:
			# print(y, e)
			return None

		if digit is None:
			# we return the full status in a string of binary digits
			return bin(x)[2:]
		else:
			# generate bitmask
			mask = 1 << digit
			return (x & mask)

		# LSB
		# D0  1   Status current command execution
		# D1  2   Status Joystick or Handwheel
		# D2  4   Status Button A
		# D3  8   Machine Error
		# D4  16  Status speed mode
		# D5  32  Status In-Window
		# D6  64  Status setinfunc
		# D7  128 Status motor enable, safety device
		# D8  256 Joystick button
		# MSB

	def abort(self, closeShutter = True):
		# return x.send("abort")
		# Send Ctri + C + self.Enter
		# Set closeShutter to False to not close the shutter when aborting
		self.send(b"\x03\x0D", raw=True)

		if closeShutter:
			self.shutter.close()

	def getError(self):
		return self.send("ge", waitClear=True)

	def identify(self):
		# Format [Model] [HW-Rev] [SW-Rev] [Board-Sw] [Dip-Sw]
		# return Format = { ^Dict in above format }
		# Dipswitch is hex-encoded see Venus-1_Corvus_2_1.pdf pp. 297
		# DS  1 2 3 4 5 6 7 8 9 10
		# ST  1 1 0 0 0 0 1 1 1  1
		# RE >2 1|8 4 2 1|8 4 2  1<
		#     \-/ \-----/ \------/
		#      3     0       F     => 30F

		if self.devMode:
			return {
				"model": "0",
				"hw-rev": "0",
				"sw-rev": "0",
				"board-sw": "0",
				"dipswitches": "0000000000"
			}

		x = self.send("identify").split()

		ret = Dict()

		ret["model"] = x[0]
		ret["hw-rev"] = x[1]
		ret["sw-rev"] = x[2]
		ret["board-sw"] = x[3]
		ret["dip-sw"] = bin(int(x[4], 16))[2:]

		return ret

	def getSerial(self):
		# Format = YY HW SERI
		# HW = Hardware Revision
		# SERI = 4-digit serial number

		x = self.send("getserialno")
		return x if x else None

	def help(self):
		self.dipswitches = {
			1: "Baudrate Switch",
			2: "Baudrate Switch",
				# Baudrate apparently determined by Dip-Switch 1 and 2
				# I referenced the manual for Corvus, but I suspect this model is different
				# It works for now and I can't care enough to experiment
				# DS1 DS2
				# 0   0    9600
				# 0   1    19200
				# 1   0    57600
				# 1   1    115200
			3: "Closed Loop On/Off",
			6: "ON = Terminal Mode; OFF = Host Mode",
				# Terminal Mode returns the actual coordinates immediately
				# Host Mode only returns data when asked
		}

	def __enter__(self):
		return self

	def __exit__(self, e_type, e_val, traceback):
		# self.abort()
		self.dev.close()

	@staticmethod
	def getDeltaTime(x, y, velocity, shutterCycles: int = 0, shutterAbsoluteMode = True):
		# shutterCycles = number of open + number of closes
		# we wait 100% of the time required before returning to the loop
		distance = math.sqrt(x**2 + y**2) if (x and y) else abs(x + y)
		time_req = distance / velocity

		# time_req *= 1.1 # We wait 10% longer

		if shutterCycles:
			shutterDuration = servos.Shutter.DEFAULT_DURATION if shutterAbsoluteMode else servos.Shutter.NONABSOLUTE_DURATION
			time_req += shutterCycles * (shutterDuration / 1000)

		return time_req

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-H', '--noHome', help="Do not home the stage", action='store_true')
	parser.add_argument('-A', '--shutterAbsolute', help="Shutter uses absolute servo", action='store_true')
	args = parser.parse_args()

	with Micos(noHome = args.noHome, shutterAbsolute = args.shutterAbsolute) as m:
		print("\n\nm = Micos()\n\n")
		# import pdb; pdb.set_trace()
		import code; code.interact(local=locals())

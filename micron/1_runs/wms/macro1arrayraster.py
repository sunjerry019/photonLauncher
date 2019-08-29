#!/usr/bin/env python3
import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import stagecontrol
import servos

s = stagecontrol.StageControl(shutter_channel = servos.Servo.RIGHTCH, shutterAbsolute = True, noHome = True)

velocities = [25, 25]
size = (30, 30)
xgap = 30
ygap = 30

for i in velocities:
	s.singleraster(velocity = i, xDist = size[0], yDist = size[1], rasterSettings = {"direction": "y", "step": 2}, returnToOrigin = True)
	s.controller.setvel(1000)
	s.controller.rmove(x = xgap + size[0], y = 0)
	print(i,"um/s speed done")
s.controller.setvel(1000)
s.controller.rmove(x = -(xgap + size[0])*len(velocities), y = 2*ygap)

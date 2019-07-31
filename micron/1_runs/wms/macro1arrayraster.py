#!/usr/bin/env python3
import sys

sys.path.insert(0, "../../")

import stagecontrol
import shutterpowerranger

s = stagecontrol.StageControl(shutter_channel = shutterpowerranger.Servo.RIGHTCH, shutterAbsolute = True, noHome = True)

velocities = [50]
size = (30, 30)
xgap = 30
ygap = 30

for i in velocities:
	s.singleraster(velocity = i, xDist = size[0], yDist = size[1], rasterSettings = {"direction": "y", "step": 1}, returnToOrigin = True)
	s.controller.setvel(1000)
	s.controller.rmove(x = xgap + size[0], y = 0)
	print(i,"um/s speed done")
s.controller.setvel(1000)
s.controller.rmove(x = -(xgap + size[0])*len(velocities), y = 2*ygap)


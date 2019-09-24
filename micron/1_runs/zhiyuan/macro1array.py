#!/usr/bin/env python3
import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import stagecontrol
import servos

s = stagecontrol.StageControl(shutter_channel = servos.Servo.RIGHTCH, shutterAbsolute = True, noHome = True)

#velocities = [100, 75, 50, 25, 12, 6]
size = (30, 30)
xgap = 30
ygap = 30

nrow = 5

for i in range(1,6):
    speed = 10*i
	s.singleraster(velocity = speed, xDist = size[0], yDist = size[1], rasterSettings = {"direction": "y", "step": 0.5}, returnToOrigin = True)
	s.controller.setvel(1000)
	s.controller.rmove(x = xgap + size[0], y = 0)
	print(i,"um/s speed done")
    if i % nrow == 0:
        s.controller.rmove(x = -nrow*(xgap + size[0]), y = ygap + size[1])


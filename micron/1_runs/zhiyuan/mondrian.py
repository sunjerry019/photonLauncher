#!/usr/bin/env python3

# For OSCAR

import sys, os


base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import picConv, micron
import servos

import datetime

# PURELY FOR THE RUDOLPH

_MAINFILENAME = "mondrian/mondrian-fib-{}.bmp"
_VELOCITIES = [50, 100, 150, 200]
_ESTIMATEONLY = True

# 0 = lines, 1 = Top, 2 = Bottom Right, 3 = Bottom Left

testPic = picConv.PicConv(
    filename = _MAINFILENAME.format(1),
    allowDiagonals = False,
    prioritizeLeft = True,
    shutterTime = servos.Shutter.DEFAULT_DURATION,
    # simulateDrawing = True,
    # simulate = True,
    # micronInstance = False, # We only want to simulate drawing
)

for i in range(4):
    testPic.filename = _MAINFILENAME.format(i)
    testPic.convert()
    testPic.parseLines()
    if not _ESTIMATEONLY:
        testPic.draw(velocity = _VELOCITIES[i], shutterAbsolute = True, shutter_channel = servos.Servo.RIGHTCH)
        testPic.controller.homeStage()
    else:
        print(datetime.timedelta(seconds = testPic.estimateTime(velocity = _VELOCITIES[i])))

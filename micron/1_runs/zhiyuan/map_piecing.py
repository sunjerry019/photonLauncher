#!/usr/bin/env python3

# For OSCAR

import sys, os


base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import picConv, micron
import servos

from extraFunctions import query_yes_no as qyn

import datetime

# PURELY FOR THE RUDOLPH

_MAINFILENAME = "map-sections/{}.bmp"
_VELOCITIES = [50, 30, 50, 30, 50, 30, 30]
_ESTIMATEONLY = False
# 0 = lines, 1 = Top, 2 = Bottom Right, 3 = Bottom Left

mic = micron.Micos(
    shutterAbsolute = False,
    noHome = True,
    shutter_channel = servos.Servo.LEFTCH,

    stageConfig = {
                "xlim" : [-10000,0],
                "ylim" : [-10000,0],
            },
)

testPic = picConv.PicConv(
    filename = _MAINFILENAME.format(1),
    allowDiagonals = True,
    prioritizeLeft = True,
    shutterTime = servos.Shutter.DEFAULT_DURATION,
    yscale = 0.5,
    xscale = 0.5,
    micronInstance = mic,
    takeoverControl = True,
    flipVertically = True,
    # simulateDrawing= True,
)

if not _ESTIMATEONLY:
    xl = abs(testPic.controller.stage.xlim[1] - testPic.controller.stage.xlim[0])
    yl = abs(testPic.controller.stage.ylim[1] - testPic.controller.stage.ylim[0])

    testPic.controller.setlimits(testPic.controller.stage.xlim[0], testPic.controller.stage.ylim[0], testPic.controller.stage.xlim[1], testPic.controller.stage.ylim[1])
    testPic.controller.setpos(x = -xl/2, y = -yl/2)

    testPic.controller.waitClear()

    oX, oY = testPic.controller.stage.x, testPic.controller.stage.y
    testPic.homed = True

    testPic.fast_velocity = 100


for i in range(6,7):
    if not i == 0:
        testPic.controller.shutter.homeclose()
        testPic.controller.shutter.close()
        testPic.filename = _MAINFILENAME.format(i)
        testPic.convert()
        testPic.parseLines()
        if not _ESTIMATEONLY:
            testPic.draw(velocity = _VELOCITIES[i])
            cX, cY = testPic.controller.stage.x, testPic.controller.stage.y
            dx, dy = cX - oX, cY - oY
            testPic.controller.shutter.close()
            testPic.controller.setvel(100)
            testPic.controller.rmove(x = -dx, y = -dy)
            while not qyn("Next?"):
                pass
        else:
            print(datetime.timedelta(seconds = testPic.estimateTime(velocity = _VELOCITIES[i])))

#!/usr/bin/env python3

# For OSCAR

import sys

sys.path.insert(0, "../../")

import picConv, micron

import datetime

_velocity = 100

testPic = picConv.PicConv(
    filename = "robinson_big.bmp", #"Australia-NewGuinea.bmp", #
    allowDiagonals = True,
    prioritizeLeft = True,
    flipVertically = True,
    yscale = 0.5,
    xscale = 0.5
)

# RODULP

# testPic.convert()
# testPic.parseLines()
# testPic.draw(velocity = _velocity, shutterAbsolute = True)

# print(datetime.timedelta(seconds = testPic.estimateTime(velocity = _velocity))

# OSCAR

testPic.controller = micron.Micos(
    stageConfig = {
        "xlim" : [-10000,0],
        "ylim" : [-10000,0],
    },
    noHome = True,
    shutterAbsolute = True
)

testPic.controller.setvel(1000)
# testPic.controller.send("rm")
# time.sleep(2)
# testPic.controller.abort()
testPic.controller.setpos(0, 0)

xl = abs(testPic.controller.stage.xlim[1] - testPic.controller.stage.xlim[0])
yl = abs(testPic.controller.stage.ylim[1] - testPic.controller.stage.ylim[0])

testPic.controller.setlimits(testPic.controller.stage.xlim[0], testPic.controller.stage.ylim[0], testPic.controller.stage.xlim[1], testPic.controller.stage.ylim[1])
testPic.controller.rmove(x = -xl/2, y = -yl/2)

testPic.controller.waitClear()
testPic.homed = True

testPic.convert()
testPic.parseLines()
testPic.draw(velocity = _velocity)

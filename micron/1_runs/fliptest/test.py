#!/usr/bin/env python3

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import picConv, micron
import time

testPic = picConv.PicConv(
    filename = "fliptest.bmp",
    allowDiagonals = True,
)

# OSCAR = VERTICAL FLIP
# testPic.controller = micron.Micos(
#     stageConfig = {
#         "xlim" : [-10000,0],
#         "ylim" : [-10000,0],
#     },
#     noHome = True,
#     shutterAbsolute = True
# )
#
# testPic.controller.setvel(1000)
# # testPic.controller.send("rm")
# # time.sleep(2)
# # testPic.controller.abort()
# testPic.controller.setpos(0, 0)
#
# xl = abs(testPic.controller.stage.xlim[1] - testPic.controller.stage.xlim[0])
# yl = abs(testPic.controller.stage.ylim[1] - testPic.controller.stage.ylim[0])
#
# testPic.controller.setlimits(testPic.controller.stage.xlim[0], testPic.controller.stage.ylim[0], testPic.controller.stage.xlim[1], testPic.controller.stage.ylim[1])
# testPic.controller.rmove(x = -xl/2, y = -yl/2)
#
# testPic.controller.waitClear()
# testPic.homed = True

# RUDOLPH = noflip

testPic.convert()
testPic.parseLines()
testPic.draw(velocity = 50, shutterAbsolute = True)

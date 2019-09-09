#!/usr/bin/env python3

# For OSCAR

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import picConv, micron
import servos

import datetime

_velocity = 25 # RUDOLPH = 50
_MODE = "RUDOLPH"
# _FILENAME = "./split/robinson-cropped-2.bmp"
# _FILENAME = "robinson.bmp"
_FILENAME = "testimage.bmp" # "fuer_elise_2.bmp"
# done
# 0, 1,3
# _FILENAME = "./split_big/robinson_big2-3.bmp" #"Australia-NewGuinea.bmp" # , #"robinson_big.bmp", #

_ESTIMATEONLY = False

# RODULPH

if _MODE == "RUDOLPH":
    testPic = picConv.PicConv(
        filename = _FILENAME,
        allowDiagonals = True,
        prioritizeLeft = True,
        shutterTime = servos.Shutter.DEFAULT_DURATION
        # simulateDrawing = True,
        # simulate = True,
        # micronInstance = False # We only want to simulate drawing
    )

    testPic.convert()
    testPic.parseLines()
    testPic.draw(velocity = _velocity, shutterAbsolute = True, shutter_channel = servos.Servo.RIGHTCH) if not _ESTIMATEONLY else print(datetime.timedelta(seconds = testPic.estimateTime(velocity = _velocity)))

# OSCAR
elif _MODE == "OSCAR":
    testPic = picConv.PicConv(
        filename = _FILENAME,
        allowDiagonals = True,
        prioritizeLeft = True,
        flipVertically = True,
        yscale = 0.5,
        xscale = 0.5,
        shutterTime = servos.Shutter.DEFAULT_DURATION
        # simulateDrawing = True
    )

    if not _ESTIMATEONLY:
        testPic.controller = micron.Micos(
            stageConfig = {
                "xlim" : [-10000,0],
                "ylim" : [-10000,0],
            },
            noHome = True,
            shutterAbsolute = True,
            shutter_channel = servos.Servo.RIGHTCH
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
    testPic.draw(velocity = _velocity) if not _ESTIMATEONLY else print(datetime.timedelta(seconds = testPic.estimateTime(velocity = _velocity)))

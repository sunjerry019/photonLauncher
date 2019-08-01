#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, "../../")

import servos

p = servos.Power(absoluteMode = False, channel = servos.Servo.RIGHTCH)
s = servos.Shutter(absoluteMode = True, channel = servos.Servo.LEFTCH)

for i in range(0,5):
    p.absolute(0.0725, duration = 150)
    time.sleep(0.5)

for i in range(0,5):
    p.absolute(0.0785, duration = 150)
    time.sleep(0.5)
s.open()
s.close()

#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, "../../")

import servos

# non absolute 360 servo ND filter mark i set up: 0.07 duty, 130 duration = 0.079 duty, 200 duration)

p = servos.Power(absoluteMode = False, channel = servos.Servo.RIGHTCH)
s = servos.Shutter(absoluteMode = True, channel = servos.Servo.LEFTCH)

p.absolute(0.07, duration = 130)
time.sleep(1)
p.absolute(0.07, duration = 130)
time.sleep(1)
p.absolute(0.079, duration = 200)
time.sleep(1)
p.absolute(0.079, duration = 200)
time.sleep(1)

s.close()
s.open()

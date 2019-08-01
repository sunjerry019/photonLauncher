#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, "../../")

import servos

p = servos.Power(absoluteMode = False, channel = servos.Servo.RIGHTCH)
s = servos.Shutter(absoluteMode = True, channel = servos.Servo.LEFTCH)

# for i in range(0,5):
#     p.absolute(0.072, duration = 200)
#     time.sleep(2)

# for i in range(0,5):
#     p.absolute(0.079, duration = 200)
#     time.sleep(2)

# s.open()
# s.close()

p.absolute(0.07, duration = 130)
time.sleep(1)
p.absolute(0.07, duration = 130)
time.sleep(1)
p.absolute(0.079, duration = 200)
time.sleep(1)
p.absolute(0.079, duration = 200)
time.sleep(1)





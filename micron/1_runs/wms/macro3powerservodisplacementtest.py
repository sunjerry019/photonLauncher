#!/usr/bin/env python3
import sys, os
import time
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import servos

# non absolute 360 servo ND filter mark i set up: 0.07 duty, 130 duration = 0.079 duty, 200 duration)

p = servos.Power(absoluteMode = False, channel = servos.Servo.RIGHTCH)

p.displacement += 5
time.sleep(1)
p.displacement -= 5
print("Power servo current displacement is", p.displacement,"!")

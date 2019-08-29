#!/usr/bin/env python3

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)
import stagecontrol

s = stagecontrol.stageControl()

s.singleraster(
    velocity = ,

)

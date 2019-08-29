#!/usr/bin/env python2

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "helpers"))
sys.path.insert(0, root_dir)
from getSpectra import Icecube

with Icecube() as cube:
    print(cube.getEEPROM())

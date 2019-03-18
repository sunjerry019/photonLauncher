#!/usr/bin/env python2

import sys
sys.path.insert(0, '../../helpers/')
from getSpectra import Icecube

with Icecube() as cube:
    print(cube.getEEPROM())

"""
Rotates the stage by a certain amount with arguments rather similar to odin.py, just that the data collection is done using an oscilloscope for a set period of time.

-zy
1 Jan 2016

"""


import sys, os
sys.path.insert(0,'../helpers/')

from mpi4py import MPI

import lecroy
import mjolnir

import argparse
import math



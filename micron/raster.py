#!/usr/bin/env python3

# Script to laser cut raster squares using the Nanomaterials Lab Microcontrollers for research experiments (ie the important stuff)
# Microcontroller Model: Micos 1860SMC Basic
# Made 2019, Wu Mingsong
# mingsongwu [at] outlook [dot] sg
# github.com/sunjerry019/photonLauncher


import sys, os
import time

import shutter

import numpy as np
import argparse as arg
import math
import pickle

from extraFunctions import query_yes_no as qyn

# raster machine should have multiple cutting modes:
# Mode 1: default, horizontal array of squares. Parameters = number of squares, size of squares, raster speed increments, inter-square gap size, raster direction preference (sideways vs up-down).
# Mode 2:

class Raster():

    def __init__(self,):









        #

#!/usr/bin/env python3

import numpy as np
from pathlib import Path
from NL_plotWavelengths import plotWavelengths
import pickle

with open("model.pkl", 'rb') as handle:
    x = pickle.load(handle)

x.setWavelengths({ 730.0 : 1 , 674.06 : 1 })
x.setOutput("data2.dat")
x.writeData()

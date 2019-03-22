#!/usr/bin/env python3

import numpy as np

withF = []
withoutF = []

with open("with", 'r') as f:
    l = f.readlines()
    for line in l:
        x = float(line.strip().split("\t")[1])
        withF.append(x)

withF = np.array(withF)

with open("without", 'r') as f:
    l = f.readlines()
    for line in l:
        x = float(line.strip().split("\t")[1])
        withoutF.append(x)

withoutF = np.array(withoutF)

opticalDensity = -np.log10(withF/withoutF)

with open("result", "w") as f:
    for wv in opticalDensity:
        f.write("{}\n".format(wv))

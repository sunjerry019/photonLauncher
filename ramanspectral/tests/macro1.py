#!/usr/bin/env python3

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "baselinecorr"))
sys.path.insert(0, root_dir)

print(sys.path)
import ramanskeletal

r = ramanskeletal.SuiteRaman()

r.parsefile('7mWgreen_100%_5scans_raman_butterflycnt_16mW_12ums_cut.txt', fliplist = True, xrng = [300, 2904])
r.plotbased(xlabel = 'Raman Shift/cm^-1', ylabel = 'Intensity (A.U.)', xrange = (100,3200), yrange = (-50, 1000), polyorder = 2, residual = 0.001, coarseness = 0.001, window = 50, iterations = 20, savefile = True)
#r.ramanbaseline(polyorder = 3, residual = 0.001, coarseness = 0.0001, window = 50, iterations = 20, savefile = True)

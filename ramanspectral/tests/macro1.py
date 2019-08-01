#!/usr/bin/env python3

import sys

sys.path.insert(0, "../baselinecorr/")
print(sys.path)
import ramanskeletal

r = ramanskeletal.SuiteRaman()

r.parsefile('7mWgreen_100%_5scans_raman_butterflycnt_16mW_12ums_cut.txt', fliplist = True, xrng = [0, 2904])
r.plotbased(xlabel = 'Raman Shift/cm^-1', ylabel = 'Intensity (A.U.)', xrange = (200,3200), yrange = (-50, 1000), polyorder = 3)
#r.ramanbaseline()

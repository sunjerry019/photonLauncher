#!/usr/bin/env python3

import numpy as np
from scipy import sparse
from numpy import array
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

## defines the baseline function used to iteratively process raman data
def baseline_als(y, lam, p, niter=10):
	L = len(y)
	D = sparse.csc_matrix(np.diff(np.eye(L), 2))
	w = np.ones(L)

	for i in range(niter):
		W = sparse.spdiags(w, 0, L, L)
		Z = W + lam * D.dot(D.transpose())
		z = spsolve(Z, w*y)
		w = p * (y > z) + (1-p) * (y < z)

	return z

##parses through all data files and executes function, plots at the end
for i in range(10,17):
	_data = np.loadtxt('data/6ums_{}mWcut_5mWgreenlaserraman_100%_5acquisition.txt'.format(i))
	y = _data[:, 1]
	y = y[0:2260]
	print('Parsing...done', y)
	x = _data[:, 0]
	x = x[0:2260]
	print('Parsing...done', x)
	z = baseline_als(y, 5*10**7,0.0005,100)
	print('Cuz you know its all about that base', z)

	x = np.array([x]).T
	y = np.array([y]).T
	z = np.array([z]).T
	final = y-z
	data = np.append(x, final, axis=1)

	print(data)
	np.savetxt('BASED_6ums_{}mWcut_5mWgreenlaserraman_100%_5acquisition.txt'.format(i), data, fmt=['%.2f','%.3f'], delimiter='\t')

	plt.plot(x, final)
	plt.show()

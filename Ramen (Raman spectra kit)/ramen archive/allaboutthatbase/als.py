#!/usr/bin/env python3

# allaboutthatbaseMARK-I

import numpy as np
from scipy import sparse
from numpy import array
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

## defines the baseline function used to iteratively process raman data
## rudimentary form of "fitness" assignment based on comparison between data points and iteratively modified "weight" matrix. IE if peaks are broad, this algorithm will NOT exclude them from fit.
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
for i in range(,):
	_data = np.loadtxt('data{}.txt'.format(i))
	y = _data[:, 1]
	##truncate data set if necessary
	#y = y[0:2260]
	print('Parsing...done', y)
	x = _data[:, 0]
	#x = x[0:2260]
	print('Parsing...done', x)
	#enter parameters lam, p and number of iterations
	z = baseline_als(y, 5*10**7,0.0005,100)
	print('Cuz you know its all about that base', z)

	x = np.array([x]).T
	y = np.array([y]).T
	z = np.array([z]).T
	final = y-z
	data = np.append(x, final, axis=1)

	print(data)
	np.savetxt('BASED data{}.txt'.format(i), data, fmt=['%.2f','%.3f'], delimiter='\t')

	plt.plot(x, final)
	plt.show()

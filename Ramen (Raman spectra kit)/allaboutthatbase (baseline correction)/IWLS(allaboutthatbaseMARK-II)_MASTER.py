#!/usr/bin/env python3
import math
import numpy as np
from scipy import sparse
from numpy import array
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import sys
import argparse

#parser = argparse.ArgumentParser(description='Raman spectrum baseline polynomial fit and removal via Iterative Weighted Least Squares')
#parser.add_argument('Polynomial order', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
#args = parser.parse_args()
#print(args.accumulate(args.integers))
## Works off Iterative Weighted Least Squares (IWLS) (Automated Background Subtraction Algorithm for Raman Spectra Based on Iterative Weighted Least Squares)
## defines the baseline function used to iteratively process raman data
##Choose order of polynomial to be fitted to baseline
n = 3
## initialise vandermonde matrix for polynomial fit.
## nth order polynomial->len(x) x (n+1) matrix
for o in range(,,):
    _data = np.loadtxt('data{}.txt'.format(o))
    x = _data[:, 0]
    x = x[0:2260]
    y = _data[:, 1]
    y = y[0:2260]
    x = np.array([x]).T
    y = np.array([y]).T
    y = np.asmatrix(y)
    L = len(x)
    vander = np.ones((L,1))
    print('Parsing...done.')

    for i in range(1, n+1):
        xpower = np.power(x, i)
        vander = np.append(vander, xpower, axis=1)
        print(vander, np.shape(vander))
    vander = np.asmatrix(vander)

    #Calculate coarseness c (L x 1) via a moving window standard deviation of the first derivative
    #rolling std and mean function
    def rocknroll(input, window):
        temp = np.empty(input.shape)
        temp.fill(np.nan)
        for i in range(window - 1, input.shape[0]):
            q = input[(i-window+1):i+1]
            temp[i-window+1] = np.sqrt((1/(window-1))*np.mean(np.power((q - q.mean()),2)))

        for i in range(input.shape[0] - window + 1, input.shape[0]):
            q = input[i:]
            temp[i] = np.sqrt((1/(window-1))*np.mean(np.power((q - q.mean()),2)))

        return temp

    #actual iteration process for fitness parameter p, threshold parameter n, number of iterations niter
    def iteration(p, z, niter, window):
        for t in range(1, niter+1):
            print("Iteration ", t)
            if t == 1:
                #initialise weight matrix using nxn identity matrix co
                weight = np.identity(L, dtype=np.float64)
                prevco = np.zeros((n+1,1))
            else:
                prevco = co
                weight = np.multiply((r < 0) + p*(r > 0), ((coarsenormalised < z) + p*(coarsenormalised > z)))
                weight = np.diagflat(weight)
                #print (weight)
            #initialise coefficient vector ((n+1) x 1)
            co = np.matmul(np.matmul(np.matmul(np.linalg.inv(np.matmul(np.matmul((np.transpose(vander)),weight), vander)), np.transpose(vander)), weight), y)
            #print(co)
            rms = math.sqrt(np.mean(np.power((co - prevco), 2)))
            print('RMS = ', rms, "\n")
            r = y - np.matmul(vander, co)
            d = np.gradient(r, axis=0)
            coarse = rocknroll(d, window)
            coarsenormalised = (coarse - min(coarse))/(max(coarse)-min(coarse))

            if rms == 0:
                break

        return co

    result = iteration(0.001, 0.0001, 50, window=50)
    signal = y - np.matmul(vander, result)
    fig = plt.figure()
    fig.suptitle('data{}'.format(o), fontsize=15)
    plt.xlabel('Raman shift/cm^-1', fontsize=15)
    plt.ylabel('Intensity/A.U.', fontsize=15)
    plt.plot(x, y)
    plt.plot(x, signal)
    plt.plot(x, np.matmul(vander, result))
    plt.show(block=False)
    plt.pause(1)
    plt.close()
    data = np.append(x, signal, axis=1)
    np.savetxt('BASED data{}'.format(o), data, fmt=['%.2f','%.3f'], delimiter='\t')



##

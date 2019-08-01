#!/usr/bin/env python3
import math
import numpy as np
from scipy import sparse
from numpy import array
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import sys
import argparse

## Works off Iterative Weighted Least Squares (IWLS) (Automated Background Subtraction Algorithm for Raman Spectra Based on Iterative Weighted Least Squares)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % 'Raman spectrum baseline polynomial fit and removal via Iterative Weighted Least Squares')
        self.print_help()
        sys.exit(2)

parser = MyParser()

parser.add_argument('polynomial', action='store', type = int, default=[3], help='An integer for the order of polynomial used to fit the spectrum. Usually 3 (cubic polynomial) is just nice. I will also display fits for 2 adjacent order polynomials to be safe :)')

parser.add_argument('-r','--residual', action='store', type = float, default=[0.001], help='Arbitrary parameter for residual acting as a weight to be applied when evaluating new coefficient vector. It is above but close to 0, Usually on the order of 10^-3 (input 0.001), experiment in the neighbourhood of this value (10^-2,  10^-4 etc) for better fits!')

parser.add_argument('-c','--coarseness', action='store', type = float, default=[0.0001], help='Arbitrary parameter for coarseness acting as a weight to be applied when evaluating new coefficient vector. Usually on the order of 10^-4 (0.0001), experiment in this neighbourhood (10^-3,  10^-5 etc) for better fits!')

parser.add_argument('-w','--window', action='store', type = int, default=[50], help='size of rolling window parsing through data array to calculate standard deviation of derivative of data. Usual size=50')

parser.add_argument('-niter','--iterations', action='store', type = int, default=[50], help='Number of iterations. Adjust this and other parameters to ensure fit converges.')

args = parser.parse_args()
N = args.polynomial
print('Polynomial order received = ',N)
p = args.residual
print('Residual fitness parameter used = ',p)
z = args.coarseness
print('Coarseness fitness parameter used = ',z)
w = args.window
print('Rolling window size = ',w)
niter = args.iterations
print('Max number of iterations = ',niter)
#Function1: Calculate coarseness c (L x 1) via a rolling window standard deviation of the first derivative. Rolling window automatically diminishes at the end.
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

#Function2: actual iteration process for fitness parameter p, threshold parameter z, number of iterations niter
def iteration(p, z, window, niter):
    for t in range(1, niter+1):
        print("Iteration ", t)
        if t == 1:
            #initialise weight matrix using nxn identity matrix co
            weight = np.identity(L, dtype=np.float64)
            prevco = np.zeros((n+1,1))
        else:
            prevco = co
            weight = np.multiply((r < 0) + p*(r >= 0), ((coarsenormalised < z) + p*(coarsenormalised >= z)))
            weight = np.diagflat(weight)
            #print (weight)
        #initialise coefficient vector ((n+1) x 1)
        co = np.matmul(np.matmul(np.matmul(np.linalg.inv(np.matmul(np.matmul((np.transpose(vander)),weight), vander)), np.transpose(vander)), weight), y)
        #print(co)
        rms = math.sqrt(np.mean(np.power((co - prevco), 2)))
        print('RMS = ', rms, "\n")
        r = y - np.matmul(vander, co)
        d = np.gradient(r, axis=0)
        finalcoarse = rocknroll(d, window)
        coarsenormalised = (finalcoarse - min(coarse))/(max(coarse)-min(coarse))

        if rms == 0:
            break
    return co

#Parsing raw data and reformating as vectors
for o in range(14,15):
    _data = np.loadtxt('data.txt')
    x = _data[:, 0]
    x = x[0:2260]
    y = _data[:, 1]
    y = y[0:2260]
    x = np.array([x]).T
    y = np.array([y]).T
    y = np.asmatrix(y)
    L = len(x)
    print('Parsing...done.')

    #initialise vandermonde matrix for polynomial fit.
    #nth order polynomial->len(x) x (n+1) matrix

    vicinity = [N-1, N, N+1]
    for n in vicinity:
        vander = np.ones((L,1))
        for i in range(1, n+1):
            xpower = np.power(x, i)
            vander = np.append(vander, xpower, axis=1)
        print(vander, np.shape(vander))
        vander = np.asmatrix(vander)

        #Actual execution of all functions with initialised matrices
        result = iteration(p, z, w, niter)
        signal = y - np.matmul(vander, result)

        fig=plt.figure(n-N+1)
        plt.xlabel('Raman shift/cm^-1', fontsize=15)
        plt.ylabel('Intensity/A.U.', fontsize=15)
        fig.suptitle('data, polynomial order={}'.format(n), fontsize=15)
        plt.plot(x, y)
        plt.plot(x, signal)
        plt.plot(x, np.matmul(vander, result))
    plt.show(block=False)
    plt.pause(20)
    plt.close()

        #data = np.append(x, signal, axis=1)
        #np.savetxt('BASED data{}'.format(o), data, fmt=['%.2f','%.3f'], delimiter='\t')



##

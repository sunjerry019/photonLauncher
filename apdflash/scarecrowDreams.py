"""
Rotates the stage by a certain amount with arguments rather similar to odin.py, just that the data collection is done using an oscilloscope for a set period of time.

-zy
1 Jan 2016

"""


import sys, os
sys.path.insert(0,'../helpers/')

from mpi4py import MPI

from lecroy import Lecroy
from mjolnir import Mjolnir
from rpiDBUploader import rpiDBUploader

import argparse
import math
import tarfile
import paramiko
import subprocess
import time

def check_dir(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)


def main(dg, step, binsize):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    print rank
    timestamp = time.strftime('%Y%m%d_%H%M')

    metadata = {
    'timestamp': timestamp,
    'bin_duration': binsize,
    'step_size':step,
    'degrees_moved': dg
    }

    check_dir(timestamp)

    with open(os.path.join(timestamp, 'metadata.json'), 'w') as f:
        json.dump(metadata,f)
    if rank == 0:
        print "on 2.188, scope control"
    elif rank == 1:
        print "on 2.194, motor control"

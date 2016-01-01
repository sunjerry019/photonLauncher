import sys,os
sys.path.insert(0, '../helpers')

import lecroy
import mjolnir

import argparse

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print rank

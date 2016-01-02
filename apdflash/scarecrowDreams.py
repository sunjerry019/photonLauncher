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
import threading
import time

def check_dir(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)

class scopeControl():
    def __init__(self,binsize):
        self.comm = MPI.COMM_WORLD
        self.binsize = binsize
        self.start_t = time.time()

        self.c = int(binsize)

        self.id = None
        self.timestamp = None
    def acquireData(self):
        check_dir(self.timestamp)
        scope = Lecroy()
        def stop():
            #scope.stop()
			print "scope stops acquisition"
            #(hist, mdata) = scope.getHistogram()
			mmdata = {
            'timestamp':    self.timestamp,
            'binsize':      self.c,
            'id':           self.id,
            'hist':         hist,
            'histMetaData': mdata}
			with open(os.path.join(self.timestamp, str(self.id)), 'wb+') as f:
                json.dump(mmdata, f)
            self.comm.send("done", dest = 1, tag = 0)
        #scope.start()
		print "scope starts acquisition"
        t = threading.Timer(self.c, stop)
        t.start()

class thorControl():
	def __init__(self, step, deg):
		self.step = step
		self.deg = deg
		self.timestamp = None
	def start(self):
		comm = MPI.COMM_WORLD
		m = Mjolnir()
		x = self.deg * 3600
		x /= float(2.16)
		s = int(self.step)
		x /= s
		self.data = {}
		for i in xrange(int(x)):
			#m.moveRotMotor(self.step)
			print "motor moves a little"
			comm.send("next", dest = 0, tag = 0)
			comm.send(i, dest = 0, tag = 1)
			if comm.recv(source = 0, tag = 0) == "done":
				continue
			time.sleep(1)
		comm.send("terminated", dest = 0, tag = 0)
		print "completed"

def main(dg, step, binsize):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    print rank
    timestamp = time.strftime('%Y%m%d_%H%M')

    metadata = {
        'timestamp':    timestamp,
        'bin_duration': binsize,
        'step_size':    step,
        'degrees_moved':dg
    }

    check_dir(timestamp)

    with open(os.path.join(timestamp, 'metadata.json'), 'w') as f:
        json.dump(metadata,f)
    if rank == 0:
        print "on 2.188, scope control"
        c = scopeControl(binsize)
        c.timestamp = timestamp
        while True:
            a = comm.recv(source = 1, tag = 0)


            if a == "next":
                b = comm.recv(source = 1, tag = 1)
                c.id = b
                c.acquireData()
            else:
                break
            # clean up and data exporting
		tar = tarfile.open("apdflashCoincidences{}.tar.gz".format(timestamp), "w:gz")
		tar.add(timestamp, arcname = timestamp)
		tar.close()

		for i in os.listdir(timestamp):
			os.remove(os.path.join(timestamp,i))
		os.rmdir(timestamp)

		ssh = rpiDBUploader("apdflashCoincidences{}.tar.gz".format(timestamp), "apdflash")
		ssh.upload()

    elif rank == 1:
        print "on 2.194, motor control"
        b = thorControl(step, dg)
        b.timestamp = timestamp
        b.start()

def init():
	parser = argparse.ArgumentParser(description = "Script to control motor for coincidence measurement of APD flash breakdown")
	parser.add_argument('degrees', metavar = 'd', type = float, help = "Total degrees to rotate")
	parser.add_argument('stepsize', metavar = 's', type = int, help = "Encoder counts to move, every rotation. Rotate until total degrees. Each encoder count is 2.16 arcseconds.")
	parser.add_argument('binlength', metavar = 'b', type = int, help = "Duration for oscilloscope to measure histogram")
	args = parser.parse_args()
	main(args.degrees, args.stepsize, args.binlength)

init()

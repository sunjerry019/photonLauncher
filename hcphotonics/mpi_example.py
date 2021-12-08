#!/bin/python2

"""
Uses MPI to communicate across two different raspis. One of them records counts from the APDs, and the other moves rotates a motor.

Other dependencies:
paramiko
mpi4py
rpiDBUploader
"""


from __future__ import division
from mpi4py import MPI
import time
import subprocess
import argparse

import numpy
import os, sys
import json
import tarfile
import paramiko
from rpiDBUploader import rpiDBUploader

from hcphotonics.thorlabs_apt import thorlabs_apt

def check_dir(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)

class apdControl():
	def __init__(self,binsize):
		self.comm = MPI.COMM_WORLD
		self.binsize = binsize
		self.start_t = time.time()
		self.c = int(binsize)
		self.data = []
		self.id = None
		self.timestamp = None
	def grabData(self):
		check_dir(self.timestamp)
		while self.c > 0:
			self.ping()
			time.sleep(0.2)
		with open(os.path.join(self.timestamp, str(self.id)), 'wb+') as f: #removed 'data',
			for i in range(len(self.data)):
				f.write("{}\t{}\t{}\n".format(i, self.data[i][1][0], self.data[i][1][1]))
		self.comm.send("done", dest = 1, tag = 0)

	def ping(self):
		proc = subprocess.Popen(['./getresponse','COUNTS?'], stdout=subprocess.PIPE)
		output = proc.stdout.read()

		if output == "timeout while waiting for response":
			pass
		else:
			t = time.time() - self.start_t
			data = output.rstrip().split(' ')
			data.pop(0)


		try:
			data = map(lambda x: float(x), data)
			_data = [t, data]
			self.c -= 1
			self.data.append(_data)
		except ValueError:
			pass

class thorControl():
	def __init__(self, step, deg):
		self.step = step
		self.deg = deg
		self.timestamp = None

	def start(self):
		comm = MPI.COMM_WORLD
		m = thorlabs_apt()
		x = self.deg / self.step
		x = int(x)
		self.data = {}
		for i in range(x):
			m.moveRotMotor(self.step)
			comm.send("next", dest = 0, tag = 0)
			comm.send([self.timestamp, i], dest = 0, tag = 1)
			#self.data[i] = comm.recv(source = 1, tag = 0)
			if comm.recv(source = 0, tag = 0) == "done":
				continue
			time.sleep(1)
		comm.send("terminated", dest = 0, tag = 0)

def main(kwargs):
	comm = MPI.COMM_WORLD
	#print "World size: {}".format(comm.Get_size())
	rank = comm.Get_rank()
	timestamp = time.strftime('%Y%m%d_%H%M')
	metadata = {'timestamp': timestamp,
				'bin_size': kwargs['binsize'],
				'step_size':kwargs['step'],
				'degrees_moved': kwargs['degree']}
	check_dir(timestamp)
	with open('copythis', 'w') as f:
		f.write(timestamp)
	with open(os.path.join(timestamp, 'metadata.json'), 'w') as f:
		json.dump(metadata, f)
	if rank == 0:
		print ("apd control")
		while True:
			a = comm.recv(source = 1, tag = 0)
			if a == "next":
				b = comm.recv(source = 1, tag = 1)
				c = apdControl(kwargs['binsize'])
				c.id = b[1]
				c.timestamp = b[0]
				c.grabData()
			else:
				break
		tar = tarfile.open("apdflash{}.tar.gz".format(timestamp), "w:gz")
		tar.add(timestamp, arcname = timestamp)
		tar.close()

		for i in os.listdir(timestamp):
			os.remove(os.path.join(timestamp,i))
		os.rmdir(timestamp)

		ssh = rpiDBUploader("apdflash{}.tar.gz".format(timestamp), "apdflash")
		ssh.upload()

	elif rank == 1:
		print ("motorised stage control")
		b = thorControl(kwargs['step'], kwargs['degree'])
		b.timestamp = timestamp
		b.start()

def init():
	parser = argparse.ArgumentParser(description = "Script to control motor for characterisation of APD flash breakdown")
	parser.add_argument('degrees', metavar = 'd', type = float, help = "Total degrees to rotate")
	parser.add_argument('stepsize', metavar = 's', type = int, help = "Degrees to move per step. Rule of thumb, not less than 1/2000.")
	parser.add_argument('binsize', metavar = 'b', type = int, help = "Number of readings the usbcounter device should record")
	args = parser.parse_args()
	main({'degree':args.degrees, 'step':args.stepsize, 'binsize': args.binsize})


init()

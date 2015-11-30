#!/bin/python3
import serial
import json
import os, sys
import time
import subprocess
import itertools

class getCounts():
  """ Returns a generator function that outputs the counts from the usbcounter device. 
  t is the no. of data points to acquire. -1 for endless stream """
  def __init__(self, t):
    timestamp = time.strftime('%Y%m%d_%H%M')
    if t == -1:
      generator = (self.talk() for i in itertools.count(0, 1))
    else:
      generator = (self.talk() for i in range(t))
    return generator
  def talk(self):
    proc = subprocess.Popen(['./getresponse', 'COUNTS?'], stdout = subprocess.PIPE)
    output = proc.stdout.read()
    if output =="timeout while waiting for response":
      pass
    else:
      data = output.rstrip().split(' ')
      data.pop(0)
      data = [float(i) for i in data]
      return data
    time.sleep(0.2)
    
    

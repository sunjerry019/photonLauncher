#!/bin/python2
import serial
import json
import os, sys
import time
import subprocess
import itertools
from collections import deque
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils

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

class logCounts():
  """ Uses getCounts() to save the counts into a folder (./raw), into a ASCII file that is timestamped. set plot to True for a live plot."""
  def check_dir(self, directory):
    if not os.path.exists(directory):
      os.makedirs(directory)
  def __init__(self,t, plot = False):
    filepath = 'raw'
    self.check_dir(filepath)
    timestamp = time.strftime('%Y%m%d_%H%M')
    if t < 1:
      raise ValueError("Infinite stream not allowed for logging")
    with open(os.path.join(filepath, timestamp), 'w') as f:
      gen = getCounts(t)
      for i in gen:
        f.write("{}\t{}\n".format(i[0], i[1]))
class plotCounts():
    """ Uses getCounts() to plot the counts. Uses a temp file. """
    def __init__(self):
        gen = getCounts(-1)
        det0 = deque([0] * 120)
        det1 = deque([0] * 120)

        tempfp = ".temp"

        self.initPlot()

        for i in gen:

            det0.appendleft(i[0])
            det1.appendleft(i[1])
            det0.pop()
            det1.pop()

            with open(tempfp, 'wb+') as f:
                for j in xrange(len(det0)):
                    f.write("{}\t{}\t{}\n".format(j, det0[j], det1[j]))

            self.g('plot "{0}" u 1:2 w l lw 3 , "{0}" u 1:3 w l lw 3'.format(tempfp))

    def initPlot(self):
        self.g = Gnuplot.Gnuplot()
        self.g("set title 'apd counts'")
        self.g("set xrange [0:120]")

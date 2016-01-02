import threading
import paramiko
import sys, os, json
import time
sys.path.insert(0, '../helpers')

from lecroy import Lecroy
from mjolnir import Mjolnir

import argparse

def check_dir(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)

def main(dg, step, binlength):
    filepath = '/home/robin/temp'
    ssh = paramiko.SSHClient()
    timestamp = time.strftime('%Y%m%d_%H%M')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.2.194', username = 'robin', password = 'freeasinfreedom')
    x = dg * 3600
    x /= float(2.16)
    s = int(step)
    x/= s
    scope = Lecroy()
    check_dir(os.path.join(filepath, timestamp))
    print x
    for i in xrange(int(x)):
        print i
        stdin,stdout, stderror = ssh.exec_command("cd photonLauncher/apdflash; python scarecrowMotor.py {}".format(step))
	print stdout.readlines()
        time.sleep(1)
	#scope.stop()
        scope.clear()
        scope.start()
        time.sleep(binlength)
        scope.stop()
        (hist, mdata) = scope.getHistogram()
        mmdata = {
            'timestamp': timestamp,
            'bin_duration':binlength,
            'id': i,
            'hist':hist,
            'histMetaData':mdata
            }
        with open(os.path.join(filepath, timestamp, str(i)),'wb+') as f:
            json.dump(mmdata, f)

def init():
	parser = argparse.ArgumentParser(description = "Script to control motor for coincidence measurement of APD flash breakdown")
	parser.add_argument('degrees', metavar = 'd', type = float, help = "Total degrees to rotate")
	parser.add_argument('stepsize', metavar = 's', type = int, help = "Encoder counts to move, every rotation. Rotate until total degrees. Each encoder count is 2.16 arcseconds.")
	parser.add_argument('binlength', metavar = 'b', type = int, help = "Duration for oscilloscope to measure histogram")
	args = parser.parse_args()
	main(args.degrees, args.stepsize, args.binlength)

init()

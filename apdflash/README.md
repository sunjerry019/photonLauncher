# odin.py

With two raspberry pis, one of them controlling a Thorlabs motor (depends on ```mjolnir.py```) and the other one logging the counts from the usbcounter device. (uses ```getresponse``` binary)

## Usage
``` $ odin.py D S N ``` 

- where D is the number of degrees the thorlabs motor will rotate in total (e.g. 90)
- where S is the number of encoder counts the motor will move per step (600,000 encoder counts are equivalent to 360 degrees)
- where N is the number of data points to take after the motor has moved a step.

The output is a folder with the timestamp you ran the script at, with ASCII files inside. The filenames are the ID number (i.e. 0, 1, 2, etc.) and so on. Have not settled on a useful naming convention, so I will leave the file naming system like this.

## Troubleshooting Checklist

- Are the raspis even on?
- Can the raspis see each other? (Check with ```mpiexec -f machinefile -n 2 hostname``` where machinefile is the directory of your machinefile)
- Can the raspis see the devices they are talking to? Is it the right port? Are permissions granted to use the devices? 
- Are you using the correct version of python? (python2)
- Does the getresponse script work by itself? (i.e. what do you see when you type ```./getresponse COUNTS?```). If it doesn't, recompile the getresponse binary and try again.
- Can the motor move by itself? SSH into the raspi, open up a python interpretor window, import mjolnir.py and try.

This order of troubleshooting steps should allow you identify which parts don't work. 

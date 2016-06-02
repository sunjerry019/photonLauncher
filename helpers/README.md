#helper libraries

Brief examples will be illustrated to demonstrate their common use cases. Should the snippets be insufficient, please do take a leap of faith and read the source code. It really isn't that difficult.

Import the ```helpers``` folder with ``` sys.path(0, '../helpers') ```
##lecroy

Communicates with Lecroy 9384TM Oscillocope via RS232 Serial communication. Serial settings (like port, baudrate, .etc. have defautls and are assumed to taken on certain values)

```python
import lecroy
scope = lecroy.Lecroy() #importing the library

(hist, metadata) = scope.getHistogram()# use of TA math channel is implicit

(waveform, metadata) = scope.getWaveform(2) # select ch2 or ch3

print scope.send("custom command") # refer to docs from lecroy for 9300 devices
```

##mjolnir

Controls Thorlabs Motorised Stages with TDC001 Controller Cube via RS-232 serial communication. [The communication protocol is provided by Thorlabs](http://www.thorlabs.hk/software_pages/ViewSoftwarePage.cfm?Code=APT). Commands to make the motor blink, and move a certain distance are supported, because we find ourselves only using those commands.

Usage of ```mjolnir``` assumes knowledge that an encoder count for the rotational motor (we use the [Thorlabs CR1-Z7](https://www.thorlabs.com/thorproduct.cfm?partnumber=CR1-Z7) is about 2.16 arcseconds per encoder count, and that the input should be adjusted accordingly. Likewise, the encoder count for our linear motor is 34304 encoder counts per millimetre.

Input to ```moveRotMotor``` is in encoder counts, which is a real integer. 
Input to ```moveLinMotor``` is in milimetres. We acknowledge this inconsistency.  (not sure about this actually, go check.) 

##spectrosco.py

Parses data files from the Spectrasuite software. These datafiles are assumed to be together in a folder. This outputs the mean and standard deviation for each wavelength in an ASCII file that gnuplot can read.

Usage:

```
python spectrosco.py DATAFOLDER -r -o ASCIIOUTPUTPATH -b BASEFILENAME
```

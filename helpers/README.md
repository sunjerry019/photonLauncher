#helper libraries

Brief examples will be illustrated to demonstrate their common use cases. Should the snippets be insufficient, please do take a leap of faith and read the source code. It really isn't that difficult.

Import the ```helpers``` folder with ``` sys.path(0, '../helpers') ```
##lecroy.py

Communicates with Lecroy 9384TM Oscillocope via RS232 Serial communication. Serial settings (like port, baudrate, .etc. have defautls and are assumed to taken on certain values)

```python
import lecroy
scope = lecroy.Lecroy() #importing the library

(hist, metadata) = scope.getHistogram()# use of TA math channel is implicit

(waveform, metadata) = scope.getWaveform(2) # select ch2 or ch3

print scope.send("custom command") # refer to docs from lecroy for 9300 devices
```

##mjolnir.py

Controls Thorlabs Motorised Stages with TDC001 Controller Cube.

##rpiDBUploader.py

##getCounts.py

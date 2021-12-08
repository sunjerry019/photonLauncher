# hcphotonics library


Some documentation may be unavailable, and we apologise for the inconvenience. Contact the authors for additional information.

## Supported equipment

Module | Equipment name
--- | ---
```hcphotonics.lecroy``` | Oscilloscope, Lecroy 9384TM (this is ancient)
```hcphotonics.thorlabs_apt```| Thorlabs TDC01 Controller Cube (CR1-Z7, MTS50-Z8)
```hcphotonics.temp_humid```| Thorlabs TSP01 Temperature and Humidity sensor (liveplotting not updated yet)
```usbcounter```| Avalanche Photon Detectors (built at NUS)


## ```hcphotonics.lecroy```

### Purpose
Obtain waveform and histogram data from Lecroy 9300C Series Oscilloscope over RS-232 connection. Acts as a wrapper, sending more basic function calls over serial.

### Usage

Importing:

```python
import hcphotonics.lecroy as lecroy
l = lecroy.Lecroy('/path/to/lecroy.conf')
```

Send arbitrary command:
```python
l.send("Arbitrary command")
```

Start and stop acquisition, then clear data on screen:
```python
l.start()
l.stop()
l.clear()
```

All the data on the screen is all the data you have recorded (be it waveform or histogram).


Get the histogram (default channel is 'A' for the math channel)
```python
hist, metadata = l.getHistogram("A")
```

Get waveforms (there are 4 channels):
```python
waveform, metadata = l.getWaveform('3')
```

Here, ```metadata``` is a dictionary that contains information on scaling, offset, and so on. You will have to process the parsed data yourself. 

### Example config for lecroy
The default configuration file, ```lecroy.conf```, should be created in the same directory 


```
lecroy.conf:
port=/dev/ttyUSB0
baudrate=19200
parity=N
stopbits=1
bytesize=8
timeout=2
rawData=/home/robin/Dropbox/hbar/GhostImaging/fruitScope/rawData
parsedData=/home/robin/Dropbox/hbar/GhostImaging/fruitScope/parsedData
```

### ```lecroy_export.py``` (included script)

This script is a wrapper around the getWaveform and getHistogram functions.

Usage:

```bash
$ python lecroy_export.py CONFIG_FILE_PATH OUTPUT_FILE_PATH [h|w] CHANNEL
```
### References

[Lecroy 9300C Series Manual](http://cdn.teledynelecroy.com/files/manuals/9300_om_reva.pdf)
[Lecroy 9300C Series Remote Control Manual](http://cdn.teledynelecroy.com/files/manuals/9300-rcm_reva.pdf)

## hcphotonics.thorlabs_apt


## Purpose

## Usage
### Example config for thorlabs_apt

port=/dev/ttyUSB0
baudrate=19200
parity=N
stopbits=1
bytesize=8
timeout=2



 

## Contact Us

Feel free to add an issue or a pull request. Our emails are open.

Our official email contact is ```photonics@hci.edu.sg```. Alternatively, drop us an email at ```hwachong.photonics@gmail.com```

Note: naming conventions are still fairly inconsistent, expect them to change.



## hcphotonics.temp_humid

Uses ```teaspoon.py``` in the helpers folder. Returns a tuple of ```(data, metadata)``` after processing the data dump from Thorlabs TSP001.

## parse_temphumid.py

Wrapper around ```teaspoon.py```, the latter of which is the general library. Outputs gnuplot-usable ASCII file to ```OUTPUT_DATA_PATH```.

Usage:

```python parse_teaspoon.py INPUT_DATA_PATH [OUTPUT_DATA_PATH]```

Output file path is an optional argument; default is to take the input data file path, which is ```abc.txt```, and output to ```abc```.

Optional arguments ```-s``` and ```-v``` for debugging purposes.
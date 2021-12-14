# hcphotonics library


Some documentation may be unavailable, and we apologise for the inconvenience. Contact the authors for additional information.


# Installation

Having cloned the repository, ```cd``` into the folder with ```setup.py``` and run:

```bash
pip install .
```

## Supported equipment

Module | Equipment name
--- | ---
```hcphotonics.lecroy``` | Oscilloscope, Lecroy 9384TM (this is ancient)
```hcphotonics.thorlabs_apt```| Thorlabs TDC01 Controller Cube (CR1-Z7, MTS50-Z8)
```hcphotonics.temp_humid```| Thorlabs TSP01 Temperature and Humidity sensor 
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

An interface for communicating with the Thorlabs TDC01 controller cube. We were specifically using the CR1-Z7 and MTS50-Z8 stages.

### Usage

Write a text config file as shown below. If the connected USB port is for a linear stage, then you would run commands for a linear stage.

To support multiple motors on different USB ports, initialise two instances of the thorlabs_apt module.

As for identifying which is which, it'll be in the order you plug them in, but I'm not sure if there's a simple way to programmatically check without already knowing the device ID.

```python
import hcphotonics.thorlabs_apt as thorlabs_apt
t = thorlabs_apt.ThorlabsApt("config.txt")
```

```python
t.homeMotor() # Homes the motor (i.e. linear stages)
t.moveLinMotor(5) # moves 5 mm from current position
t.moveRotMotor(45) # moves 45 degrees relative to current position
t.absRotMotor(75) # move to 75 degrees defined from 0 
```
### Example config for thorlabs_apt

port=/dev/ttyUSB0
baudrate=19200
parity=N
stopbits=1
bytesize=8
timeout=2

## hcphotonics.temp_humid

Written to support the [Thorlabs TSP01 Temperature and Humidity](https://www.thorlabs.com/thorproduct.cfm?partnumber=TSP01) sensor.

### Usage

```python
import hcphotonics.temp_humid as temp_humid
th = temp_humid.ThorlabsTempHumid()

# these return floats
temp = th.getTemperatureOnboard()
temp_probe = th.getTemperatureOnboard()
humidity = th.getHumidity()
```
## usbcounter

Obtained from [NUS CQT](https://www.quantumlah.org/). Used to count signals from Avalanche Photon Detectors.

### Usage

First, run the Makefile:
```bash
make
```
which will compile ```getresponse``` and ```addrows```.

The script ```apd_counter.py``` provides an example of how ```getresponse``` is used to count the number of detected photons per time bin.

## mpi_example.py

Example script in which two different Raspis each control different equipment, one talking to the APDs, and the other talking to a rotational stage. They are controlled via MPI. 


## Contact Us

Feel free to add an issue or a pull request. Our emails are open.

Note: naming conventions are still fairly inconsistent, expect them to change.


## hcphotonics.temp_humid

Uses ```teaspoon.py``` in the helpers folder. Returns a tuple of ```(data, metadata)``` after processing the data dump from Thorlabs TSP001.

## parse_temphumid.py

Wrapper around ```teaspoon.py```, the latter of which is the general library. Outputs gnuplot-usable ASCII file to ```OUTPUT_DATA_PATH```.

Usage:

```python parse_teaspoon.py INPUT_DATA_PATH [OUTPUT_DATA_PATH]```

Output file path is an optional argument; default is to take the input data file path, which is ```abc.txt```, and output to ```abc```.

Optional arguments ```-s``` and ```-v``` for debugging purposes.
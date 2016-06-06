# scopy

This is a library for interacting with the Lecroy Oscilloscope via RS323 <--> USB Serial.

## Exporting stuff from the scope

Check that the RS232 cable is connected. Run ```python export.py``` with the relevant arguments.

Example: saving the waveform on channel 2 to ```~/FILEPATH``` 
```
python export.py ~/FILEPATH w 2
```

## Initialisation
```python
import lecroy
scope = lecroy.Lecroy()
```

## Acquiring the Histogram

```python
(hist, metadata) = scope.getHistogram()
```

This returns a tuple, ```(hist, metadata)```, both of which have been parsed. ```hist``` is a list of ```[x,y]``` values. The first math channel (```TA```) is implicit in the acquisition of the histogram.

The x-axis data is also scaled up by ```10 ** 9 ``` as in our use case, a histogram in nanoseconds is easier to read, and also because of floating point errors.

```metadata``` is a dictionary, and is relevant to both the histogram and waveform, as it contains the values for the x-axis data, along with things like acquisition duration, oscilloscope model, etc.

## Acquiring the Waveform

```python
(waveform, metadata) = scope.getWaveform()
```

This works in a very similar fashion to ```getHistogram()```, though you'll now have to specify the channel. (We usually use ```2``` or ```3```) Note that the parsing is only very slightly different for ```getWaveform()```

## Sending your own command

```python
scope.send(cmd)
```
where ```cmd``` is your own command. Refer to the [Lecroy Manual for 9300 Series devices](http://cdn.teledynelecroy.com/files/manuals/9300-rcm_reva.pdf) for additional information.

## Troubleshooting
The primary problem you'll come across is the serial port. The Lecroy's serial port is accessed at ```/dev/ttyUSBX``` where X is a number.

To verify that you're using the correct port:
```bash
ls /dev/ | grep ttyUSB
```
Change the value for ```port``` in the configuration file (found at ```lecroy.conf```), or directly edit the value in ```lecroy.py```.

To allow ```scopy``` to access that port:
```bash
sudo chmod a+rw /dev/ttyUSBX
```
where X is your port number.

# fruitScope

This is a library for interacting with the Lecroy Oscilloscope via RS323 <--> USB Serial.

## Documentation

### Initialisation
```python
> import lecroy
> scope = lecroy.Lecroy()
```

### Acquiring the Histogram

```python
> scope.getHistogram()
```

This returns a tuple, ```(hist, metadata)```, both of which have been parsed. ```hist``` is a list of ```[x,y]``` values. The first math channel (```TA```) is implicit in the acquisition of the histogram.

The x-axis data is also scaled up by ```10 ** 9 ``` as in our use case, a histogram in nanoseconds is easier to read, and also because of floating point errors.

### Acquiring the Waveform

### Sending your own command

```python
> scope.send(cmd)
```
where ```cmd``` is your own command. Refer to the [Lecroy Manual for 9300 Series devices](http://cdn.teledynelecroy.com/files/manuals/9300-rcm_reva.pdf) for additional information.

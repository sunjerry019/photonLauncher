# OceanOptics

This is a submodule that provides support for the OceanOptics (now renamed Ocean Insight) tabletop spectrometers (2000 and 4000), along with Flame-S, a UV-VIS spectrometer.

# Usage

As this is not packaged into a Python module, this can be installed by extending ```oceanoptics.py```, or moving ```oceanoptics.py``` into your working directory.

This depends on [libusb1](https://pypi.org/project/libusb1/).

# Example

```python
from oceanoptics import OceanOptics

with OceanOptics as s:
	s.setIntegrationTime(100) # in milliseconds
	spectra = s.getSpectra() # returns list of tuples (wavelength, reading)
```

# Note

The folders 'get' and 'process' are kept here for archival purposes and do not contribute to functionality. 
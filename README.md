# photonLauncher
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)
---------
 > Look again at that dot. That's here. That's home. That's us. On it everyone you love, everyone you know, everyone you ever heard of, every human being who ever was, lived out their lives.
 >
 > Pale Blue Dot, Carl Sagan

Github repository for the collection of scripts that we have made in this neverending journey of scientific exploration. Scripts include equipment control, as well as administrative and housekeeping tools.

As of 05/2019, some scripts specific to the Hwa Chong Photonics Lab has been moved to the ```0_hcphotonics``` folder. They are all working, just irrelevant.

Some documentation may be unavailable, and we apologise for the inconvenience. Contact the authors for additional information.

**Documentation for individual scripts / experiments can be found in their respective folders.**

Use
```python
# sys.path.insert(0, '../helpers/')
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "helpers"))
sys.path.insert(0, root_dir)
```
to access libraries in ```helpers```.

## Supported equipment

Location | Equipment name
--- | ---
```oceanoptics/get/icecube.py```| OceanOptics Spectrometer, USB2000, USB4000 and Spectra Series
```0_hcphotonics/helpers/lecroy.py``` | Oscilloscope, Lecroy 9384TM (this is ancient)
```0_hcphotonics/helpers/mjolnir.py```| Thorlabs TDC01 Controller Cube (CR1-Z7, MTS50-Z8)
```0_hcphotonics/usbcounter/arthur2.py```| Avalanche Photon Detectors (built at NUS)
```0_hcphotonics/teaspoon/climate.py```| Thorlabs TSP01 Temperature and Humidity sensor (liveplotting not updated yet)
```0_hcphotonics/roger/roger.py```| Photometer with Arduino as a voltage sensor


## Contact Us

Feel free to add an issue or a pull request. Our emails are open.

The repository is now mainly maintained by ```sunjerry019```, with help from ```starryblack```. Any queries may be directed to ```sunjerry019 [at] gmail [dot] com```.

The official email contact for Hwa Chong Photonics is ```photonics@hci.edu.sg```. Alternatively, drop us an email at ```hwachong.photonics@gmail.com```

Note: naming conventions are still fairly inconsistent, expect them to change.

## Labs

This repository contains code made while working at the following labs:
- Hwa Chong Photonics Lab (2015 - 2016)
- NUS Nanomaterials Lab (2019 - )

# photonLauncher
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
---------
 > Look again at that dot. That's here. That's home. That's us. On it everyone you love, everyone you know, everyone you ever heard of, every human being who ever was, lived out their lives.
 >
 > Pale Blue Dot, Carl Sagan

Github repo for the Photonics Lab at Hwa Chong Institution. A collection of scripts that control equipment, as well as administrative and housekeeping tools.

Some documentation may be unavailable, and we apologise for the inconvenience. Contact the authors for additional information. 

**Documentation for individual scripts / experiments can be found in their respective folders.**

Use ```sys.path.insert(0, '../helpers/')``` to access libraries in ```helpers```.

## Supported equipment

Location | Equipment name
--- | ---
```helpers/lecroy.py``` | Oscilloscope, Lecroy 9384TM (this is ancient)
```helpers/mjolnir.py```| Thorlabs TDC01 Controller Cube (CR1-Z7, MTS50-Z8)
```usbcounter/arthur2.py```| Avalanche Photon Detectors (built at NUS)
```oceanoptics/get/icecube.py```| OceanOptics Spectrometer, USB2000 and USB4000 (liveplotting works!!) 
```teaspoon/climate.py```| Thorlabs TSP01 Temperature and Humidity sensor (liveplotting not updated yet)
```roger/roger.py```| Photometer with Arduino as a voltage sensor


## Contact Us

Feel free to add an issue or a pull request. Our emails are open.

Our official email contact is ```photonics@hci.edu.sg```. Alternatively, drop us an email at ```hwachong.photonics@gmail.com```

Note: naming conventions are still fairly inconsistent, expect them to change.

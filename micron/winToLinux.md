This file is meant to describe the procedures that must be taken for the use of this script on a linux machine instead of the standard windows machine that the lab uses.

1. Download and install the latest version of `python` and `python-pip` (Version 3.x)
2. `pip install serial playsound`
3. `import sound.linux-shutter` instead of `import shutter` in `micron.py`
4. Change 'COM1' to '/dev/ttyACM0' or something similiar based on your system
5. Ensure that the current user has permissions to `/dev/ttyACM0`
6. Everything should work just fine. I think.


Sun Yudong
2019
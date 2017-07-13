# roger.py:

## Setup:

Used with the Photometer (IF PM, looks blue with two pins); an Arduino (either at 3.3 V or 5 V) references the pins across the photometer (maximum voltage around 1.2 V).

You'll probably want to callibrate the numbers on the photometer screen to the voltage reading from ```roger.py```; look for a line that does linear scaling.

Check the Arduino's port number,  and edit ```roger.py``` accordingly.

```
$ ls /dev/ | grep ttyACM
```


## Usage:

```
$ python roger.py TOTALDATAPOINTS [-f logging] [-d additional details]
```

Saves a timestamped file to the current directory. Takes approximately 2500 readings per second.


# brieflysummarise.py

## Setup:

Used with the Photometer (as with ```roger.py```). Also controls the Thorlabs Linear Motor (documented in the ```/helpers/``` folder using the ```mjolnir``` library).

Check that the motor port is accessible, editing the config file (```/cfg/.mjolnir```) if needed.

```
$ ls /dev/ | grep ttyUSB
```

## Usage:

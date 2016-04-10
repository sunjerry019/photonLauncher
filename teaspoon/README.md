#teaspoon

Uses ```teaspoon.py``` in the helpers folder. Returns a tuple of ```(data, metadata)``` after processing the data dump from Thorlabs TSP001.

#parse_teaspoon.py

Wrapper around ```teaspoon.py```, the latter of which is the general library. Outputs gnuplot-usable ASCII file to ```OUTPUT_DATA_PATH```.

Usage:

```python parse_teaspoon.py INPUT_DATA_PATH [OUTPUT_DATA_PATH]```

Output file path is an optional argument; default is to take the input data file path, which is ```abc.txt```, and output to ```abc```.

Optional arguments ```-s``` and ```-v``` for debugging purposes.

#plot.sh

Shortcut to use gnuplot to plot both the temperature and humidity data into an EPS file. Uses multiplot and is preset. Requires command line arguments.

Usage:

```./plot.sh INPUT_ASCII_FILE OUTPUT_EPS_FILE.eps TITLE_TEXT```



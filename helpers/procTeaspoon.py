
#parser for data dump from tsp01 thorlabs application
#tsp01 is a temperature and humidty sensor

#we assume an external temperature probe (th1) that is attached

#call from command line / import the function

#this probably belongs inside the helper folder

#zy
#5 apr 2016


import os, json, sys
import argparse
import time
import datetime

def getac(x):
    """Shortcut to return the second value of a data line. """
    return x.split(":\\t")[1]

def getMetadata(s):
    """Returns the measurement interval and duration as a dictionary."""
    for i in s:
        if "Date" in i:
            d = getac(i)
        if "Time (" in i:
            t = getac(i)
        if "Number of S" in i:
            N = getac(i)
        if "Measurement Int" in i:
            dt = getac(i)
            #print(dt)
    datetime = (time.strftime('%Y%m%d_%H%M',time.strptime(d + t,'%Y-%m-%d%H:%M:%S')))
    metadata = {}
    metadata['N'] = float(N)
    metadata['time'] = datetime
    metadata['time_interval'] = float(dt)
    return metadata
    #print(date + " " + time)

def parseline(s):
    """ Returns the temperature / humidity data as a list, removing the last two lines as they are not yet used. """
    line = (s.split("\\t"))[:-2]
    line = [float(x.strip()) for x in line]
    return line


# the data is organised in columns as follows
# time in seconds   onboard temp sensor     onboard rel humidity sensor     external temperature probe 1    external temperature probe 2
def parse(filepath):
    """ Returns a tuple of data, as well as metadata. """
    with open(filepath, 'rb') as f:
        raw_text = str(f.read())
        raw_text = raw_text.split('\\r\\n')
        #print(raw_text)
        metadata = getMetadata(raw_text)
        parse_data = False
        data  = []
        for i in raw_text:
            if parse_data:
                data.append(parseline(i))
            if "Time [s]" in i:
                parse_data = True
        data.pop()
        return(data, metadata)

def main():
    """ argparse to process CLI options in case we want to use this directly, instead of using a separate controller script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("fp", type = str, help = "Path to textfile from Thorlabs TSP01 to be parsed.")
    args = parser.parse_args()
    parse(args.fp)

if __name__ == '__main__':
    main()

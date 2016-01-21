import argparse
from os import listdir
from os.path import isfile, join
import sys, json

""" main class takes a string of folder name, then returns a dictionary with the relevant statistics. option to save json file."""

class spec():
    def __init__(foldername, output = None, basefilename = ""):
        f = [join(foldername, f) for f in listdir(foldername) if isfile(join(foldername, f))]


if __name__ == '__main__':
    print "Hello World!"

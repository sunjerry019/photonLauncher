"""
parseSignal.py

Used to interpret voltage data from the oscilloscope, as the data is formatted slightly differently for the both of them.

"""


import json
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import argparse
import time, os, sys
import tempfile
import math

def parseSignal(filename):
    """ Returns a plottable list of voltage readings and their respective time values."""
    with open(os.path.join('rawdata', filename), 'r') as f:
        text = f.read()
        text = text.split('---')

    def parseMetaData(text):
        text = text.split('"')[3].split('\n')
        metadata = {}
        for i in text:
            if len(i) > 1:
                x = i.split(':')
                k = x[0].strip()
                v = x[1].strip()
                try:
                    v = float(v)
                    k = k.lower()
                except:
                    pass
                metadata[k] = v

        return metadata
    def parseContents(text):
        text = text.split('"')[3]
        text = text.split('\n')
        text = ''.join(text)
        text = text.strip().split(" ")
        voltage = []
        for i in text:
            voltage.append(float(i))
        return voltage
    contents = parseContents(text[1])
    metadata = parseMetaData(text[2])
    data = []
    for i in range(len(contents)):
        x = metadata['horiz_offset'] + (i * metadata['horiz_interval'])
        x *= 10**9  # dealing with nano second units here, scaling it up for easier readability
        data.append([round(x,4), contents[i]])
    return data

def plotSignal(timestamp):
    data = parseSignal(timestamp)
    with open(os.path.join('parseddata', timestamp), 'w') as f:
        for i in data:
            f.write('{}\t{}\n'.format(i[0], i[1]))
    g = Gnuplot.Gnuplot()
    g('set term epscairo noenhanced truecolor')
    g('set output "{}.eps"'.format(os.path.join('parseddata',timestamp)))
    g('set xlabel "Time (ns)"')
    g('set ylabel "Volts (V)"')
    g('set title "{} {}"'.format("apd nim signal", timestamp))
    g.plot(data)
def analyseSignal(timestamp):
    data = parseSignal(timestamp)
    for i in data:
        if i[1] < -0.5:
            print(i[1])
plotSignal('20151124_0834')
analyseSignal('20151124_0834')

import json
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
import argparse
import time, os, sys
import tempfile
import math

def check_dir(directory):
    if not os.path.exists(directory):
        print "Directory {} does not exist...creating...".format(directory)
        os.makedirs(directory)

def main():
    parser = argparse.ArgumentParser(description = "Plots and saves json objects in folder parseddata, uses a config file for plot setting inside cfg/.plotjson for gnuplot settings")
    parser.add_argument('f', metavar = 'f', help="Filename of json file to be plotted.")
    parser.add_argument('title', metavar = 't', help = "Title to be included in plot.")
    parser.add_argument('-e', '--errorbars', help = "Use this flag to NOT plot with error bars, in case the plot is too messy.", action = "store_true")

    args = parser.parse_args()
    p = plotJson(args.errorbars)
    p.load(args.f, args.title)

def hms(x):
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    return "%dh:%02dm:%02ds" % (h, m, s)
class plotJson():
    def __init__(self, eb):
        self.eb = eb
        self.cfg = {}
        try:
            with open('cfg/.plotjson', 'rb+') as f:
                x = f.read()
                x = x.split('\n')
                for i in x:
                    if len(i) > 0:
                        i = i.rstrip()
                        i = i.split('=')
                        self.cfg[i[0]] = i[1]
        except:
            print "No config file found...using default settings";
            self.cfg =
            {
                "format": "epscairo",
                "xlabel": "t@level (ns)",
                "ylabel": "Two-photon coincidence events"
            }
    def getx(self,hist, desc):
        h_offset = float(desc['horiz_offset']) * 10 ** 9
        h_binsize = float(desc['horiz_interval']) * 10 ** 9
        s = []
        for i in xrange(len(hist)):
            s.append([(i * h_binsize) + h_offset, hist[i]])
        return s
    def load(self, path, title):
        #fpath = 'parseddata/' + path
        fpath = path
        with open(fpath, 'rb+') as datafile:
            data = json.load(datafile)
        if not isinstance(data['hist'][0], list):
            data['hist'] = self.getx(data['hist'], data['desc'])
        duration = int(float(data['desc']['acq_duration']))
        duration = hms(duration)

        rawf = open(fpath + ".dat", 'wb+')
        for i in xrange(len(data['hist'])):
            _x = data['hist'][i][0]
            _y = data['hist'][i][1]
            _yerror = round(math.sqrt(_y),1)
            rawf.write("{}\t{}\n".format(_x, _y))
        rawf.close()

        self.initPlot()
        self.g('set title "{} {}, acquisition duration {}"'.format(path,title,duration))
        self.g('set output "{}.eps"'.format(fpath))
        if not self.eb:
            self.g('f(x) = mean_y')
            self.g('fit f(x) "{}" u 1:2 via mean_y'.format(fpath))
            self.g('plot "{}" u 1:2:(sqrt(mean_y)) with yerrorbars pt 7 ps 0.2 '.format(fpath))
        else:
            self.g('plot "{}" u 1:2 w p pt 7 ps 0.2'.format(fpath))

    def initPlot(self):
        self.g = Gnuplot.Gnuplot()
        self.g('set term {} transparent truecolor size 10,7.5'.format(self.cfg['format']))
        self.g('set xlabel "{}"'.format(self.cfg['xlabel']))
        self.g('set ylabel {}'.format(self.cfg['ylabel']))


main()

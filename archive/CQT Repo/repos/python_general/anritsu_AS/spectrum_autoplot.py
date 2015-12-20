#!/usr/bin/python

from Tkinter import Tk
from tkFileDialog import askopenfilename, askopenfilenames
import spectrum_class as spc


Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filenames = askopenfilenames()  #defaultextension='*.spa', initialdir='.')  # show an "Open" dialog box and return the path to the selected file
#print(filename)

spectra = [spc.Spectrum(i) for i in filenames]

spectra[0].plot(new_figure='yes')

if len(spectra) > 1:
    for sp in spectra:
        sp.plot(new_figure='no')
#if
## prepare the figure and plot
#plt.figure('Spectrum from file: '+self.filename)
#            plt.xlabel('frequency (MHz)')
#            plt.ylabel('noise (dBm)')
#sp1.plot(new_figure='no')
#
spc.plt.show()

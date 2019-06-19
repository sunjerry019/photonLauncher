#!/usr/bin/env python3
# WMS's attempt at starting the graphical user interface effort for the benefit of future members of the Nanomaterials lab ("if only everything can be done with a single click of a single button")
# Swapped to PyQt4 from Tkinter, because the former is more powerful/intuitive to implement features
# microgui will pair functions with commands imported from raster.py

#import raster
import sys
from PyQt4 import QtGui

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Micos Stage Controller MARK II")
        self.setWindowIcon(QtGui.QIcon('pictures/fibonacci.bmp'))
        self.show()



app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Graphical User Interface for stagecontrol.py

# WMS's attempt at starting the graphical user interface effort for the benefit of future members of the Nanomaterials lab ("if only everything can be done with a single click of a single button")
# Swapped to PyQt4 from Tkinter, because the former is more powerful/intuitive to implement features
# microgui will pair functions with commands imported from stagecontrol.py which uses raster in turn
# also using qt designer to get quick visual preview of how the window should look like. Please install qt designer to open the .ui file. It CAN be converted to python code, but its like a translated-from-c++ version and very inelegant. Trying to define the functions individually for easier debugging/edits.

# Made 2019, Wu Mingsong
# mingsongwu [at] outlook [dot] sg

import sys
from PyQt4 import QtCore, QtGui

import stagecontrol

class MicroGui(QtGui.QMainWindow):
    def __init__(self):
        super(MicroGui, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50,50,500,300)
        self.setWindowTitle('Micos Stage Controller MARK II beta')
        self.setWindowIcon(QtGui.QIcon('pictures/fibonacci.bmp'))
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addwidget(self.stage)
        self.setCentralWidget(self.central_widget)
        self.show()

# first layout
    def stage(self):
        self.home_position = QPushButton("Move to absolute home (0,0)")
        self.set_origin = QPushButton("Set as (0,0)")

        self.velocity = QLineEdit()
        self.velocity.setValidator(QIntValidator(0,1000))
        self.velocity.setFont(QFont("Arial",20))

        self.step_size = QLineEdit()
        self.step_size.setValidator(QIntValidator(0.5,1000))
        self.step_size.setFont(QFont("Arial",20))

        # need to link to stagecontrol to read position of controllers
        self.lcdx = QLCDNumber()
        self.lcdy = QLCDNumber()

        self.first_layout = QGridLayout()
        self.first_layout.addWidget(self.home_position)
        self.first_layout.addWidget(self.set_origin)
        self.first_layout.addWidget(self.velocity)
        self.first_layout.addWidget(self.step_size)
        self.first_layout.addWidget(self.lcdx)
        self.first_layout.addWidget(self.lcdy)
        self.first_layout.addWidget(self.first_layout)

        self.stage_widget = Qwidget()
        self.stage_widget.setLayout = (self.first_layout)
        self.setCentralWidget(self.stage_widget)

# second layout
    def single_raster(self):

    pass
# third layout
    def array_raster(self):
    pass


# fourth layout
    def drawpic(self):
    pass

def main():
    app = QApplication(sys.argv)
    window = MicroGui()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

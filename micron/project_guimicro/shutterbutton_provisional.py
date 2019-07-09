#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

sys.path.insert(0, '../')
import stagecontrol
import shutterpowerranger

class Butt(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        self.shutter = shutterpowerranger.Servo(absoluteMode = True)
        self.isOpen = False

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        if self.isOpen:
            self.shutter.close()
            self.isOpen = False
        else:
            self.shutter.open()
            self.isOpen = True
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Butt()
    sys.exit(app.exec_())

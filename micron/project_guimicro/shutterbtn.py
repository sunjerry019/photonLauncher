#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

sys.path.insert(0, '../')
# import stagecontrol
import shutterpowerranger

class Butt(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Optical audio shutter'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.shutter = shutterpowerranger.Shutter(absoluteMode = True, channel = shutterpowerranger.Servo.RIGHTCH)
        self.isOpen = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLabel(self)
        self.textbox.move(100, 20)
        self.textbox.resize(350,80)
        self.textbox.setText("HELLO WORLD")
        self.setStyleSheet("QLabel {font: bold 18pt Roboto}")


        button = QPushButton('LAUNCH\nSEQUENCE', self)
        button.setToolTip('A single button. Click it maybe?')
        button.move(125,125)
        button.resize(250,250)
        button.setStyleSheet('QPushButton {background-color: red; color: black; font: bold 20pt Roboto}')
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        if self.isOpen:
            self.shutter.close()
            self.isOpen = False
            self.textbox.setText("You closed the shutter\nGood job!!")
        else:
            self.shutter.open()
            self.isOpen = True
            self.textbox.setText("You opened the shutter\nWE'RE DOOMED!!")

def main():
    app = QApplication(sys.argv)
    ex = Butt()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

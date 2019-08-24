#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

sys.path.insert(0, '../')
# import stagecontrol
import servos
from guimicro import moveToCentre

class Butt(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Optical audio shutter'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.shutter = servos.Shutter(absoluteMode = True, channel = servos.Servo.RIGHTCH)
        self.isOpen = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        moveToCentre(self)

        self._layout = QGridLayout()

        self.textbox = QLabel(self)
        self.textbox.setText("HELLO WORLD")
        self.setStyleSheet("QLabel {font: bold 18pt Roboto}")
        self.textbox.setMaximumHeight(100)


        button = QPushButton('LAUNCH\nSEQUENCE', self)
        button.setToolTip('A single button. Click it maybe?')
        button.setStyleSheet('QPushButton {background-color: red; color: black; font: bold 20pt Roboto}')
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setMaximumHeight(300)
        button.setMaximumWidth(350)
        button.clicked.connect(self.on_click)

        self._layout.addWidget(self.textbox, 0, 0)
        self._layout.addWidget(button, 1, 0)
        # self._layout.setAlignment(button, Qt.AlignHCenter)

        self.setLayout(self._layout)

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

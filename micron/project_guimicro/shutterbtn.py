#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)
# import stagecontrol
import servos
from extraFunctions import moveToCentre

import platform, ctypes

class Butt(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.customicon = os.path.join(base_dir, 'icons', 'shutterbtn.svg')

        self.title = 'Optical audio shutter'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.shutter = servos.Shutter(absoluteMode = True, channel = servos.Servo.RIGHTCH)
        self.isOpen = False

        # https://stackoverflow.com/a/1857/3211506
		# Windows = Windows, Linux = Linux, Mac = Darwin
        # For setting icon on Windows
		if platform.system() == "Windows":
            # https://stackoverflow.com/a/1552105/3211506
			myappid = 'NUS.Nanomaterials.ShutterBtn.0.16' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(QIcon(self.customicon))

        moveToCentre(self)

        self._layout = QGridLayout()
        self.textbox = QLabel(self)
        self.textbox.setText("HELLO WORLD\n")
        self.setStyleSheet("QLabel {font-weight: bold; font-size: 18pt; font-family: Roboto, 'Segoe UI'; }")
        self.textbox.setMaximumHeight(100)
        # self.textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        button = QPushButton('LAUNCH\nSEQUENCE', self)
        button.setToolTip('A single button. Click it maybe?')
        button.setStyleSheet("QPushButton {background-color: red; color: black; font-weight: bold; font-size: 20pt; font-family: Roboto, 'Segoe UI';}")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setMaximumHeight(300)
        button.setMaximumWidth(350)
        button.clicked.connect(self.on_click)

        self._layout.addWidget(self.textbox, 0, 0)

        # https://stackoverflow.com/a/25515321/3211506
        self.horizontal_wrapper = QWidget()
        self.horizontal_wrapper_layout = QHBoxLayout()
        self.horizontal_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_wrapper_layout.addStretch(1)
        self.horizontal_wrapper_layout.addWidget(button)
        self.horizontal_wrapper_layout.setStretchFactor(button, 3)
        self.horizontal_wrapper_layout.addStretch(1)
        self.horizontal_wrapper.setLayout(self.horizontal_wrapper_layout)

        self._layout.addWidget(self.horizontal_wrapper, 1, 0)



        # We still set this as this is not default behaviour on Windows
        self._layout.setAlignment(self.textbox, Qt.AlignCenter)
        # self._layout.setAlignment(button, Qt.AlignCenter)

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

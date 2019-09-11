#!/usr/bin/env python3

import sys, os
# import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
import time

import threading

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from extraFunctions import moveToCentre, ThreadWithExc

def informationDialog(message, title = "Information", informativeText = None, host = None):
    _msgBox = QtWidgets.QMessageBox(host)
    _msgBox.setIcon(QtWidgets.QMessageBox.Information)
    _msgBox.setWindowTitle(title)
    _msgBox.setText(message)
    if informativeText is not None:
        _msgBox.setInformativeText(informativeText)

    # Get height and width
    _h = _msgBox.height()
    _w = _msgBox.width()
    _msgBox.setGeometry(0, 0, _w, _h)

    moveToCentre(_msgBox)

    # mb.setTextFormat(Qt.RichText)
    # mb.setDetailedText(message)

    # _msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    return _msgBox.exec_()




class fenster(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.window_widget = QtWidgets.QWidget()
        self.window_widget_layout = QtWidgets.QVBoxLayout()

        self.btn = QtWidgets.QPushButton("PUSH")
        self.btn.clicked.connect(lambda: self.showThread())

        self.window_widget_layout.addWidget(self.btn)

        self.window_widget.setLayout(self.window_widget_layout)
        self.setCentralWidget(self.window_widget)

        self.wank = QtCore.pyqtSignal()
        self.wank.connect(lambda: showDialog())

    def showThread(self):
        q = ThreadWithExc(target=self._thread)

        q.start()

    def _thread(self):
        time.sleep(5)

        self.wank.emit()

    def showDialog(self):
        informationDialog(message = "hi")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = fenster()
    # Start the signal handler
    # window.startInterruptHandler()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

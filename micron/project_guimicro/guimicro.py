#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Graphical User Interface for stagecontrol.py

# Swapped to PyQt5 from Tkinter, because the former is more powerful/intuitive to implement features
# microgui will pair functions with commands imported from stagecontrol.py which uses raster in turn

# I'm sorry to whoever has to maintain this GUI code. I tried my best to make it as clear and precise as 
# possible but it like trying to make a HTML page using pure JavaScript and it's well...messy

# The helper codes used in this are meant to be extensible for any weird scale coding projects that you might want

# Made 2019, Sun Yudong, Wu Mingsong
# sunyudong [at] outlook [dot] sg, mingsongwu [at] outlook [dot] sg

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time

from contextlib import redirect_stdout
import io, threading

sys.path.insert(0, '../')
import stagecontrol

class MicroGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50,50,500,300) # x, t, w, h
        
        moveToCentre(self)
        
        self.setWindowTitle('Micos Stage Controller MARK II 0.01a')
        self.setWindowIcon(QtGui.QIcon('./pictures/icon.bmp'))

        # Essentially the steps for the gui works like this
        # Create a widget -> Create a layout -> Add widgets to layout -> Assign layout to widget -> Assign widget to window

        # WINDOW_WIDGET
        self.window_widget = QtWidgets.QWidget()
        self.window_layout = QtWidgets.QVBoxLayout()

        # MENU
        self.createMenu()
        # / MENU

        # MODE WIDGET
        self.mode_widget = self.createModes()
        self.window_layout.addWidget(self.mode_widget)
        # / MODE WIDGET

        # MAIN WIDGET
        self.main_widget = QtWidgets.QStackedWidget() # We use stacked widget to avoid using a stackedlayout

        # Add widgets in order of the top menu
        # DrawPic, Single Raster, Array Raster, Stage Movement
        self.drawpic_widget = self.create_drawpic()
        self.single_raster_widget = self.create_single_raster()
        self.array_raster_widget = self.create_array_raster()
        self.stage_widget = self.create_stage()

        self.main_widget.addWidget(self.drawpic_widget)
        self.main_widget.addWidget(self.single_raster_widget)
        self.main_widget.addWidget(self.array_raster_widget)
        self.main_widget.addWidget(self.stage_widget)

        # / MAIN WIDGET
        self.window_layout.addWidget(self.main_widget)

        # / WINDOW_WIDGET
        self.window_widget.setLayout(self.window_layout)

        # WRAP UP
        self.setCentralWidget(self.window_widget)

        self.initializeDevice()

        # Show actual window
        self.show()

    def initializeDevice(self):
        # We create a blocked window which the user cannot close
        initWindow = QtWidgets.QDialog()
        initWindow.setWindowTitle("Initializing...")
        initWindow.setGeometry(50,50,300,200)
        initWindow.setWindowFlags(QtCore.Qt.WindowType.WindowTitleHint | QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowMaximizeButtonHint | QtCore.Qt.WindowType.CustomizeWindowHint) 
        moveToCentre(initWindow)

        initWindow_layout = QtWidgets.QVBoxLayout()

        initWindow_wrapper_widget = QtWidgets.QWidget()
        initWindow_wrapper_layout = QtWidgets.QVBoxLayout()        

        statusLabel = QtWidgets.QLabel("Initializing...")
        statusLabel.setWordWrap(True)
        statusLabel.setMaximumWidth(250)

        topLabel = QtWidgets.QLabel("--- INITIALIZING STAGECONTROL---")
        topLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bottomLabel = QtWidgets.QLabel("-- PLEASE DO NOT CLOSE --")
        bottomLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        lineC = QtWidgets.QFrame()
        lineC.setFrameShape(QtWidgets.QFrame.Shape.HLine);
        lineD = QtWidgets.QFrame()
        lineD.setFrameShape(QtWidgets.QFrame.Shape.HLine);

        initWindow_wrapper_layout.addWidget(topLabel)
        initWindow_wrapper_layout.addWidget(lineC)
        initWindow_wrapper_layout.addStretch(1)
        initWindow_wrapper_layout.addWidget(statusLabel)
        initWindow_wrapper_layout.addStretch(1)
        initWindow_wrapper_layout.addWidget(lineD)
        initWindow_wrapper_layout.addWidget(bottomLabel)
        initWindow_wrapper_widget.setLayout(initWindow_wrapper_layout)

        initWindow_layout.addWidget(initWindow_wrapper_widget)
        initWindow.setLayout(initWindow_layout)

        # We create a file-like object to capture the micron-messages
        f = io.StringIO()
        l = []

        def initMicron():
            with redirect_stdout(f):
                self.stageControl = stagecontrol.StageControl()
                # for i in range(4):
                #     print("Message number:", i)
                #     time.sleep(1)

        def printStuff():
            prevValue = ""
            while True:
                q = f.getvalue()

                if q != prevValue:
                    prevValue = q
                    status = q.split("\n")[-2].strip()

                    # l.append(status)
                    # initWindow.setWindowTitle(q.split()[-1].strip())

                    statusLabel.setText(status)

                if threading.activeCount() == baselineThreads:
                    # The initialization is done and we quit the initWindow
                    initWindow.close()
                    break
                
                time.sleep(0.5) # We have to sleep to release the lock on f

        thread1 = threading.Thread(target = initMicron, args = ())
        thread2 = threading.Thread(target = printStuff, args = ())

        thread1.start()
        baselineThreads = threading.activeCount()
        thread2.start()

        # We need exec so that the event loop is started to show the widgets
        initWindow.exec() 

        # We end the initWindow from the thread itself since code below .exec() doesn't actually get run
        # This is because .exec() starts a loop that blocks the process

        # thread1.join()
        # thread2.join()
        # initWindow.close()

# We declare a decorator to initialize a widget and assign the layout
    def make_widget_from_layout(function):
        def wrapper(self):
            # We create a widget
            widget = QtWidgets.QWidget()
            # Get the layout
            layout = function(self, widget)
            # Assign the layout to the widget
            widget.setLayout(layout)

            return widget

        return wrapper

# Menu
    def createMenu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")        

        settings = QtWidgets.QAction("Settings", self)
        settings.setShortcut("Ctrl+,")
        settings.setStatusTip('Configure the application')
        # settings.triggered.connect(self.showSettings)
        file_menu.addAction(settings)

        quit = QtWidgets.QAction("Quit", self)
        quit.setShortcut("Ctrl+Q")
        quit.setStatusTip('Exit application')
        quit.triggered.connect(self.close)
        file_menu.addAction(quit)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")    

        about = QtWidgets.QAction("About", self)
        about.setStatusTip('About this application')
        about.triggered.connect(self.showAbout)
        help_menu.addAction(about)

    def showAbout(self):
        self.exPopup = aboutPopUp()
        self.exPopup.setGeometry(100, 200, 200, 300)
        self.exPopup.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.exPopup.exec()  # show()
        # buttonReply = QtWidgets.QMessageBox.about(self, 'About', "Made 2019, Sun Yudong, Wu Mingsong\n\nsunyudong [at] outlook [dot] sg\n\nmingsongwu [at] outlook [dot] sg")

# Top row buttons
    @make_widget_from_layout
    def createModes(self, widget):
        _mode_layout = QtWidgets.QHBoxLayout()
        _modes = [
            QtWidgets.QPushButton("Draw Picture") ,
            QtWidgets.QPushButton("Array Raster") ,
            QtWidgets.QPushButton("Single Raster") ,
            QtWidgets.QPushButton("Stage Movement")
        ]

        for i, btn in enumerate(_modes):
            btn.triggered.conenct(lambda: self.showPage(i))

        for btn in _modes:
            _mode_layout.addWidget(btn)

        return _mode_layout

    def showPage(self, page):
        # Page 0 = Draw Picture
        # Page 1 = Array Raster
        # Page 2 = Single Raster
        # Page 3 = Stage Movement
        self.main_widget.setCurrentIndex(page)

# first layout
    @make_widget_from_layout
    def create_stage(self, widget):
        # Create all child elements
        # _velocity = QtWidgets.QLineEdit()
        # _velocity.setValidator(QtGui.QIntValidator(0,1000))
        # _velocity.setFont(QtGui.QFont("Arial",20))

        # _step_size = QtWidgets.QLineEdit()
        # _step_size.setValidator(QtGui.QIntValidator(0.5,1000))
        # _step_size.setFont(QtGui.QFont("Arial",20))

        # need to link to stagecontrol to read position of controllers
        _lcdx = QtWidgets.QLCDNumber()
        _lcdy = QtWidgets.QLCDNumber()

        # Create the layout with the child elements
        _stage_layout = QtWidgets.QGridLayout()
        # _stage_layout.addWidget(_velocity, 0, 0)
        # _stage_layout.addWidget(_step_size, 0, 1)
        _stage_layout.addWidget(_lcdx, 0, 0)
        _stage_layout.addWidget(_lcdy, 0, 1)

        return _stage_layout

# second layout
    @make_widget_from_layout
    def create_single_raster(self):
        return _single_raster_layout

# third layout
    @make_widget_from_layout
    def create_array_raster(self):
        return _array_raster_layout

# fourth layout
    @make_widget_from_layout
    def create_drawpic(self):
        return _drawpic_layout

# Status Bar

class aboutPopUp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lblName = QtWidgets.QLabel("FILL IN SOME ABOUT TEXT HERE", self)

def moveToCentre(QtObj):
    # Get center of the window and move the window to the centre
    # Remember to setGeometry of the object first
    # https://pythonprogramminglanguage.com/pyqt5-center-window/
    _qtRectangle = QtObj.frameGeometry()
    _centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    _qtRectangle.moveCenter(_centerPoint)
    QtObj.move(_qtRectangle.topLeft())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MicroGui()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# final level Graphical User Interface for stagecontrol.py

# Swapped to PyQt5 from Tkinter, because the former is more powerful/intuitive to implement features
# microgui will pair functions with commands imported from stagecontrol.py which uses raster in turn

# I'm sorry to whoever has to maintain this GUI code. I tried my best to make it as clear and precise as
# possible but it like trying to make a HTML page using pure JavaScript and it's well...messy

# The helper codes used in this are meant to be extensible for any weird scale coding projects that you might want

# Made 2019, Sun Yudong, Wu Mingsong
# sunyudong [at] outlook [dot] sg, mingsongwu [at] outlook [dot] sg

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
import time, datetime

import argparse

from contextlib import redirect_stdout
import io, threading

import traceback

import math

# To catch Ctrl+C
import signal

sys.path.insert(0, '../')
import stagecontrol
import shutterpowerranger

class MicroGui(QtWidgets.QMainWindow):
    def __init__(self, devMode = False, noHome = False):
        super().__init__()

        self.micronInitialized = False
        self.currentStatus = ""
        self.devMode = devMode

        self.noHome = noHome

        # symboldefs
        self.MICROSYMBOL = u"\u00B5"

        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 700, 500) # x, y, w, h

        moveToCentre(self)

        self.setWindowTitle('Micos Stage Controller MARK II 0.01a')
        self.setWindowIcon(QtGui.QIcon('./pictures/icon.bmp'))

        # Essentially the steps for the gui works like this
        # Create a widget -> Create a layout -> Add widgets to layout -> Assign layout to widget -> Assign widget to window

        # FONTS AND STYLES
        # TODO INSERT SOME HERE

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
        self.main_widget.addWidget(self.array_raster_widget)
        self.main_widget.addWidget(self.single_raster_widget)
        self.main_widget.addWidget(self.stage_widget)

        # / MAIN WIDGET
        self.window_layout.addWidget(self.main_widget)

        # SHUTTER WIDGET
        self.shutter_widget = self.create_shutter_control()
        self.window_layout.addWidget(self.shutter_widget)
        # / SHUTTER WIDGET

        # STATUS BAR WIDGET
        self.statusBarWidget = QtWidgets.QStatusBar()
        self._statusbar_label = QtWidgets.QLabel("status")
        self.setStyleSheet("QStatusBar::item { border: 0px solid black };");            # Remove border around the status
        self.statusBarWidget.addWidget(self._statusbar_label, stretch = 1)
        self.setStatusBar(self.statusBarWidget)
        # / STATUS BAR WIDGET

        # / WINDOW_WIDGET
        self.window_widget.setLayout(self.window_layout)

        # WRAP UP
        self.setCentralWidget(self.window_widget)

        self.initializeDevice()
        self.initEventListeners()

        # Set to the last menu item
        self.showPage(self.main_widget.count() - 1)

        # Show actual window
        self.show()

    def startInterruptHandler(self):
        # Usually not started because signal doesn't work with PyQt anyway

        # https://stackoverflow.com/a/4205386/3211506
        signal.signal(signal.SIGINT, self.KeyboardInterruptHandler)

    def KeyboardInterruptHandler(self, signal = None, frame = None):
        # 2 args above for use with signal.signal

        self.setOperationStatus("^C Detected: Aborting the FIFO stack. Shutter will be closed as part of the aborting process.")

        if not self.devMode:
            self.stageControl.controller.abort()
            self.StageControl.controller.shutter.close()

            # Some code here to detect printing/array state

        # self.dev.close()
        # print("Exiting")
        # sys.exit(1)
        # use os._exit(1) to avoid raising any SystemExit exception

    def initializeDevice(self):
        # We create a blocked window which the user cannot close
        initWindow = QtWidgets.QDialog()
        initWindow.setWindowTitle("Initializing...")
        self.setOperationStatus("Initializing StageControl()")
        initWindow.setGeometry(50, 50, 300, 200)
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
        bottomLabel = QtWidgets.QLabel("-- PLEASE WAIT AND DO NOT CLOSE --")
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
                if self.devMode:
                    # Following code is for testing and emulation of homing commands
                    # for i in range(2):
                    #     print("Message number:", i)
                    #     time.sleep(1)
                    self.stageControl = stagecontrol.StageControl(noCtrlCHandler = True, devMode = True, GUI_Object = self)

                else:
                    try:
                        self.stageControl = stagecontrol.StageControl(noCtrlCHandler = True, GUI_Object = self, shutter_channel = shutterpowerranger.Servo.RIGHTCH, noHome = self.noHome)
                    except RuntimeError as e:
                        initWindow.close()
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                        msgBox.setWindowTitle("Oh no!")
                        msgBox.setText("System has encountered a RuntimeError and will now exit.")
                        msgBox.setInformativeText("Error: {}".format(e))
                        moveToCentre(msgBox)

                        # mb.setTextFormat(Qt.RichText)
                        # mb.setDetailedText(message)

                        msgBox.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

                        ret = msgBox.exec_()
                        os._exit(1)             # For the exit to propogate upwards

            self.micronInitialized = True
            self.setOperationStatus("StageControl Initialized")

        def printStuff():
            prevValue = ""
            while True:
                q = f.getvalue()

                if q != prevValue:
                    prevValue = q
                    status = q.split("\n")[-2].strip()

                    # l.append(status)
                    # initWindow.setWindowTitle(q.split()[-1].strip())
                    self.setOperationStatus(status, printToTerm = False)
                    statusLabel.setText(status)

                if threading.activeCount() == baselineThreads:
                    # The initialization is done and we quit the initWindow
                    self.updatePositionDisplay()
                    initWindow.close()
                    break

                time.sleep(0.5) # We have to sleep to release the lock on f

        thread1 = threading.Thread(target = initMicron, args = ())
        thread2 = threading.Thread(target = printStuff, args = ())

        thread1.start()
        baselineThreads = threading.activeCount()
        thread2.start()

        # We need exec so that the event loop is started to show the widgets
        initWindow.exec_()

        # We end the initWindow from the thread itself since code below .exec() doesn't actually get run
        # This is because .exec() starts a loop that blocks the process
        # exec() and exec_() is equivalent for Py3

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
        self.exPopup.exec_()  # show()
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

        # for i, btn in enumerate(_modes):
        #     _modes[i].clicked.connect(lambda: self.showPage(i))

        # Somehow I cannot dynamic the showpage index

        _modes[0].clicked.connect(lambda: self.showPage(0))
        _modes[1].clicked.connect(lambda: self.showPage(1))
        _modes[2].clicked.connect(lambda: self.showPage(2))
        _modes[3].clicked.connect(lambda: self.showPage(3))

        for btn in _modes:
            _mode_layout.addWidget(btn)

        return _mode_layout

    def showPage(self, page):
        # Page 0 = Draw Picture
        # Page 1 = Array Raster
        # Page 2 = Single Raster
        # Page 3 = Stage Movement
        self.main_widget.setCurrentIndex(page)

# Shutter Control layout

    @make_widget_from_layout
    def create_shutter_control(self, widget):
        _shutter_layout = QtWidgets.QHBoxLayout()

        # Shutter controls
        self._shutter_label = QtWidgets.QLabel("Shutter Controls")
        self._shutter_state = QtWidgets.QLabel() # Change color
        self._open_shutter  = QtWidgets.QPushButton("Open")
        self._close_shutter = QtWidgets.QPushButton("Close")

        self._shutter_state.setStyleSheet("QLabel { background-color: #DF2928; }")
        self._shutter_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        _shutter_layout.addWidget(self._shutter_label)
        _shutter_layout.addWidget(self._shutter_state)
        _shutter_layout.addWidget(self._open_shutter)
        _shutter_layout.addWidget(self._close_shutter)

        return _shutter_layout

# first layout
    @make_widget_from_layout
    def create_stage(self, widget):
        # Create all child elements

        # need to link to stagecontrol to read position of controllers

        # LCDS
        _lcdx_label = QtWidgets.QLabel("Current X")
        _lcdy_label = QtWidgets.QLabel("Current Y")
        _lcdx_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        _lcdy_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        _lcdx_label.setMaximumHeight(20)
        _lcdy_label.setMaximumHeight(20)

        self._lcdx = QtWidgets.QLCDNumber()
        self._lcdy = QtWidgets.QLCDNumber()
        # TODO: Some styling here for the QLCD number

        # BUTTONS
        self._upArrow    = QtWidgets.QPushButton(u'\u21E7')
        self._downArrow  = QtWidgets.QPushButton(u'\u21E9')
        self._leftArrow  = QtWidgets.QPushButton(u'\u21E6')
        self._rightArrow = QtWidgets.QPushButton(u'\u21E8')
        self._homeBtn    = QtWidgets.QPushButton("Home\nStage")

        self.arrowFont = QtGui.QFont("Arial", 30)
        self.arrowFont.setBold(True)

        self._upArrow.setFont(self.arrowFont); self._downArrow.setFont(self.arrowFont); self._leftArrow.setFont(self.arrowFont); self._rightArrow.setFont(self.arrowFont);

        # SETTINGS AND PARAMS
        _velocity_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _velocity_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        _step_size_label = QtWidgets.QLabel("Step size ({}m)".format(self.MICROSYMBOL))

        self._SL_velocity = QtWidgets.QLineEdit()
        self._SL_velocity.setText('100')
        self._SL_velocity.setValidator(QtGui.QIntValidator(0,10000))
        # _velocity.setFont(QtGui.QFont("Arial",20))

        self._step_size = QtWidgets.QLineEdit()
        self._step_size.setText('10')
        self._step_size.setValidator(QtGui.QIntValidator(0.5,1000))
        # _step_size.setFont(QtGui.QFont("Arial",20))

        # Create the layout with the child elements
        _stage_layout = QtWidgets.QGridLayout()

        # void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        # void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())

        # currx, y label
        _stage_layout.addWidget(_lcdx_label, 0, 1, 1, 2)
        _stage_layout.addWidget(_lcdy_label, 0, 3, 1, 2)

        _stage_layout.addWidget(self._lcdx, 1, 1, 1, 2)
        _stage_layout.addWidget(self._lcdy, 1, 3, 1, 2)

        _stage_layout.addWidget(_lcdx_label, 0, 1, 1, 2)
        _stage_layout.addWidget(_lcdy_label, 0, 3, 1, 2)

        _stage_layout.addWidget(_velocity_label, 2, 0)
        _stage_layout.addWidget(self._SL_velocity, 2, 1, 1, 2)
        _stage_layout.addWidget(self._step_size, 2, 3, 1, 2)
        _stage_layout.addWidget(_step_size_label, 2, 5)

        _stage_layout.addWidget(self._upArrow, 4, 2, 1, 2)
        _stage_layout.addWidget(self._downArrow, 5, 2, 1, 2)
        _stage_layout.addWidget(self._leftArrow, 5, 0, 1, 2)
        _stage_layout.addWidget(self._rightArrow, 5, 4, 1, 2)

        _stage_layout.addWidget(self._homeBtn, 4, 0, 1, 2)

        return _stage_layout

# second layout
    @make_widget_from_layout
    def create_single_raster(self, widget):
        _single_raster_layout = QtWidgets.QGridLayout()

        _single_raster_layout.addWidget(QtWidgets.QLabel("Single Raster Layout"))

        return _single_raster_layout

# third layout
    @make_widget_from_layout
    def create_array_raster(self, widget):
        # Widget defs

        # AR_initial_settings
        # self.AR_initial_settings = QtWidgets.QGroupBox("Initial Values")
        # self.AR_initial_settings_layout = QtWidgets.QVBoxLayout()
        #
        # self.AR_initial_settings.setLayout(self.AR_initial_settings_layout)
        # / AR_initial_settings


        # Create Layout to add widgets
        _array_raster_layout = QtWidgets.QGridLayout()

        _array_raster_layout.addWidget(QtWidgets.QLabel("Array Raster Layout"))

        # Velocities, comma separated
        # Size
        # Power, comma separated

        # JUMP TO DEF
        # def arrayraster(self, xDist, yDist, xGap, yGap, rasterSettings, nrow, ncol, inipower, finxpower, finypower, inivel, finxvel, finyvel, returnToOrigin = False):

        # Raster in a rectangle
		# rasterSettings = {
		# 	"direction": "x" || "y" || "xy", 		# Order matters here xy vs yx
		# 	"step": 1								# If set to xy, step is not necessary
		# }

        # _

        return _array_raster_layout

# fourth layout
    @make_widget_from_layout
    def create_drawpic(self, widget):
        _drawpic_layout = QtWidgets.QGridLayout()

        _drawpic_layout.addWidget(QtWidgets.QLabel("Draw Pic Layout"))

        return _drawpic_layout

# INTERACTION FUNCTONS

    def initEventListeners(self):
        self.UP, self.RIGHT, self.DOWN, self.LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)

        self.cardinalStageMoving = False

        self._upArrow.clicked.connect(lambda: self.cardinalMoveStage(self.UP))
        self._downArrow.clicked.connect(lambda: self.cardinalMoveStage(self.DOWN))
        self._leftArrow.clicked.connect(lambda: self.cardinalMoveStage(self.LEFT))
        self._rightArrow.clicked.connect(lambda: self.cardinalMoveStage(self.RIGHT))
        self._homeBtn.clicked.connect(lambda: self.homeStage())

        self.keyMapping = {
            QtCore.Qt.Key_Up   : "Up",
            QtCore.Qt.Key_Down : "Down",
            QtCore.Qt.Key_Left : "Left",
            QtCore.Qt.Key_Right: "Right"
        }

        # self.keysPressed = {}
        # Not implementing due to not being able to obtain keyPress events reliably

        self.stage_widget.installEventFilter(self)
        self.installEventFilter(self)

        # Shutter
        self._close_shutter.clicked.connect(lambda: self.stageControl.controller.shutter.close())
        self._open_shutter.clicked.connect(lambda: self.stageControl.controller.shutter.open())



    # keyPressEvent(self, evt)

    def eventFilter(self, source, evt):
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qt.html#Key-enum
        # print(evt)

        if isinstance(evt, QtGui.QKeyEvent): #.type() ==
            # Check source here
            evtkey = evt.key()

            # if (evt.type() == QtCore.QEvent.KeyPress):
            #     print("KeyPress : {}".format(key))
            #     if key not in self.keysPressed:
            #         self.keysPressed[key] = 1

                # if key in self.keysPressed:
                #     del self.keysPressed[key]
            # print("\033[K", str(self.keysPressed), end="\r")

            if (evt.type() == QtCore.QEvent.KeyRelease):
                # print("KeyRelease : {}".format(evtkey))

                # All KeyRelease events go here
                if evtkey == QtCore.Qt.Key_C and (evt.modifiers() & QtCore.Qt.ControlModifier):
                    # Will work everywhere
                    self.KeyboardInterruptHandler()

                    return True # Prevents further handling

                if evtkey == QtCore.Qt.Key_Space:
                    self.stageControl.controller.shutter.close() if self.stageControl.controller.shutter.isOpen else self.stageControl.controller.shutter.open()
                    return True # Prevents further handling

                if evtkey == QtCore.Qt.Key_Up and source == self.stage_widget:
                    # print("Up")
                    self.cardinalMoveStage(self.UP)

                if evtkey == QtCore.Qt.Key_Down and source == self.stage_widget:
                    # print("Down")
                    self.cardinalMoveStage(self.DOWN)

                if evtkey == QtCore.Qt.Key_Left and source == self.stage_widget:
                    # print("Left")
                    self.cardinalMoveStage(self.LEFT)

                if evtkey == QtCore.Qt.Key_Right and source == self.stage_widget:
                    # print("Right")
                    self.cardinalMoveStage(self.RIGHT)

        # return QtWidgets.QWidget.eventFilter(self, source, evt)
        return super(QtWidgets.QWidget, self).eventFilter(source, evt)

    def homeStage(self):
        if not self.devMode:
            self.setOperationStatus("Homing stage...If any error arises, abort immediately with Ctrl + C")
            self.stageControl.controller.homeStage()
            self.setOperationStatus("Home stage finished")
        else:
            self.setOperationStatus("devMode, not homing...")

    def cardinalMoveStage(self, dir):
        # Get the distance
        dist = float(self._step_size.text())
        vel  = float(self._SL_velocity.text())

        # Move the stage
        if not self.devMode:
            self.moveStage(dir, distance = dist, velocity = vel)

    def moveStage(self, dir, distance, velocity):
        # dir is a (dx, dy) tuple/vector that defines the direction that gets multiplied by distance
        if sum(map(abs, dir)) > 1:
            _mag = math.sqrt(dir[0]**2 + dir[1]**2)
            dir = dir[0] / _mag , dir[1] / _mag

        if not self.cardinalStageMoving:
            self.cardinalStageMoving = True

            if self.stageControl.controller.velocity != velocity:
                # We reset the velocity if it is different
                self.stageControl.controller.setvel(velocity)

            self.stageControl.controller.rmove(x = dir[0] * distance, y = dir[1] * distance)
            self.updatePositionDisplay()

            self.cardinalStageMoving = False

    def updatePositionDisplay(self):
        if self.stageControl is not None:
            self._lcdx.display(self.stageControl.controller.stage.x)
            self._lcdy.display(self.stageControl.controller.stage.y)

    def setOperationStatus(self, status, printToTerm = True):
        self.currentStatus = status
        if printToTerm:
            print("[{}]".format(datetime.datetime.now().time()), status)
        # Do some updating of the status bar
        self._statusbar_label.setText(status)

# Status Bar

class aboutPopUp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lblName = QtWidgets.QLabel("Made by\n\nSun Yudong, Wu Mingsong\n\n2019\n\nsunyudong [at] outlook [dot] sg\n\nmingsongwu[at] outlook [dot] sg", self)

def moveToCentre(QtObj):
    # Get center of the window and move the window to the centre
    # Remember to setGeometry of the object first
    # https://pythonprogramminglanguage.com/pyqt5-center-window/
    _qtRectangle = QtObj.frameGeometry()
    _centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    _qtRectangle.moveCenter(_centerPoint)
    QtObj.move(_qtRectangle.topLeft())

def main(**kwargs):
    app = QtWidgets.QApplication(sys.argv)
    window = MicroGui(**kwargs)
    # Start the signal handler
    # window.startInterruptHandler()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--devMode', help="Use DevMode so that StageControl is not initialized", action='store_true')
    parser.add_argument('-H', '--noHome', help="Stage will not be homed", action='store_true')
    args = parser.parse_args()

    main(devMode = args.devMode, noHome = args.noHome)

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
# import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
import time, datetime
from PIL import Image as PILImage
import argparse

# AUDIO
from contextlib import redirect_stdout
import io, threading
# threading for interrupt
# multiprocessing so we can terminate the processes on abort

import traceback
import math
from functools import reduce

# To catch Ctrl+C
import signal

import platform, ctypes # For Windows Icon

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import stagecontrol, picConv
import servos
from micron import Stage as mstage # for default x and y lims

from extraFunctions import moveToCentre, ThreadWithExc, DoneObject

if platform.system() == "Windows":
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

class MicroGui(QtWidgets.QMainWindow):
    def __init__(self, devMode = False, noHome = False):
        super().__init__()

        self.micronInitialized = False
        self.currentStatus = ""
        self.devMode = devMode

        self.noHome = noHome

        self.customicon = os.path.join(base_dir, 'icons', 'guimicro.svg')

        self._DP_optionsChangedFlag = False

        # symboldefs
        self.MICROSYMBOL = u"\u00B5"

        self.KEYSTROKE_TIMEOUT = 10 # ms
        # Default based on 100ums / 10um
        # need to change on speed and interval change

        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 800, 700) # x, y, w, h

        # moveToCentre(self)

        self.setWindowTitle('Micos Stage Controller MARK II 0.15b')
        self.setWindowIcon(QtGui.QIcon(self.customicon))

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

        self.initSettings()
        self.initEventListeners()
        self.initializeDevice()
        self.winAudioSetMuted(False)
        self.recalculateARValues()

        # Set to the last menu item
        self.showPage(self.main_widget.count() - 1)

        if platform.system() == "Windows":
            self.resize(self.minimumSizeHint())

        moveToCentre(self)

        # Show actual window
        self.show()

    def initSettings(self):
        # Here we make a QSettings Object and read data from it to populate default variables
        QtCore.QCoreApplication.setOrganizationName("NUS Nanomaterials Lab")
        QtCore.QCoreApplication.setOrganizationDomain("physics.nus.edu.sg")
        QtCore.QCoreApplication.setApplicationName("Micos Stage Controller and Shutter")
        # These settings are to be shared between this and shutterbtn

        self.qsettings = QtCore.QSettings()

        self.set_shutterAbsoluteMode = self.qsettings.value("shutter/absoluteMode", True, type = bool)
        self.set_shutterChannel      = self.qsettings.value("shutter/channel", servos.Servo.RIGHTCH, type = int)
        self.set_powerAbsoluteMode   = self.qsettings.value("power/absoluteMode", False, type = bool)
        self.set_invertx             = self.qsettings.value("stage/invertx", False, type = bool)
        self.set_inverty             = self.qsettings.value("stage/inverty", False, type = bool)
        self.set_stageConfig         = self.qsettings.value("stage/config", None, type = dict) # Should be a dictionary
        self.explicitNoHomeSet = self.noHome
        self.noHome                  = self.qsettings.value("stage/noHome", False, type = bool) if not self.noHome else self.noHome
        # Load nohome from settings only if not explicitly specified ^
        self.set_noFinishTone        = self.qsettings.value("audio/noFinishTone", True, type = bool)

        self.logconsole("Settings Loaded:\n\tShutterAbsolute = {}\n\tShutterChannel = {}\n\tPowerAbsolute = {}\n\tInvert-X = {}\n\tInvert-Y = {}\n\tStageConfig = {}\n\tnoHome = {}\n\tnoFinishTone = {}".format(
            self.set_shutterAbsoluteMode ,
            self.set_shutterChannel      ,
            self.set_powerAbsoluteMode   ,
            self.set_invertx             ,
            self.set_inverty             ,
            self.set_stageConfig         ,
            self.noHome                  ,
            self.set_noFinishTone        ,
        ))

        # Update GUI Checkboxes
        self._SL_invertx_checkbox.setChecked(self.set_invertx)
        self._SL_inverty_checkbox.setChecked(self.set_inverty)

        # Settings will be reloaded whenever the settings window is called

        # self.qsettings.sync()

    def startInterruptHandler(self):
        # Usually not started because signal doesn't work with PyQt anyway

        # https://stackoverflow.com/a/4205386/3211506
        signal.signal(signal.SIGINT, self.KeyboardInterruptHandler)

    def KeyboardInterruptHandler(self, signal = None, frame = None, abortTrigger = False):
        # 2 args above for use with signal.signal
        # ALt + B also aborts

        # Disable the abort button
        self._abortBtn.setEnabled(False)
        self._abortBtn.setStyleSheet("background-color: #ccc;")

        # Close shutter
        self.stageControl.controller.shutter.quietLog = True
        if not abortTrigger:
            self.setOperationStatus("^C Detected: Aborting the FIFO stack. Shutter will be closed as part of the aborting process.")
        else:
            self.setOperationStatus("Aborting the FIFO stack. Shutter will be closed as part of the aborting process.")
        self.stageControl.controller.shutter.close()
        self.stageControl.controller.shutter.quietLog = False
        # / Close shutter

        # End all running threads
        main_thread = threading.main_thread()
        for p in threading.enumerate():
            if p is main_thread:
                continue

            if isinstance(p, ThreadWithExc):
                p.terminate()
        # / End all running threads

        if not self.devMode:
            self.stageControl.controller.abort()

        self._SR_start.setEnabled(True)
        self._AR_start.setEnabled(True)

        # Enable the abort button
        self._abortBtn.setStyleSheet("background-color: #DF2928;")
        self._abortBtn.setEnabled(True)

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
        initWindow.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.CustomizeWindowHint)
        initWindow.setWindowIcon(QtGui.QIcon(self.customicon))
        moveToCentre(initWindow)

        initWindow_layout = QtWidgets.QVBoxLayout()

        initWindow_wrapper_widget = QtWidgets.QWidget()
        initWindow_wrapper_layout = QtWidgets.QVBoxLayout()

        statusLabel = QtWidgets.QLabel("Initializing...")
        statusLabel.setWordWrap(True)
        statusLabel.setMaximumWidth(250)

        topLabel = QtWidgets.QLabel("--- INITIALIZING STAGECONTROL---")
        topLabel.setAlignment(QtCore.Qt.AlignCenter)
        bottomLabel = QtWidgets.QLabel("-- PLEASE WAIT AND DO NOT CLOSE --")
        bottomLabel.setAlignment(QtCore.Qt.AlignCenter)

        lineC = QtWidgets.QFrame()
        lineC.setFrameShape(QtWidgets.QFrame.HLine);
        lineD = QtWidgets.QFrame()
        lineD.setFrameShape(QtWidgets.QFrame.HLine);

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
            self.stageControl = None
            with redirect_stdout(f):
                if self.devMode:
                    # Following code is for testing and emulation of homing commands
                    # for i in range(2):
                    #     print("Message number:", i)
                    #     time.sleep(1)
                    self.stageControl = stagecontrol.StageControl(noCtrlCHandler = True, devMode = True, GUI_Object = self, shutter_channel = self.set_shutterChannel, shutterAbsolute = self.set_shutterAbsoluteMode, powerAbsolute = self.set_powerAbsoluteMode, noFinishTone = self.set_noFinishTone)

                else:
                    try:
                        self.stageControl = stagecontrol.StageControl(
                            noCtrlCHandler = True,
                            GUI_Object = self,
                            noHome = self.noHome,
                            noinvertx = -1 if self.set_invertx else 1,
                            noinverty = -1 if self.set_inverty else 1,
                            stageConfig = self.set_stageConfig,
                            shutter_channel = self.set_shutterChannel,
                            shutterAbsolute = self.set_shutterAbsoluteMode,
                            powerAbsolute = self.set_powerAbsoluteMode,
                            noFinishTone = self.set_noFinishTone,
                        )

                    except RuntimeError as e:
                        initWindow.close()

                        # mb.setTextFormat(Qt.RichText)
                        # mb.setDetailedText(message)
                        # msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

                        self.EL_self_criticalDialog.emit("System has encountered a RuntimeError and will now exit.", "Oh no!", "Error: {}".format(e), True)

            # Clean up unneeded settings

            del self.set_shutterChannel
            del self.set_shutterAbsoluteMode
            del self.set_powerAbsoluteMode
            del self.set_invertx
            del self.set_inverty
            del self.set_stageConfig
            del self.set_noFinishTone

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
        settings.triggered.connect(self.showSettings)
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
        self.exPopup = aboutPopUp(parent = self)
        self.exPopup.exec_()  # show()
        # buttonReply = QtWidgets.QMessageBox.about(self, 'About', "Made 2019, Sun Yudong, Wu Mingsong\n\nsunyudong [at] outlook [dot] sg\n\nmingsongwu [at] outlook [dot] sg")

    def showSettings(self):
        self.settingsScreen = SettingsScreen(parent = self)
        self.settingsScreen.exec_()

# Top row buttons
    @make_widget_from_layout
    def createModes(self, widget):
        _mode_layout = QtWidgets.QHBoxLayout()
        self._modes = [
            QtWidgets.QPushButton("Draw &Picture") ,
            QtWidgets.QPushButton("&Array Raster") ,
            QtWidgets.QPushButton("Single &Raster") ,
            QtWidgets.QPushButton("&Stage Movement")
        ]

        # for i, btn in enumerate(_modes):
        #     _modes[i].clicked.connect(lambda: self.showPage(i))

        # Somehow I cannot dynamic the showpage index

        self._modes[0].clicked.connect(lambda: self.showPage(0))
        self._modes[1].clicked.connect(lambda: self.showPage(1))
        self._modes[2].clicked.connect(lambda: self.showPage(2))
        self._modes[3].clicked.connect(lambda: self.showPage(3))

        for btn in self._modes:
            _mode_layout.addWidget(btn)

        return _mode_layout

    def showPage(self, page):
        # Page 0 = Draw Picture
        # Page 1 = Array Raster
        # Page 2 = Single Raster
        # Page 3 = Stage Movement

        # Change colour of the current tab
        self._modes[self.main_widget.currentIndex()].setStyleSheet("")
        self._modes[page].setStyleSheet("border : 0px; border-bottom : 4px solid #09c; padding-bottom: 3px; padding-top: -3px")

        self.main_widget.setCurrentIndex(page)

        if page == 3:
            self.updatePositionDisplay()

# Shutter Control layout
    @make_widget_from_layout
    def create_shutter_control(self, widget):
        _shutter_layout = QtWidgets.QGridLayout()

        # Shutter controls
        self._shutter_label = QtWidgets.QLabel("Shutter Controls")
        self._shutter_state = QtWidgets.QLabel() # Change color
        self._open_shutter  = QtWidgets.QPushButton("&Open")
        self._close_shutter = QtWidgets.QPushButton("&Close")
        self._abortBtn      = QtWidgets.QPushButton("A&bort")

        self._shutter_state.setStyleSheet("QLabel { background-color: #DF2928; }")
        self._shutter_state.setAlignment(QtCore.Qt.AlignCenter)
        self._abortBtn.setMinimumHeight(50)
        self._abortBtn.setStyleSheet("background-color: #DF2928;")

        _shutter_layout.addWidget(self._shutter_label, 0, 0)
        _shutter_layout.addWidget(self._shutter_state, 0, 1)
        _shutter_layout.addWidget(self._open_shutter, 0, 2)
        _shutter_layout.addWidget(self._close_shutter, 0, 3)
        _shutter_layout.addWidget(self._abortBtn, 1, 0, 1, 4)

        return _shutter_layout

# first layout
    @make_widget_from_layout
    def create_stage(self, widget):
        # Create all child elements

        # need to link to stagecontrol to read position of controllers

        # LCDS
        _lcdx_label = QtWidgets.QLabel("Current X")
        _lcdy_label = QtWidgets.QLabel("Current Y")
        _lcdx_label.setAlignment(QtCore.Qt.AlignCenter)
        _lcdy_label.setAlignment(QtCore.Qt.AlignCenter)
        _lcdx_label.setMaximumHeight(20)
        _lcdy_label.setMaximumHeight(20)

        self._lcdx = QtWidgets.QLCDNumber()
        self._lcdx.setDigitCount(8)
        self._lcdx.setSmallDecimalPoint(True)
        self._lcdx.setMaximumHeight(200)
        self._lcdx.setMinimumHeight(150)
        self._lcdy = QtWidgets.QLCDNumber()
        self._lcdy.setDigitCount(8)
        self._lcdy.setSmallDecimalPoint(True)
        self._lcdy.setMaximumHeight(200)
        self._lcdy.setMinimumHeight(150)
        # TODO: Some styling here for the QLCD number

        # BUTTONS
        self._upArrow    = QtWidgets.QPushButton(u'\u21E7')
        self._downArrow  = QtWidgets.QPushButton(u'\u21E9')
        self._leftArrow  = QtWidgets.QPushButton(u'\u21E6')
        self._rightArrow = QtWidgets.QPushButton(u'\u21E8')
        self._homeBtn    = QtWidgets.QPushButton("Home\nStage")

        self._stage_buttons = [
            self._upArrow    ,
            self._downArrow  ,
            self._leftArrow  ,
            self._rightArrow ,
            self._homeBtn    ,
        ]

        for btn in self._stage_buttons:
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            btn.setMaximumHeight(150)

        self.arrowFont = QtGui.QFont("Arial", 30)
        self.arrowFont.setBold(True)

        self._upArrow.setFont(self.arrowFont); self._downArrow.setFont(self.arrowFont); self._leftArrow.setFont(self.arrowFont); self._rightArrow.setFont(self.arrowFont);

        # SETTINGS AND PARAMS
        _velocity_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _velocity_label.setAlignment(QtCore.Qt.AlignRight)
        _step_size_label = QtWidgets.QLabel("Step size ({}m)".format(self.MICROSYMBOL))

        self._SL_velocity = QtWidgets.QLineEdit()
        self._SL_velocity.setText('100')
        self._SL_velocity.setValidator(QtGui.QDoubleValidator(0,10000, 12))
        # _velocity.setFont(QtGui.QFont("Arial",20))

        self._SL_step_size = QtWidgets.QLineEdit()
        self._SL_step_size.setText('10')
        self._SL_step_size.setValidator(QtGui.QDoubleValidator(0.5,10000, 12))
        # _step_size.setFont(QtGui.QFont("Arial",20))

        _SL_settings = QtWidgets.QWidget()
        _SL_settings_layout = QtWidgets.QVBoxLayout()
        self._SL_invertx_checkbox = QtWidgets.QCheckBox("Invert Horizontal")
        self._SL_inverty_checkbox = QtWidgets.QCheckBox("Invert Vertical")
        _SL_settings_layout.addWidget(self._SL_invertx_checkbox)
        _SL_settings_layout.addWidget(self._SL_inverty_checkbox)
        _SL_settings.setLayout(_SL_settings_layout)

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
        _stage_layout.addWidget(self._SL_step_size, 2, 3, 1, 2)
        _stage_layout.addWidget(_step_size_label, 2, 5)

        _stage_layout.addWidget(self._upArrow, 4, 2, 1, 2)
        _stage_layout.addWidget(self._downArrow, 5, 2, 1, 2)
        _stage_layout.addWidget(self._leftArrow, 5, 0, 1, 2)
        _stage_layout.addWidget(self._rightArrow, 5, 4, 1, 2)

        _stage_layout.addWidget(_SL_settings, 4, 4, 1, 2)

        _stage_layout.addWidget(self._homeBtn, 4, 0, 1, 2)

        return _stage_layout

# second layout
    @make_widget_from_layout
    def create_single_raster(self, widget):
        _single_raster_layout = QtWidgets.QGridLayout()

        # Velocity and power adjustments
        _SR_params = QtWidgets.QGroupBox("Parameters")
        _SR_params_layout = QtWidgets.QGridLayout()

        _SR_vel_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _SR_vel_label.setAlignment(QtCore.Qt.AlignHCenter| QtCore.Qt.AlignVCenter)

        _SR_pow_label = QtWidgets.QLabel("Power (steps)")
        _SR_pow_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self._SR_pow_up = QtWidgets.QPushButton("++")
        self._SR_pow_up.setToolTip("Increase Power")
        self._SR_pow_dn = QtWidgets.QPushButton("--")
        self._SR_pow_dn.setToolTip("Decrease Power")
        self._SR_pow_step = QtWidgets.QLineEdit()
        self._SR_pow_step.setText('1')
        self._SR_pow_step.setValidator(QtGui.QIntValidator(0,10000))
        self._SR_pow_step.setAlignment(QtCore.Qt.AlignHCenter)

        self._SR_velocity = QtWidgets.QLineEdit()
        self._SR_velocity.setText('100')
        self._SR_velocity.setValidator(QtGui.QDoubleValidator(0,10000, 12))
        self._SR_velocity.setAlignment(QtCore.Qt.AlignHCenter)

        _SR_params_layout.addWidget(_SR_vel_label, 0, 0, 1, 1)
        _SR_params_layout.addWidget(self._SR_velocity, 1, 0, 1, 1)
        _SR_params_layout.addWidget(_SR_pow_label, 0, 1, 1, 1)
        _SR_params_layout.addWidget(self._SR_pow_step, 1, 1, 1, 1)
        _SR_params_layout.addWidget(self._SR_pow_up, 0, 2, 1, 1)
        _SR_params_layout.addWidget(self._SR_pow_dn, 1, 2, 1, 1)

        _SR_params_layout.setColumnStretch(0, 1)
        _SR_params_layout.setColumnStretch(1, 1)
        _SR_params_layout.setColumnStretch(2, 1)

        _SR_params.setLayout(_SR_params_layout)
        # / Velocity and power adjustments

        # Box Settings
        _SR_settings = QtWidgets.QGroupBox("Settings")
        _SR_settings_layout = QtWidgets.QGridLayout()

        _SR_size_y_label = QtWidgets.QLabel("Height ({}m)".format(self.MICROSYMBOL))
        _SR_size_y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _SR_size_x_label = QtWidgets.QLabel("Width ({}m)".format(self.MICROSYMBOL))
        _SR_size_x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _SR_step_size_label = QtWidgets.QLabel("Step Size ({}m)".format(self.MICROSYMBOL))
        _SR_step_size_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._SR_size_x = QtWidgets.QLineEdit()
        self._SR_size_x.setText("10")
        self._SR_size_x.setValidator(QtGui.QDoubleValidator(1,10000,12))

        self._SR_size_y = QtWidgets.QLineEdit()
        self._SR_size_y.setText("10")
        self._SR_size_y.setValidator(QtGui.QDoubleValidator(1,10000,12))

        self._SR_step_size = QtWidgets.QLineEdit()
        self._SR_step_size.setText("1")
        self._SR_step_size.setValidator(QtGui.QDoubleValidator(0.1,10000,12))

        self._SR_raster_x = QtWidgets.QCheckBox()
        self._SR_raster_y = QtWidgets.QCheckBox()
        self._SR_raster_y.setChecked(True)
        _SR_raster_step_along_label = QtWidgets.QLabel("Steps?")
        _SR_raster_step_along_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        self._SR_raster_style = QtWidgets.QLabel("Filled square\nContinuous along y-axis")
        self._SR_raster_style.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        _SR_settings_layout.addWidget(_SR_step_size_label, 0, 0)
        _SR_settings_layout.addWidget(self._SR_step_size, 0, 1)
        _SR_settings_layout.addWidget(_SR_raster_step_along_label, 0, 2)
        _SR_settings_layout.addWidget(self._SR_raster_y, 1, 2)
        _SR_settings_layout.addWidget(self._SR_raster_x, 2, 2)
        _SR_settings_layout.addWidget(_SR_size_y_label, 1, 0)
        _SR_settings_layout.addWidget(_SR_size_x_label, 2, 0)
        _SR_settings_layout.addWidget(self._SR_size_y, 1, 1)
        _SR_settings_layout.addWidget(self._SR_size_x, 2, 1)
        _SR_settings_layout.addWidget(self._SR_raster_style, 3, 0, 1, 3)
        _SR_settings.setLayout(_SR_settings_layout)
        # / Box Settings

        # Action Buttons
        _SR_action_btns = QtWidgets.QWidget()
        _SR_action_btns_layout = QtWidgets.QGridLayout()

        # https://stackoverflow.com/a/33793752/3211506
        _SR_action_btns_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self._SR_retToOri = QtWidgets.QCheckBox("Return to Origin")
        self._SR_retToOri.setChecked(True)
        self._SR_start = QtWidgets.QPushButton("START")

        _SR_action_btns_layout.setColumnStretch(0, 0)

        _SR_action_btns_layout.addItem(_SR_action_btns_spacer, 0, 0)
        _SR_action_btns_layout.addWidget(self._SR_retToOri, 1, 0)
        _SR_action_btns_layout.addWidget(self._SR_start, 2, 0)
        _SR_action_btns.setLayout(_SR_action_btns_layout)
        # / Action Buttons

        _single_raster_layout.addWidget(_SR_settings, 0, 1, 1, 1)
        _single_raster_layout.addWidget(_SR_params, 1, 1, 1, 1)
        _single_raster_layout.addWidget(_SR_action_btns, 2, 1, 1, 1)

        _single_raster_layout.setColumnStretch(0, 1)
        _single_raster_layout.setColumnStretch(1, 2)
        _single_raster_layout.setColumnStretch(2, 1)

        return _single_raster_layout

# third layout
    @make_widget_from_layout
    def create_array_raster(self, widget):
        # https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/core/Qt.AlignmentFlag.html

        # Widget Defs

        # AR_initial_settings
        _AR_initial_settings = QtWidgets.QGroupBox("Initial Values")
        _AR_initial_settings_layout = QtWidgets.QGridLayout()

        _AR_init_vel_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _AR_init_vel_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        _AR_init_pow_label = QtWidgets.QLabel("Power (steps)")
        _AR_init_pow_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._AR_init_velocity = QtWidgets.QLineEdit()
        self._AR_init_velocity.setText('100')
        self._AR_init_velocity.setValidator(QtGui.QDoubleValidator(0,10000, 12))

        self._AR_init_power = QtWidgets.QLineEdit()
        self._AR_init_power.setText('0')
        self._AR_init_power.setValidator(QtGui.QIntValidator(0,10000))

        _AR_initial_settings_layout.addWidget(_AR_init_vel_label, 0, 0)
        _AR_initial_settings_layout.addWidget(_AR_init_pow_label, 1, 0)
        _AR_initial_settings_layout.addWidget(self._AR_init_velocity, 0, 1)
        _AR_initial_settings_layout.addWidget(self._AR_init_power, 1, 1)

        _AR_initial_settings.setLayout(_AR_initial_settings_layout)
        # / AR_initial_settings

        # AR_X_final_settings
        self._AR_X_final_settings = QtWidgets.QGroupBox("Calculated Final Values")
        _AR_X_final_settings_layout = QtWidgets.QGridLayout()

        _AR_X_final_vel_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _AR_X_final_vel_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _AR_X_final_pow_label = QtWidgets.QLabel("Power (steps)")
        _AR_X_final_pow_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._AR_X_final_velocity = QtWidgets.QLabel("0")
        self._AR_X_final_power = QtWidgets.QLabel("0")
        self._AR_X_final_velocity.setAlignment(QtCore.Qt.AlignVCenter)
        self._AR_X_final_power.setAlignment(QtCore.Qt.AlignVCenter)

        _AR_X_final_settings_layout.addWidget(_AR_X_final_vel_label, 0, 0)
        _AR_X_final_settings_layout.addWidget(_AR_X_final_pow_label, 1, 0)
        _AR_X_final_settings_layout.addWidget(self._AR_X_final_velocity, 0, 1)
        _AR_X_final_settings_layout.addWidget(self._AR_X_final_power, 1, 1)

        self._AR_X_final_settings.setLayout(_AR_X_final_settings_layout)
        # / AR_X_final_settings

        # AR_Y_final_settings
        self._AR_Y_final_settings = QtWidgets.QGroupBox("Calculated Final Values")
        _AR_Y_final_settings_layout = QtWidgets.QGridLayout()

        _AR_Y_final_vel_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _AR_Y_final_vel_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _AR_Y_final_pow_label = QtWidgets.QLabel("Power (steps)")
        _AR_Y_final_pow_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._AR_Y_final_velocity = QtWidgets.QLabel("0")
        self._AR_Y_final_power = QtWidgets.QLabel("0")
        self._AR_Y_final_velocity.setAlignment(QtCore.Qt.AlignVCenter)
        self._AR_Y_final_power.setAlignment(QtCore.Qt.AlignVCenter)

        _AR_Y_final_settings_layout.addWidget(_AR_Y_final_vel_label, 0, 0)
        _AR_Y_final_settings_layout.addWidget(_AR_Y_final_pow_label, 1, 0)
        _AR_Y_final_settings_layout.addWidget(self._AR_Y_final_velocity, 0, 1)
        _AR_Y_final_settings_layout.addWidget(self._AR_Y_final_power, 1, 1)

        self._AR_Y_final_settings.setLayout(_AR_Y_final_settings_layout)
        # / AR_Y_final_settings

        # X Interval
        _AR_X_interval_settings = QtWidgets.QGroupBox("Horizontal Settings")
        _AR_X_interval_settings_layout = QtWidgets.QGridLayout()

        self._AR_X_mode = QtWidgets.QComboBox()
        self._AR_X_mode.addItem("Velocity")
        self._AR_X_mode.addItem("Power")

        _AR_cols_label = QtWidgets.QLabel("NCols")
        _AR_cols_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._AR_cols = QtWidgets.QLineEdit()
        self._AR_cols.setText("1")
        self._AR_cols.setValidator(QtGui.QIntValidator(1,10000))

        _AR_X_intervals_label = QtWidgets.QLabel("Increment")
        _AR_X_intervals_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._AR_X_intervals = QtWidgets.QLineEdit()
        self._AR_X_intervals.setText("10")
        self._AR_X_intervals.setValidator(QtGui.QDoubleValidator(-10000,10000,12))
        # self._AR_X_intervals.setMinimumWidth(50)

        _AR_X_spacing_label = QtWidgets.QLabel("Spacing")
        _AR_X_spacing_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._AR_X_spacing = QtWidgets.QLineEdit()
        self._AR_X_spacing.setText("10")
        self._AR_X_spacing.setValidator(QtGui.QDoubleValidator(1,10000,12))

        _AR_X_interval_settings_layout.addWidget(self._AR_X_mode, 0, 0, 1, 2)
        _AR_X_interval_settings_layout.addWidget(_AR_X_intervals_label, 0, 2)
        _AR_X_interval_settings_layout.addWidget(self._AR_X_intervals, 0, 3)
        _AR_X_interval_settings_layout.addWidget(_AR_cols_label, 1, 0)
        _AR_X_interval_settings_layout.addWidget(self._AR_cols, 1, 1)
        _AR_X_interval_settings_layout.addWidget(_AR_X_spacing_label, 1, 2)
        _AR_X_interval_settings_layout.addWidget(self._AR_X_spacing, 1, 3)

        _AR_X_interval_settings.setLayout(_AR_X_interval_settings_layout)
        _AR_X_interval_settings.setStyleSheet("QGroupBox { background-color: rgba(0,0,0,0.1); }")
        # / X Interval

        # Y Interval
        _AR_Y_interval_settings = QtWidgets.QGroupBox("Vertical Settings")
        _AR_Y_interval_settings_layout = QtWidgets.QGridLayout()

        self._AR_Y_mode = QtWidgets.QComboBox()
        self._AR_Y_mode.addItem("Velocity")
        self._AR_Y_mode.addItem("Power")

        _AR_rows_label = QtWidgets.QLabel("NRows")
        _AR_rows_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self._AR_rows = QtWidgets.QLineEdit()
        self._AR_rows.setText("1")
        self._AR_rows.setValidator(QtGui.QIntValidator(1,10000))

        _AR_Y_intervals_label = QtWidgets.QLabel("Increment")
        _AR_Y_intervals_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self._AR_Y_intervals = QtWidgets.QLineEdit()
        self._AR_Y_intervals.setText("10")
        self._AR_Y_intervals.setValidator(QtGui.QDoubleValidator(-10000,10000,12))

        _AR_Y_spacing_label = QtWidgets.QLabel("Spacing")
        _AR_Y_spacing_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self._AR_Y_spacing = QtWidgets.QLineEdit()
        self._AR_Y_spacing.setText("10")
        self._AR_Y_spacing.setValidator(QtGui.QDoubleValidator(1,10000,12))

        _AR_Y_interval_settings_layout.addWidget(self._AR_Y_mode, 0, 0, 2, 1)
        _AR_Y_interval_settings_layout.addWidget(_AR_Y_intervals_label, 0, 1)
        _AR_Y_interval_settings_layout.addWidget(self._AR_Y_intervals, 1, 1)
        _AR_Y_interval_settings_layout.addWidget(_AR_rows_label, 2, 0)
        _AR_Y_interval_settings_layout.addWidget(self._AR_rows, 3, 0)
        _AR_Y_interval_settings_layout.addWidget(_AR_Y_spacing_label, 2, 1)
        _AR_Y_interval_settings_layout.addWidget(self._AR_Y_spacing, 3, 1)

        _AR_Y_interval_settings.setLayout(_AR_Y_interval_settings_layout)
        _AR_Y_interval_settings.setStyleSheet("QGroupBox { background-color: rgba(0,0,0,0.1); }")
        # / Y Interval

        # AR_XY_final_settings
        self._AR_XY_final_settings = QtWidgets.QGroupBox("Calculated Final Values")
        _AR_XY_final_settings_layout = QtWidgets.QGridLayout()

        _AR_XY_final_vel_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _AR_XY_final_vel_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _AR_XY_final_pow_label = QtWidgets.QLabel("Power (steps)")
        _AR_XY_final_pow_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._AR_XY_final_velocity = QtWidgets.QLabel("0")
        self._AR_XY_final_power = QtWidgets.QLabel("0")
        self._AR_XY_final_velocity.setAlignment(QtCore.Qt.AlignVCenter)
        self._AR_XY_final_power.setAlignment(QtCore.Qt.AlignVCenter)

        _AR_XY_final_settings_layout.addWidget(_AR_XY_final_vel_label, 0, 0)
        _AR_XY_final_settings_layout.addWidget(_AR_XY_final_pow_label, 1, 0)
        _AR_XY_final_settings_layout.addWidget(self._AR_XY_final_velocity, 0, 1)
        _AR_XY_final_settings_layout.addWidget(self._AR_XY_final_power, 1, 1)

        self._AR_XY_final_settings.setLayout(_AR_XY_final_settings_layout)
        # / AR_XY_final_settings

        # Arrows
        # https://www.compart.com/en/unicode/U+1F82F
        _right_dash  = QtWidgets.QLabel(u"\u25B6")
        _down_dash   = QtWidgets.QLabel(u"\u25BC")
        _right_arrow = QtWidgets.QLabel(u"\u25B6")
        _down_arrow  = QtWidgets.QLabel(u"\u25BC")
        _arrows = [_right_dash, _down_dash, _right_arrow, _down_arrow]

        for arr in _arrows:
            arr.setAlignment(QtCore.Qt.AlignCenter)
            # arr.setStyleSheet("line-height: 25px; font-size: 25px;")
        # / Arrows

        # Each Box Size
        _AR_size = QtWidgets.QGroupBox("Individual Raster Setting")
        _AR_size_layout = QtWidgets.QGridLayout()

        _AR_size_y_label = QtWidgets.QLabel("Height ({}m)".format(self.MICROSYMBOL))
        _AR_size_y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _AR_size_x_label = QtWidgets.QLabel("Width ({}m)".format(self.MICROSYMBOL))
        _AR_size_x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        _AR_step_size_label = QtWidgets.QLabel("Step Size ({}m)".format(self.MICROSYMBOL))
        _AR_step_size_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self._AR_size_x = QtWidgets.QLineEdit()
        self._AR_size_x.setText("10")
        self._AR_size_x.setValidator(QtGui.QDoubleValidator(1,10000,12))

        self._AR_size_y = QtWidgets.QLineEdit()
        self._AR_size_y.setText("10")
        self._AR_size_y.setValidator(QtGui.QDoubleValidator(1,10000,12))

        self._AR_step_size = QtWidgets.QLineEdit()
        self._AR_step_size.setText("1")
        self._AR_step_size.setValidator(QtGui.QDoubleValidator(0.1,10000,12))

        self._AR_raster_x = QtWidgets.QCheckBox()
        self._AR_raster_y = QtWidgets.QCheckBox()
        self._AR_raster_y.setChecked(True)
        _AR_raster_step_along_label = QtWidgets.QLabel("Steps?")
        _AR_raster_step_along_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        self._AR_raster_style = QtWidgets.QLabel("Filled square\nContinuous along y-axis")
        self._AR_raster_style.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        _AR_size_layout.addWidget(_AR_step_size_label, 0, 0)
        _AR_size_layout.addWidget(self._AR_step_size, 0, 1)
        _AR_size_layout.addWidget(_AR_raster_step_along_label, 0, 2)
        _AR_size_layout.addWidget(self._AR_raster_y, 1, 2)
        _AR_size_layout.addWidget(self._AR_raster_x, 2, 2)
        _AR_size_layout.addWidget(_AR_size_y_label, 1, 0)
        _AR_size_layout.addWidget(_AR_size_x_label, 2, 0)
        _AR_size_layout.addWidget(self._AR_size_y, 1, 1)
        _AR_size_layout.addWidget(self._AR_size_x, 2, 1)
        _AR_size_layout.addWidget(self._AR_raster_style, 3, 0, 1, 3)
        _AR_size.setLayout(_AR_size_layout)
        # / Each Box Size

        # Summary
        _AR_summary = QtWidgets.QGroupBox("Array Raster Summary")
        _AR_summary_layout = QtWidgets.QGridLayout()

        self._AR_summary_text = QtWidgets.QLabel("-")
        self._AR_summary_text.setAlignment(QtCore.Qt.AlignVCenter)

        _AR_summary_layout.addWidget(self._AR_summary_text, 0, 0)
        _AR_summary.setLayout(_AR_summary_layout)
        _AR_summary.setStyleSheet("QGroupBox { background-color: rgba(255, 165, 0, 0.4); }")
        # / Summary

        # Action Buttons
        _AR_action_btns = QtWidgets.QWidget()
        _AR_action_btns_layout = QtWidgets.QGridLayout()

        # https://stackoverflow.com/a/33793752/3211506
        _AR_action_btns_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self._AR_retToOri = QtWidgets.QCheckBox("Return to Origin")
        self._AR_retToOri.setChecked(True)
        self._AR_start = QtWidgets.QPushButton("START")

        _AR_action_btns_layout.setColumnStretch(0, 0)

        _AR_action_btns_layout.addItem(_AR_action_btns_spacer, 0, 0)
        _AR_action_btns_layout.addWidget(self._AR_retToOri, 1, 0)
        _AR_action_btns_layout.addWidget(self._AR_start, 2, 0)
        _AR_action_btns.setLayout(_AR_action_btns_layout)
        # / Action Buttons

        # void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        # void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())

        # Create Layout to add widgets
        _AR_numrows = 5
        _AR_numcols = 6
        _array_raster_layout = QtWidgets.QGridLayout()
        # Add widgets at position
        _array_raster_layout.addWidget(_AR_initial_settings, 0, 0)
        _array_raster_layout.addWidget(_right_dash, 0, 1)
        _array_raster_layout.addWidget(_AR_X_interval_settings, 0, 2, 1, 2)
        _array_raster_layout.addWidget(_right_arrow, 0, 4)
        _array_raster_layout.addWidget(self._AR_X_final_settings, 0, 5)
        _array_raster_layout.addWidget(_down_dash, 1, 0)
        _array_raster_layout.addWidget(_AR_Y_interval_settings, 2, 0)
        _array_raster_layout.addWidget(_down_arrow, 3, 0)
        _array_raster_layout.addWidget(_AR_size, 1, 2, 2, 2)
        _array_raster_layout.addWidget(_AR_summary, 4, 1, 1, 4)
        _array_raster_layout.addWidget(self._AR_Y_final_settings, 4, 0)
        _array_raster_layout.addWidget(self._AR_XY_final_settings, 4, 5)
        _array_raster_layout.addWidget(_AR_action_btns, 2, 5)

        # To ensure each row and column is the same width
        # https://stackoverflow.com/a/40154349/3211506
        for i in range(_AR_numrows):
            _array_raster_layout.setRowStretch(i, 1)
            for j in range(_AR_numcols):
                _array_raster_layout.setColumnStretch(j, 1)

        _array_raster_layout.setColumnStretch(1, 0.5)
        _array_raster_layout.setColumnStretch(4, 0.5)
        _array_raster_layout.setRowStretch(1, 0.5)
        _array_raster_layout.setRowStretch(3, 0.5)

        # Velocities, comma separated
        # Size
        # Power, comma separated

        return _array_raster_layout

# fourth layout
    @make_widget_from_layout
    def create_drawpic(self, widget):
        _drawpic_layout = QtWidgets.QGridLayout()

        # INSTRUCTION
        # _DP_instructions = QtWidgets.QGroupBox("Instructions")
        # _DP_instructions_layout = QtWidgets.QVBoxLayout()

        _DP_instructions_scrollArea = QtWidgets.QScrollArea() # QTextBrowser
        _DP_instructions_label = QtWidgets.QLabel()
        _DP_instructions_string = [
            "<b style='color: #22F;'>Instructions</b>",
            "'Draw Picture' takes in a 1-bit BMP image and prints it out using the stage.",
            "Each option has some hints on mouseover.",
            "Go through each step <span style='font-family: Menlo, Consolas, monospace;'>[i]</span> sequentially to print the image. Each pixel represents 1 {}m.".format(self.MICROSYMBOL),
            "Scale:<br>If x-scale = 2, this means that for every 1-pixel move along the x-direction the code sees, it moves 2{0}m along the x-direction. Generally, scale = beamspot-size in {0}m if x-scale = y-scale. Test and iterate to ensure.".format(self.MICROSYMBOL),
            "Print a non-symmetrical image (e.g. <a href='{}'>fliptest.bmp</a>) to test whether the horizontal and vertical needs to be flipped. <span style='color: red;'>NOTE:</span> Flipping flips the image first before parsing its lines! To flip after, use a negative number as the scale.".format(os.path.join(root_dir, '1_runs', 'fliptest', 'fliptest.bmp')),
            "The code will greedily search for the next pixel to the right of the current pixel to determine continuous lines. To prioritize searching the left pixel first, check 'Search left before right'."
        ]

        _DP_instructions_label.setText("<br/><br/>".join(_DP_instructions_string))
        _DP_instructions_label.setWordWrap(True)
        _DP_instructions_label.setTextFormat(QtCore.Qt.RichText)
        _DP_instructions_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        _DP_instructions_label.setOpenExternalLinks(True)

        _DP_instructions_scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        _DP_instructions_scrollArea.setWidget(_DP_instructions_label)
        _DP_instructions_scrollArea.setWidgetResizable(True)
        # https://www.oipapio.com/question-3065786

        # _DP_instructions_layout.addWidget(_DP_instructions_scrollArea)
        # _DP_instructions.setLayout(_DP_instructions_layout)
        # / INSTRUCTIONS

        # DRAW PIC INTERFACE
        _DP_main = QtWidgets.QGroupBox("Parameters")
        _DP_main_layout = QtWidgets.QGridLayout()

        # _DP_picture_fn_label = QtWidgets.QLabel("BMP File")
        # _DP_picture_fn_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._DP_picture_fn  = QtWidgets.QLineEdit()
        self._DP_picture_fn.setPlaceholderText("File name")
        self._DP_picture_btn = QtWidgets.QPushButton("Browse...")
        self._DP_picture_load = QtWidgets.QPushButton("Load")

        self._DP_picture_preview = QtWidgets.QLabel("<i>Preview Here</i>")
        self._DP_picture_preview.setStyleSheet("color: #777;")
        self._DP_picture_preview.setAlignment(QtCore.Qt.AlignCenter)

        # Options
        # def __init__(self, filename, xscale = 1, yscale = 1, cut = 0, allowDiagonals = False, prioritizeLeft = False, flipHorizontally = False, flipVertically = False ,frames = False, simulate = False, simulateDrawing = False, micronInstance = None, shutterTime = 800)
        _DP_options = QtWidgets.QWidget() # QGroupBox("Options")
        _DP_options_layout = QtWidgets.QGridLayout()

        _DP_xscale_label = QtWidgets.QLabel("X-Scale")
        _DP_xscale_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._DP_xscale = QtWidgets.QLineEdit("1")
        # self._DP_xscale.setValidator(QtGui.QDoubleValidator(0,10000, 12))
        self._DP_xscale.setValidator(QtGui.QDoubleValidator())
        self._DP_xscale.setToolTip("This is usually your beam spot size.")
        _DP_yscale_label = QtWidgets.QLabel("Y-Scale")
        _DP_yscale_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._DP_yscale = QtWidgets.QLineEdit("1")
        # self._DP_yscale.setValidator(QtGui.QDoubleValidator(0,10000, 12))
        self._DP_yscale.setValidator(QtGui.QDoubleValidator())
        self._DP_yscale.setToolTip("This is usually your beam spot size.")

        _DP_cutMode_label = QtWidgets.QLabel("Cut")
        _DP_cutMode_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._DP_cutMode = QtWidgets.QComboBox()
        self._DP_cutMode.addItem("Black")
        self._DP_cutMode.addItem("White")

        self._DP_allowDiagonals = QtWidgets.QCheckBox("Allow Diagonals")
        self._DP_flipVertically = QtWidgets.QCheckBox("Flip Vertically")
        self._DP_flipHorizontally = QtWidgets.QCheckBox("Flip Horizontally")

        self._DP_allowDiagonals.setChecked(True)
        self._DP_allowDiagonals.setToolTip("Diagonal pixels will also be considered adjacent\npixels when parsing the picture into lines.")
        self._DP_flipVertically.setToolTip("Use a simple image to test whether flipping is necessary.\nImage is flipped BEFORE parsing it.")
        self._DP_flipHorizontally.setToolTip("Use a simple image to test whether flipping is necessary.\nImage is flipped BEFORE parsing it.")

        self._DP_prioritizeLeft = QtWidgets.QCheckBox("Search left before right")
        self._DP_prioritizeLeft.setToolTip("Algorithm moves from right to left and searches for\na left pixel first before of the right pixel.")

        _DP_options_layout.addWidget(_DP_xscale_label          , 0, 0, 1, 1)
        _DP_options_layout.addWidget(self._DP_xscale           , 0, 1, 1, 1)
        _DP_options_layout.addWidget(_DP_yscale_label          , 1, 0, 1, 1)
        _DP_options_layout.addWidget(self._DP_yscale           , 1, 1, 1, 1)
        _DP_options_layout.addWidget(_DP_cutMode_label         , 2, 0, 1, 1)
        _DP_options_layout.addWidget(self._DP_cutMode          , 2, 1, 1, 1)
        _DP_options_layout.addWidget(self._DP_allowDiagonals   , 2, 2, 1, 1)
        _DP_options_layout.addWidget(self._DP_flipVertically   , 1, 2, 1, 1)
        _DP_options_layout.addWidget(self._DP_flipHorizontally , 0, 2, 1, 1)
        _DP_options_layout.addWidget(self._DP_prioritizeLeft   , 3, 0, 1, 3)


        _DP_options_layout.setColumnStretch(0, 1)
        _DP_options_layout.setColumnStretch(1, 2)
        _DP_options_layout.setColumnStretch(2, 1)

        _DP_options.setLayout(_DP_options_layout)
        # / Options

        self._DP_picture_parse = QtWidgets.QPushButton("Parse Picture")

        _DP_moveToZero = QtWidgets.QLabel('Move to (0, 0), usually top-left, of the image using "Stage Movement"')
        _DP_moveToZero.setWordWrap(True)

        _DP_velocity_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        _DP_velocity_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._DP_velocity = QtWidgets.QLineEdit("100")
        self._DP_velocity.setValidator(QtGui.QDoubleValidator(0,10000, 12))

        self._DP_picture_estimateTime = QtWidgets.QPushButton("Estimate Time")
        self._DP_picture_draw = QtWidgets.QPushButton("Draw")

        _DP_steps_labels = []
        for i in range(6):
            _temp_label = QtWidgets.QLabel("[{}]".format(i + 1))
            _temp_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            _temp_label.setStyleSheet("font-family: Menlo, Consolas, monospace;")
            _DP_steps_labels.append(_temp_label)

        _DP_main_layout.addWidget(_DP_steps_labels[0], 0, 0, 1, 1)
        # _DP_main_layout.addWidget(_DP_picture_fn_label, 1, 1, 1, 1)
        _DP_main_layout.addWidget(self._DP_picture_fn, 0, 1, 1, 3)
        _DP_main_layout.addWidget(self._DP_picture_btn, 0, 4, 1, 1)

        _DP_main_layout.addWidget(_DP_steps_labels[1], 1, 0, 1, 1)
        _DP_main_layout.addWidget(self._DP_picture_load, 1, 1, 1, 4)

        _DP_main_layout.addWidget(_DP_steps_labels[2], 2, 0, 1, 1)
        _DP_main_layout.addWidget(_DP_options, 2, 1, 1, 4)

        _DP_main_layout.addWidget(_DP_steps_labels[3], 3, 0, 1, 1)
        _DP_main_layout.addWidget(self._DP_picture_parse, 3, 1, 1, 4)

        _DP_main_layout.addWidget(_DP_steps_labels[4], 4, 0, 1, 1)
        _DP_main_layout.addWidget(_DP_moveToZero, 4, 1, 1, 4)

        _DP_main_layout.addWidget(_DP_steps_labels[5], 5, 0, 1, 1)
        _DP_main_layout.addWidget(_DP_velocity_label, 5, 1, 1, 1)
        _DP_main_layout.addWidget(self._DP_velocity, 5, 2, 1, 3)

        _DP_main_layout.addWidget(self._DP_picture_estimateTime, 6, 0, 1, 2)
        _DP_main_layout.addWidget(self._DP_picture_draw, 6, 2, 1, 3)

        _DP_main_layout.setColumnStretch(0, 1)
        for i in range(1, 4):
            _DP_main_layout.setColumnStretch(i, 2)

        _DP_main.setLayout(_DP_main_layout)
        # / DRAW PIC INTERFACE

        # _drawpic_layout.addWidget(_DP_instructions, 0, 0)
        _drawpic_layout.addWidget(self._DP_picture_preview, 0, 0, 1, 1)
        _drawpic_layout.addWidget(_DP_instructions_scrollArea, 1, 0, 1, 1)
        _drawpic_layout.addWidget(_DP_main, 0, 1, 2, 1)

        _drawpic_layout.setColumnStretch(0, 1)
        _drawpic_layout.setColumnStretch(1, 1)
        _drawpic_layout.setRowStretch(0, 1)
        _drawpic_layout.setRowStretch(1, 1)

        return _drawpic_layout

# INTERACTION FUNCTONS
    def initEventListeners(self):

        # STAGE
        self.UP, self.RIGHT, self.DOWN, self.LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)

        self.cardinalStageMoving = False
        self.lastCardinalStageMove = datetime.datetime.now()

        self._upArrow.clicked.connect(lambda: self.cardinalMoveStage(self.UP))
        self._downArrow.clicked.connect(lambda: self.cardinalMoveStage(self.DOWN))
        self._leftArrow.clicked.connect(lambda: self.cardinalMoveStage(self.LEFT))
        self._rightArrow.clicked.connect(lambda: self.cardinalMoveStage(self.RIGHT))
        self._homeBtn.clicked.connect(lambda: self.homeStage())
        self._SL_invertx_checkbox.stateChanged.connect(lambda: self.invertCheck())
        self._SL_inverty_checkbox.stateChanged.connect(lambda: self.invertCheck())
        self._SL_velocity.textChanged.connect(lambda: self.recalculateKeystrokeTimeout())
        self._SL_step_size.textChanged.connect(lambda: self.recalculateKeystrokeTimeout())

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

        # note that the following you cannot connect(self.checkSRValues) because the value will be passed in as an argument to self.checkSRValues

        # COMMON
        self.operationDone.connect(self.on_operationDone)
        self.EL_self_criticalDialog.connect(self.on_EL_self_criticalDialog)

        # SINGLE RASTER
        self._SR_velocity.textChanged.connect(lambda: self.checkSRValues())
        self._SR_size_x.textChanged.connect(lambda: self.checkSRValues())
        self._SR_size_y.textChanged.connect(lambda: self.checkSRValues())
        self._SR_step_size.textChanged.connect(lambda: self.checkSRValues())
        self._SR_raster_x.stateChanged.connect(lambda: self.checkSRValues())
        self._SR_raster_y.stateChanged.connect(lambda: self.checkSRValues())
        self._SR_retToOri.stateChanged.connect(lambda: self.checkSRValues())
        self._SR_start.clicked.connect(lambda: self.checkSRValues(startRaster = True))
        self._SR_pow_up.clicked.connect(lambda: self.adjustPower(direction = "+"))
        self._SR_pow_dn.clicked.connect(lambda: self.adjustPower(direction = "-"))
        self._SR_pow_step.textChanged.connect(lambda: self._SR_pow_step.setStyleSheet("background-color: none; color: #000;"))

        # ARRAY RASTER
        self._AR_init_velocity.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_init_power.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_X_mode.currentIndexChanged.connect(lambda: self.recalculateARValues())
        self._AR_cols.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_X_intervals.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_X_spacing.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_Y_mode.currentIndexChanged.connect(lambda: self.recalculateARValues())
        self._AR_rows.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_Y_intervals.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_Y_spacing.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_size_x.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_size_y.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_step_size.textChanged.connect(lambda: self.recalculateARValues())
        self._AR_raster_x.stateChanged.connect(lambda: self.recalculateARValues())
        self._AR_raster_y.stateChanged.connect(lambda: self.recalculateARValues())
        self._AR_retToOri.stateChanged.connect(lambda: self.recalculateARValues())
        self._AR_start.clicked.connect(lambda: self.recalculateARValues(startRaster = True))

        # DRAW PIC
        self._DP_picture_btn.clicked.connect(lambda: self._DP_getFile())
        self._DP_picture_load.clicked.connect(lambda: self._DP_loadPicture())
        self._DP_picture_parse.clicked.connect(lambda: self._DP_parsePicture())
        self._DP_picture_estimateTime.clicked.connect(lambda: self._DP_drawPicture(estimateOnly = True))
        self._DP_picture_draw.clicked.connect(lambda: self._DP_drawPicture())
        self._DP_xscale.textChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_yscale.textChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_cutMode.currentIndexChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_allowDiagonals.stateChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_flipVertically.stateChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_flipHorizontally.stateChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_prioritizeLeft.stateChanged.connect(lambda: self._DP_optionsChanged())
        self._DP_picture_fn.textChanged.connect(lambda: self._DP_filenameLineEditChanged())

        self.picConvWarn.connect(self.on_picConvWarn)


        # SHUTTER
        self._close_shutter.clicked.connect(lambda: self.stageControl.controller.shutter.close())
        self._open_shutter.clicked.connect(lambda: self.stageControl.controller.shutter.open())

        self._abortBtn.clicked.connect(lambda: threading.Thread(target = self.KeyboardInterruptHandler, kwargs = dict(abortTrigger = True)).start())

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

                # self.logconsole(self.lastCardinalStageMove)

                # now = datetime.datetime.now()
                # try:
                #     if now >= self.lastEvent + datetime.timedelta(seconds = 1):
                #         print(self.numEvents)
                #         self.numSeconds += 1
                #         self.lastEvent = now
                #         self.numEvents = 0
                # except Exception as e:
                #     self.lastEvent = now
                #     self.numSeconds = 0
                #     self.numEvents = 0
                #
                # self.numEvents += 1
                # ==> we deduce about 66 events / second

                # we try to block it as early and possible
                # WARNING: This still doesn't work as expected like in the previous VBA iteration of this

                if source == self.stage_widget and not self.cardinalStageMoving and datetime.datetime.now() > self.lastCardinalStageMove + datetime.timedelta(milliseconds = self.KEYSTROKE_TIMEOUT):

                    if evtkey == QtCore.Qt.Key_Up:
                        self.cardinalMoveStage(self.UP)

                    if evtkey == QtCore.Qt.Key_Down:
                        self.cardinalMoveStage(self.DOWN)

                    if evtkey == QtCore.Qt.Key_Left:
                        self.cardinalMoveStage(self.LEFT)

                    if evtkey == QtCore.Qt.Key_Right:
                        self.cardinalMoveStage(self.RIGHT)

        # TODO: Catching alert sound
        # if isintance(evt, QtGui.QAccessibleEvent)

        # return QtWidgets.QWidget.eventFilter(self, source, evt)
        return super(QtWidgets.QWidget, self).eventFilter(source, evt)

# Custom functions
# Stage Movement
    def homeStage(self):
        if not self.devMode:
            self.setOperationStatus("Homing stage...If any error arises, abort immediately with Ctrl + C")
            self.stageControl.controller.homeStage()
            self.setOperationStatus("Home stage finished")
        else:
            self.setOperationStatus("devMode, not homing...")

    def cardinalMoveStage(self, direction):
        # Get the distance
        dist = float(self._SL_step_size.text())
        vel  = float(self._SL_velocity.text())

        # Move the stage
        if not self.devMode:
            self.moveStage(direction, distance = dist, velocity = vel)

    def moveStage(self, direction, distance, velocity):
        # direction is a (dx, dy) tuple/vector that defines the direction that gets multiplied by distance
        if sum(map(abs, direction)) > 1:
            _mag = math.sqrt(direction[0]**2 + direction[1]**2)
            direction = (direction[0] / _mag , direction[1] / _mag)

        if not self.cardinalStageMoving:
            self.cardinalStageMoving = True

            if self.stageControl.controller.velocity != velocity:
                # We reset the velocity if it is different
                self.stageControl.controller.setvel(velocity)

            self.stageControl.controller.rmove(x = direction[0] * distance * self.stageControl.noinvertx, y = direction[1] * distance * self.stageControl.noinverty)
            self.updatePositionDisplay()

            self.lastCardinalStageMove = datetime.datetime.now()

            self.cardinalStageMoving = False

    def updatePositionDisplay(self):
        if self.stageControl is not None:
            # self.logconsole(self.stageControl.controller.stage.position)
            self._lcdx.display(self.stageControl.controller.stage.x)
            self._lcdy.display(self.stageControl.controller.stage.y)

    def invertCheck(self):
        self.stageControl.noinvertx = -1 if self._SL_invertx_checkbox.checkState() else 1
        self.stageControl.noinverty = -1 if self._SL_inverty_checkbox.checkState() else 1

        self.qsettings.setValue("stage/invertx", True) if self.stageControl.noinvertx == -1 else self.qsettings.setValue("stage/invertx", False)
        self.qsettings.setValue("stage/inverty", True) if self.stageControl.noinverty == -1 else self.qsettings.setValue("stage/inverty", False)
        self.qsettings.sync()

    def recalculateKeystrokeTimeout(self):
        try:
            vel = float(self._SL_velocity.text())
            dist = float(self._SL_step_size.text())
            estTime = self.stageControl.controller.getDeltaTime(x = dist, y = 0, velocity = vel)
            self.KEYSTROKE_TIMEOUT = estTime * 66 * 0.002 * 1000 # 66 events per second, 0.002 to process each event
            # i.e. to say how long to burn all the events
            # Issue is events gets queued, not the connected function

        except Exception as e:
            self.logconsole(e)
            self.KEYSTROKE_TIMEOUT = 10

# Common
    def setStartButtonsEnabled(self, state):
        self._SR_start.setEnabled(state)
        self._AR_start.setEnabled(state)
        self._DP_picture_draw.setEnabled(state)

    def winAudioSetMuted(self, state):
        if not hasattr(self, "pycaw_sess"):
            if platform.system() == "Windows":
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    if session.Process and session.Process.name() == "python.exe":
                        self.pycaw_sess = session
                        self.pycaw_vol = self.pycaw_sess._ctl.QueryInterface(ISimpleAudioVolume)
            else:
                self.pycaw_sess = None

        if self.pycaw_sess is None:
            return

        return self.pycaw_vol.SetMasterVolume(0, None) if state else self.pycaw_vol.SetMasterVolume(1, None)

# Single Raster
    def adjustPower(self, direction):
        try:
            assert direction == "+" or direction == "-", "Invalid Direction"
            _step = int(self._SR_pow_step.text())
        except ValueError as e:
            self._SR_pow_step.setStyleSheet("background-color: #DF2928; color: #fff;")
            return
        except AssertionError as e:
            self.logconsole("Invalid call to MicroGUI.adjustPower(direction = {})".format(direction))
            return

        self._SR_pow_step.setStyleSheet("background-color: none; color: #000;")

        self.setOperationStatus("Adjusting power...")
        self._SR_pow_up.setEnabled(False)
        self._SR_pow_dn.setEnabled(False)

        powerThread = ThreadWithExc(target = self._adjustPower, kwargs = dict(_step = _step, direction = direction))
        powerThread.start()

        # self._adjustPower()

    def _adjustPower(self, _step, direction):
        self.stageControl.controller.powerServo.powerstep(number = (-1 * _step) if direction == "-" else (_step))
        self._SR_pow_up.setEnabled(True)
        self._SR_pow_dn.setEnabled(True)
        self.setOperationStatus("Ready.")

    def checkSRValues(self, startRaster = False):
        _got_error = False
        try:
            # Recalculate the values for Array Raster
            _vel = float(self._SR_velocity.text())

            # we convert 2 to 1 since .checkState gives 0 = unchecked, 2 = checked
            step_along_x = not not self._SR_raster_x.checkState()
            step_along_y = not not self._SR_raster_y.checkState()

            step_size = float(self._SR_step_size.text())

            returnToOrigin = not not self._SR_retToOri.checkState()

            # sizes
            # y, x
            size = [float(self._SR_size_y.text()), float(self._SR_size_x.text())]

            # Recalculate size based on flooring calculations
            _lines = math.floor(abs(size[step_along_x] / step_size))
            size[step_along_x] = _lines * step_size

            # Indivdual Raster Type
            indiv_type = "square" if size[0] == size[1] else "rectangle"

            # catch all errors:
            _got_error = (size[1] <= 0 or size[0] <= 0 or _vel <= 0)

            self._SR_size_x.setStyleSheet("background-color: #DF2928; color: #fff;") if size[1] <= 0 else self._SR_size_x.setStyleSheet("background-color: none; color: #000;")
            self._SR_size_y.setStyleSheet("background-color: #DF2928; color: #fff;") if size[0] <= 0 else self._SR_size_y.setStyleSheet("background-color: none; color: #000;")

            # If power, ensure changes are integer

            # RASTER SETTINGS
            self._SR_raster_style.setStyleSheet("background-color: none; color: #000;")
            if step_along_x and step_along_y:
                self._SR_raster_style.setText("Unfilled {}\nDrawing an outline".format(indiv_type))
                self._SR_step_size.setReadOnly(True)
                self._SR_step_size.setStyleSheet("background-color: #ccc; color: #555;")
            elif step_along_x:
                self._SR_raster_style.setText("Filled {}\nContinuous along x-axis".format(indiv_type))
                self._SR_step_size.setReadOnly(False)
                self._SR_step_size.setStyleSheet("background-color: none; color: #000;")
            elif step_along_y:
                self._SR_raster_style.setText("Filled {}\nContinuous along y-axis".format(indiv_type))
                self._SR_step_size.setReadOnly(False)
                self._SR_step_size.setStyleSheet("background-color: none; color: #000;")
            else:
                _got_error = True
                self._SR_raster_style.setText("No axis selected\nChoose at least one axis")
                self._SR_raster_style.setStyleSheet("background-color: #DF2928; color: #fff;")
                self._SR_step_size.setReadOnly(False)
                self._SR_step_size.setStyleSheet("background-color: none; color: #000;")

        except Exception as e:
            # We assume the user is not done entering the data
            self.logconsole("{}: {}".format(type(e).__name__, e))
            self._SR_size_x.setStyleSheet("background-color: none; color: #000;")
            self._SR_size_y.setStyleSheet("background-color: none; color: #000;")

            self._SR_raster_style.setText("-\n")
            self._SR_raster_style.setStyleSheet("background-color: none; color: #000;")

        # Check if the values are even valid
        # Change background if necessary
        else:
            # There are no errors, and we check if startRaster
            if startRaster and not _got_error:
                # JUMP TO DEF
                # def singleraster(self, velocity, xDist, yDist, rasterSettings, returnToOrigin = False, estimateTime = True, onlyEstimate = False):

                # Raster in a rectangle
        		# rasterSettings = {
        		# 	"direction": "x" || "y" || "xy", 		# Order matters here xy vs yx
        		# 	"step": 1								# If set to xy, step is not necessary
        		# }
                if not step_along_x and not step_along_y:
                    self.setOperationStatus("Step-axis not selected!")
                    return

                rsSettingsDir = ""
                rsSettingsDir += "x" if step_along_x else ""
                rsSettingsDir += "y" if step_along_y else ""

                if step_along_x and step_along_y:
                    rsSettings = { "direction" : rsSettingsDir }
                else:
                    rsSettings = { "direction" : rsSettingsDir, "step": step_size }

                self.setOperationStatus("Starting Single Raster...")

                self.setStartButtonsEnabled(False)
                self.setOperationStatus("Starting Single Raster...")
                sr_thread = ThreadWithExc(target = self._singleRaster, kwargs = dict(
                    velocity       = _vel,
                    xDist          = size[1],
                    yDist          = size[0],
                    rasterSettings = rsSettings,
                    returnToOrigin = returnToOrigin
                ))
                sr_thread.start()

            elif startRaster:
                # Alert got error
                self.criticalDialog(message = "Error in single raster settings.\nPlease check again!", host = self)

    def _singleRaster(self, **kwargs):
        try:
            self.stageControl.singleraster(**kwargs)
        except Exception as e:
            self.setOperationStatus("Error Occurred. {}".format(e))
            if self.devMode:
                raise
        else:
            # If no error
            self.setOperationStatus("Ready.")
        finally:
            # Always run
            self.setStartButtonsEnabled(True)

# Array Raster
    def recalculateARValues(self, startRaster = False):
        _got_error = False
        try:
            # Recalculate the values for Array Raster
            vel_0 = float(self._AR_init_velocity.text())
            pow_0 = int(self._AR_init_power.text())

            # we convert 2 to 1 since .checkState gives 0 = unchecked, 2 = checked
            step_along_x = not not self._AR_raster_x.checkState()
            step_along_y = not not self._AR_raster_y.checkState()

            step_size = float(self._AR_step_size.text())

            # 0 = Velocity, 1 = Power
            x_isPow = self._AR_X_mode.currentIndex()
            x_incr = float(self._AR_X_intervals.text())
            x_cols = int(self._AR_cols.text())
            x_spac = float(self._AR_X_spacing.text())

            y_isPow = self._AR_Y_mode.currentIndex()
            y_incr = float(self._AR_Y_intervals.text())
            y_rows = int(self._AR_rows.text())
            y_spac = float(self._AR_Y_spacing.text())

            returnToOrigin = not not self._AR_retToOri.checkState()

            # sizes
            # y, x
            size = [float(self._AR_size_y.text()), float(self._AR_size_x.text())]

            # Recalculate size based on flooring calculations
            _lines = math.floor(abs(size[step_along_x] / step_size))
            size[step_along_x] = _lines * step_size

            # Horizontal
            vel_x_f = vel_0 + (x_cols - 1) * x_incr if not x_isPow else vel_0
            pow_x_f = pow_0 + (x_cols - 1) * x_incr if x_isPow else pow_0
            # Vertical
            vel_y_f = vel_0 + (y_rows - 1) * y_incr if not y_isPow else vel_0
            pow_y_f = pow_0 + (y_rows - 1) * y_incr if y_isPow else pow_0

            # Final
            vel_xy_f = vel_x_f + vel_y_f - vel_0
            pow_xy_f = pow_x_f + pow_y_f - pow_0

            # Total Raster Area
            tt_x = x_cols * size[1] + (x_cols - 1) * x_spac
            tt_y = y_rows * size[0] + (y_rows - 1) * y_spac

            # Indivdual Raster Type
            indiv_type = "square" if size[0] == size[1] else "rectangle"

            # catch all errors:
            _got_error = (x_cols <= 0 or y_rows <= 0 or size[1] <= 0 or size[0] <= 0 or vel_x_f < 0 or vel_y_f < 0 or vel_xy_f < 0)

            self._AR_cols.setStyleSheet("background-color: #DF2928; color: #fff;") if x_cols <= 0 else self._AR_cols.setStyleSheet("background-color: none; color: #000;")
            self._AR_rows.setStyleSheet("background-color: #DF2928; color: #fff;") if y_rows <= 0 else self._AR_rows.setStyleSheet("background-color: none; color: #000;")

            self._AR_size_x.setStyleSheet("background-color: #DF2928; color: #fff;") if size[1] <= 0 else self._AR_size_x.setStyleSheet("background-color: none; color: #000;")
            self._AR_size_y.setStyleSheet("background-color: #DF2928; color: #fff;") if size[0] <= 0 else self._AR_size_y.setStyleSheet("background-color: none; color: #000;")

            self._AR_X_final_settings.setStyleSheet("background-color: #DF2928; color: #fff;") if vel_x_f < 0 else self._AR_X_final_settings.setStyleSheet("background-color: none; color: #000;")
            self._AR_Y_final_settings.setStyleSheet("background-color: #DF2928; color: #fff;") if vel_y_f < 0 else self._AR_Y_final_settings.setStyleSheet("background-color: none; color: #000;")
            self._AR_XY_final_settings.setStyleSheet("background-color: #DF2928; color: #fff;") if vel_xy_f < 0 else self._AR_XY_final_settings.setStyleSheet("background-color: none; color: #000;")

            self._AR_summary_text.setText("Rastering a {} x {} array\nEach {} {} x {} {}m\nRaster Area = {} x {} {}m".format(y_rows, x_cols, indiv_type, *size, self.MICROSYMBOL, tt_y, tt_x, self.MICROSYMBOL))

            self._AR_X_final_velocity.setText(str(vel_x_f))
            self._AR_Y_final_velocity.setText(str(vel_y_f))
            self._AR_XY_final_velocity.setText(str(vel_xy_f))

            self._AR_X_final_power.setText(str(pow_x_f))
            self._AR_Y_final_power.setText(str(pow_y_f))
            self._AR_XY_final_power.setText(str(pow_xy_f))

            # If power, ensure changes are integer
            if x_isPow and not (x_incr.is_integer()):
                # x_power error
                _got_error = True
                self._AR_X_intervals.setStyleSheet("background-color: #DF2928; color: #fff;")
                self._AR_X_final_power.setText("<b style='color: red'>INT!<b>")
                self._AR_XY_final_power.setText("<b style='color: red'>INT!<b>")
            else:
                self._AR_X_intervals.setStyleSheet("background-color: none; color: #000;")

            if y_isPow and not (y_incr.is_integer()):
                # y_power error
                _got_error = True
                self._AR_Y_intervals.setStyleSheet("background-color: #DF2928; color: #fff;")
                self._AR_Y_final_power.setText("<b style='color: red'>INT!<b>")
                self._AR_XY_final_power.setText("<b style='color: red'>INT!<b>")
            else:
                self._AR_Y_intervals.setStyleSheet("background-color: none; color: #000;")

            # RASTER SETTINGS
            self._AR_raster_style.setStyleSheet("background-color: none; color: #000;")
            if step_along_x and step_along_y:
                self._AR_raster_style.setText("Unfilled {}\nDrawing an outline".format(indiv_type))
                self._AR_step_size.setReadOnly(True)
                self._AR_step_size.setStyleSheet("background-color: #ccc; color: #555;")
            elif step_along_x:
                self._AR_raster_style.setText("Filled {}\nContinuous along x-axis".format(indiv_type))
                self._AR_step_size.setReadOnly(False)
                self._AR_step_size.setStyleSheet("background-color: none; color: #000;")
            elif step_along_y:
                self._AR_raster_style.setText("Filled {}\nContinuous along y-axis".format(indiv_type))
                self._AR_step_size.setReadOnly(False)
                self._AR_step_size.setStyleSheet("background-color: none; color: #000;")
            else:
                _got_error = True
                self._AR_raster_style.setText("No axis selected\nChoose at least one axis")
                self._AR_raster_style.setStyleSheet("background-color: #DF2928; color: #fff;")
                self._AR_step_size.setReadOnly(False)
                self._AR_step_size.setStyleSheet("background-color: none; color: #000;")

        except Exception as e:
            # We assume the user is not done entering the data
            self.logconsole("{}: {}".format(type(e).__name__, e))
            self._AR_Y_final_settings.setStyleSheet("background-color: none; color: #000;")
            self._AR_Y_final_settings.setStyleSheet("background-color: none; color: #000;")
            self._AR_XY_final_settings.setStyleSheet("background-color: none; color: #000;")

            self._AR_rows.setStyleSheet("background-color: none; color: #000;")
            self._AR_rows.setStyleSheet("background-color: none; color: #000;")
            self._AR_size_x.setStyleSheet("background-color: none; color: #000;")
            self._AR_size_y.setStyleSheet("background-color: none; color: #000;")

            self._AR_summary_text.setText("-")

            self._AR_raster_style.setText("-\n")
            self._AR_raster_style.setStyleSheet("background-color: none; color: #000;")

            self._AR_X_final_velocity.setText("-")
            self._AR_Y_final_velocity.setText("-")
            self._AR_XY_final_velocity.setText("-")

            self._AR_X_final_power.setText("-")
            self._AR_Y_final_power.setText("-")
            self._AR_XY_final_power.setText("-")

        # Check if the values are even valid
        # Change background if necessary
        else:
            # There are no errors, and we check if startRaster
            if startRaster and not _got_error:
                # JUMP TO DEF
                # def arrayraster(self, inivel, inipower, x_isVel, ncols, xincrement, xGap, y_isVel, nrows, yincrement, ygap, xDist, yDist, rasterSettings, returnToOrigin = True):

                # Raster in a rectangle
        		# rasterSettings = {
        		# 	"direction": "x" || "y" || "xy", 		# Order matters here xy vs yx
        		# 	"step": 1								# If set to xy, step is not necessary
        		# }
                if not step_along_x and not step_along_y:
                    self.setOperationStatus("Step-axis not selected!")
                    return

                rsSettingsDir = ""
                rsSettingsDir += "x" if step_along_x else ""
                rsSettingsDir += "y" if step_along_y else ""

                if step_along_x and step_along_y:
                    rsSettings = { "direction" : rsSettingsDir }
                else:
                    rsSettings = { "direction" : rsSettingsDir, "step": step_size }

                self.setStartButtonsEnabled(False)
                self.setOperationStatus("Starting Array Raster...")
                ar_thread = ThreadWithExc(target = self._arrayraster, kwargs = dict(
                    xDist      = size[1],         yDist      = size[0],
                    xGap       = x_spac,          yGap       = y_spac,
                    nrows      = y_rows,          ncols      = x_cols,
                    inivel     = vel_0,           inipower   = pow_0,
                    x_isVel    = x_isPow ^ 1,     y_isVel    = y_isPow ^ 1,
                    xincrement = x_incr,          yincrement = y_incr,
                    rasterSettings = rsSettings,
                    returnToOrigin = returnToOrigin
                ))
                ar_thread.start()

            elif startRaster:
                # Alert got error
                self.criticalDialog(message = "Error in array raster settings.\nPlease check again!", host = self)

    def _arrayraster(self, **kwargs):
        try:
            self.stageControl.arrayraster(**kwargs)
        except Exception as e:
            self.setOperationStatus("Error Occurred. {}".format(e))
            if self.devMode:
                raise
        else:
            self.setOperationStatus("Ready.")
        finally:
            self.setStartButtonsEnabled(True)

# Draw Picture
    def _DP_getFile(self):
        # THIS IS PURELY FOR GUI CHOOSE FILE

        # Attempt to get filename from QLineEdit
        filename = self._DP_picture_fn.text()
        if os.path.isfile(filename):
            filename = os.path.abspath(os.path.realpath(os.path.expanduser(filename)))
            dirname  = os.path.dirname(filename)
        else:
            dirname  = base_dir # base_dir of this file

        self._DP_FileDialog = QtWidgets.QFileDialog(self, "Open Image", dirname, "1-Bit Bitmap Files (*.bmp)")
        self._DP_FileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self._DP_FileDialog.setViewMode(QtWidgets.QFileDialog.Detail)

        firstRun = True
        isValid  = False
        error    = None

        while not os.path.isfile(filename) or not isValid:
            if not firstRun:
                self.criticalDialog(message = "You have selected an invalid file", informativeText = "E: {}".format(error), title = "Invalid File", host = self)

            firstRun = False

            if (self._DP_FileDialog.exec_()):
                filename = self._DP_FileDialog.selectedFiles()[0]
                filename = os.path.abspath(os.path.realpath(os.path.expanduser(filename)))
                # Running this before loadPicture is so that windows gives the same file path url
            else:
                return
            # else (i.e. the user cancelled) we just ignore and act as though nothing happened

            # We run some checks here
            try:
                isValid = self._DP_runChecks(filename)
            except picConv.ImageError as e:
                isValid = False
                error = e

        if isValid:
            self._DP_picture_fn.setText(filename)

    def _DP_runChecks(self, filename):
        # Checks if the file exists and is valid
        # Raises picConv.ImageError if there are any errors

        if not os.path.isfile(filename):
            raise picConv.ImageError("Path is not file!")

        try:
            image = PILImage.open(filename)
        except Exception as e:
            raise picConv.ImageError("({}): {}".format(type(e).__name__, e))

        if image.format != "BMP":
            raise picConv.ImageError("The selected image is not a valid .bmp file!")

        if image.mode != '1':
            raise picConv.ImageError("Your image has mode {}. Please use a 1-bit indexed (mode 1) image, see <a href='https://pillow.readthedocs.io/en/stable/handbook/concepts.html#bands'>https://pillow.readthedocs.io/en/stable/handbook/concepts.html#bands</a>. If using GIMP to convert picture to 1-bit index, ensure 'remove colour from palette' is unchecked. ".format(image.mode))

        # Check size purely based on image and stage size
        # Does not take into account the scaling factor yet

        xlim = self.stageControl.controller.stage.xlim
        ylim = self.stageControl.controller.stage.ylim

        if image.size[0] > abs(xlim[1] - xlim[0]) or image.size[1] > abs(ylim[1] - ylim[0]):
            raise picConv.ImageError("Image way too big ._., exceeds stage limits")

        return True

    def _DP_loadPictureIntoPreviewer(self, filename):
        self._DP_picture_preview_pic = QtGui.QPixmap()
        if self._DP_picture_preview_pic.load(filename):
            self._DP_picture_preview_pic = self._DP_picture_preview_pic.scaled(self._DP_picture_preview.size(), QtCore.Qt.KeepAspectRatio)
            self._DP_picture_preview.setPixmap(self._DP_picture_preview_pic)
            return DoneObject()
        else:
            return self.criticalDialog(message = "Unable to load the selected file into preview", title = "Unable to load file", host = self)

    def _DP_loadPicture(self):
        # run tests again
        filename = self._DP_picture_fn.text()

        try:
            filename = os.path.abspath(os.path.realpath(os.path.expanduser(filename)))
            isValid = self._DP_runChecks(filename)
        except picConv.ImageError as e:
            return self.criticalDialog(message = "You have selected an invalid file", informativeText = "E: {}".format(e), title = "Invalid File", host = self)

        # Load picture into previewer
        x = self._DP_loadPictureIntoPreviewer(filename)
        if isinstance(x, DoneObject):
            # save the filename if everything passes
            self._DP_filename_string = filename
            self._DP_optionsChanged()

    def _DP_filenameLineEditChanged(self):
        self._DP_picture_load.setStyleSheet("background-color: #FF8800;")

    def _DP_optionsChanged(self):
        if hasattr(self, "_DP_filename_string"):
            self._DP_optionsChangedFlag = True
            self._DP_picture_load.setStyleSheet("")
            self._DP_picture_parse.setStyleSheet("background-color: #FF8800;")

    def _DP_parsePicture(self):
        # _DP_loadPicture has to be run first to do sanity checks
        if not hasattr(self, "_DP_filename_string") or self._DP_filename_string is None or not len(self._DP_filename_string):
            return self.criticalDialog(message = "Image not loaded!", informativeText = "Please load the image first before parsing. Filename not captured", title = "Image not loaded!", host = self)

        # Differs from Line edit, prompt to let user know
        lefn =  self._DP_picture_fn.text()
        if self._DP_filename_string != lefn:
            ret = self.unsavedQuestionDialog(message = "Load new filenames?", title = "Differing filenames",informativeText = "Registered filename differs from the input filename:\n\nREG:{}\nENT:{}\n\nSave to proceed.\nDiscard/Cancel to go back".format(self._DP_filename_string, lefn), host = self)

            if ret == QtWidgets.QMessageBox.Save:
                self._DP_loadPicture()
            else:
                return

        # Change colour of the Parse button
        self._DP_picture_parse.setStyleSheet("")

        # Get Options
        try:
            xscale = float(self._DP_xscale.text())
            yscale = float(self._DP_yscale.text())
            cutMode = self._DP_cutMode.currentIndex()
            allowDiagonals = not not self._DP_allowDiagonals.checkState()
            flipVertically = not not self._DP_flipVertically.checkState()
            flipHorizontally = not not self._DP_flipHorizontally.checkState()
            prioritizeLeft = not not self._DP_prioritizeLeft.checkState()
        except Exception as e:
            return self.criticalDialog(message = "Invalid values", informativeText = "Please double check your parameters.", host = self)


        # TODO: create the picConv object
        #    def __init__(self, filename, xscale = 1, yscale = 1, cut = 0, allowDiagonals = False, prioritizeLeft = False, flipHorizontally = False, flipVertically = False ,frames = False, simulate = False, simulateDrawing = False, micronInstance = None, shutterTime = 800):
        self.picConv = picConv.PicConv(
            filename = self._DP_filename_string,
            xscale = xscale,
            yscale = yscale,
            cut = cutMode,
            allowDiagonals = allowDiagonals,
            prioritizeLeft = prioritizeLeft,
            flipHorizontally = flipHorizontally,
            flipVertically = flipVertically,
            shutterTime = self.stageControl.controller.shutter.duration * 2,
            micronInstance = self.stageControl.controller,
            GUI_Object = self
        )
        # def progressDialog(self, host = None, title = "Progress", labelText = None, cancelButtonText = "Cancel", range = (0, 100)):
        # Should be regenerated every time
        if hasattr(self, "pDialog"):
            del self.pDialog

        self.pDialog = self.progressDialog(
            host = self,
            title = "PicConv",
            labelText = "Converting Picture",
        )
        self.picConv_conversion_thread = ThreadWithExc(target = self._DP_ConvertParseLines)
        self.picConv_conversion_thread.start()
        self.pDialog.exec_()

        if hasattr(self, "pDialog"):
            del self.pDialog

    def _DP_ConvertParseLines(self):
        def cancelOperation(self):
            return self.pDialog.close() if hasattr(self, "pDialog") else None

        self.pDialog.canceled.connect(lambda: cancelOperation(self))
        self.pDialog.setValue(0)

        # Redirect output through pDialog.setLabelText()
        try:
            self.picConv.convert()
        except Exception as e:
            # The error should have been emitted already
            self.logconsole("{}: {}".format(type(e).__name__, e))
            return cancelOperation(self)

        # Show test.png
        try:
            self._DP_loadPictureIntoPreviewer("picconv_test.png")
        except Exception as e:
            self.logconsole("{}: {}".format(type(e).__name__, e))

        while datetime.datetime.now() < self.lastPDialogUpdate + datetime.timedelta(seconds = self.PDIALOG_TIMEOUT):
            time.sleep(self.PDIALOG_TIMEOUT)
        self.pDialog.setWindowTitle("Parsing Lines")
        self.pDialog_setLabelText("Parsing Lines")

        try:
            self.picConv.parseLines()
        except Exception as e:
            # The error should have been emitted already
            self.logconsole("{}: {}".format(type(e).__name__, e))
            return cancelOperation(self)

        # Change Colour of Draw
        self._DP_picture_draw.setStyleSheet("background-color: #FF8800;")
        self._DP_optionsChangedFlag = False

        return self.pDialog.close() if hasattr(self, "pDialog") else None

    def _DP_drawPicture(self, estimateOnly = False):
        # Check if loaded
        if not hasattr(self, "_DP_filename_string") or self._DP_filename_string is None or not len(self._DP_filename_string):
            return self.criticalDialog(message = "Image not loaded!", informativeText = "Please load the image first before parsing and drawing. Filename not captured", title = "Image not loaded!", host = self)

        # Check if parseded
        if not hasattr(self, "picConv") or not isinstance(self.picConv, picConv.PicConv):
            return self.criticalDialog(message = "Image not parsed!", informativeText = "Please parse the image first before drawing. Image and options not captured.", title = "Image not parsed!", host = self)

        # Check if options changed
        if self._DP_optionsChangedFlag:
            ret = self.unsavedQuestionDialog(message = "Reparse with changed options?", title = "Options Changed",informativeText = "The parsing options have been changed since the last parse.\n\nSave to reparse with new options\nDiscard/Cancel to go back", host = self)

            if ret == QtWidgets.QMessageBox.Save:
                self._DP_parsePicture()
            else:
                return

        # Check if enough space
        if not estimateOnly:
            size = self.picConv.image.size # (width, height)
            fx = self.stageControl.controller.stage.x + self.picConv.scale["x"] * size[0]
            fy = self.stageControl.controller.stage.y + self.picConv.scale["y"] * size[1]

            xlim = sorted(self.stageControl.controller.stage.xlim)
            ylim = sorted(self.stageControl.controller.stage.ylim)

            xcond = xlim[0] <= fx <= xlim[1]
            ycond = ylim[0] <= fy <= ylim[1]

            if not xcond and not ycond:
                return self.criticalDialog(message = "Image too large!", informativeText = "At the current position, printing the picture will exceed stage limits in both the x and y direction\n\nStage Limits = x[{}, {}], y[{}, {}]\nImage Size = ({}, {})\nCurrent Stage Position = ({}, {})".format(*xlim, *ylim, *size, *self.stageControl.controller.stage.position), title = "Image too large!", host = self)
            elif not xcond:
                return self.criticalDialog(message = "Image too large!", informativeText = "At the current position, printing the picture will exceed stage limits in the x direction\n\nStage Limits = x[{}, {}]\nImage Size = ({}, {})\nCurrent Stage Position = ({}, {})".format(*xlim, *size, *self.stageControl.controller.stage.position), title = "Image too large!", host = self)
            elif not ycond:
                return self.criticalDialog(message = "Image too large!", informativeText = "At the current position, printing the picture will exceed stage limits in the y direction\n\nStage Limits = y[{}, {}]\nImage Size = ({}, {})\nCurrent Stage Position = ({}, {})".format(*ylim, *size, *self.stageControl.controller.stage.position), title = "Image too large!", host = self)
        # / Check space

        # Check the velocity
        vel = self._DP_velocity.text()
        try:
            vel = float(vel)
        except Exception as e:
            return self.criticalDialog(message = "Input Error", informativeText = "Unable to parse velocity into float. (Got {})".format(vel), title = "Input Error", host = self)

        if not estimateOnly:
            # alert confirm user has moved to (0,0)
            # We don't bother if the user changed the filename without loading, we just let them know what image will be drawn.
            ret = self.unsavedQuestionDialog(message = "Start drawing?", title = "Draw Picture",informativeText = "Using {}\n\nThis point has been taken as the (0, 0) of the image. This usually the top left.\n\nDraw to proceed.\nCancel to go back and change stage position.".format(self._DP_filename_string), host = self, buttons = {
                QtWidgets.QMessageBox.Save : "Draw"
            }, noDiscard = True)
            if ret != QtWidgets.QMessageBox.Save:
                return

            # Here we start to draw
            self.setStartButtonsEnabled(False)
            self._DP_picture_draw.setStyleSheet("")
            self.setOperationStatus("Starting Draw Picture...")
            q = ThreadWithExc(target = self._picConv_draw, args=(vel,))
            q.start()
        else:
            td = datetime.timedelta(seconds = self.picConv.estimateTime(velocity = vel))
            return self.informationDialog(message = "The picture will take approximately {}.".format(td), title = "Estimated Time", host = self)

    def _picConv_draw(self, velocity):
        try:
            # Errors are supposed to be emitted directly
            self.stageControl.controller.shutter.quietLog = True
            self.picConv.draw(velocity = velocity)
            self.stageControl.controller.shutter.quietLog = False
            self.stageControl.finishTone()
        except Exception as e:
            self.setOperationStatus("Error Occurred. {}".format(e))
            if self.devMode:
                raise
        else:
            # If no error
            self.setOperationStatus("Ready.")
        finally:
            # Always run
            self.setStartButtonsEnabled(True)

    PDIALOG_TIMEOUT = 1       # in seconds
    def pDialog_setValue(self, val):
        # print("SETTING VALUE:         ", val)
        if val == 100 or val == 50 or val == 0 or datetime.datetime.now() > self.lastPDialogUpdate + datetime.timedelta(seconds = self.PDIALOG_TIMEOUT):
            self.lastPDialogUpdate = datetime.datetime.now()
            self.pDialog.setValue(val)
        elif val == 100:
            time.sleep(PDIALOG_TIMEOUT)
            self.pDialog_setValue(val)

    def pDialog_setLabelText(self, text):
        if datetime.datetime.now() > self.lastPDialogUpdate + datetime.timedelta(seconds = self.PDIALOG_TIMEOUT):
            self.lastPDialogUpdate = datetime.datetime.now()
            self.pDialog.setLabelText(text)

# Helper functions
    def setOperationStatus(self, status, printToTerm = True, **printArgs):
        self.currentStatus = status
        if printToTerm:
            print("[{}]".format(datetime.datetime.now().time()), status, **printArgs)
        # Do some updating of the status bar
        self._statusbar_label.setText(status)

    def logconsole(self, status):
        print("[{}]".format(datetime.datetime.now().time()), status)

    EL_self_criticalDialog = QtCore.pyqtSignal('QString', 'QString', 'QString', 'bool')
    def on_EL_self_criticalDialog(self, message, title = "Oh no!", informativeText = None, exitAfter = False):
        ret = self.criticalDialog(message = message, title = title, informativeText = informativeText, host = self)

        if exitAfter:
            return os._exit(1)             # For the exit to propagate upwards
        else:
            return ret

    def criticalDialog(self, message, title = "Oh no!", informativeText = None, host = None):
        _msgBox = QtWidgets.QMessageBox(host)
        _msgBox.setIcon(QtWidgets.QMessageBox.Critical)
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

        _msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.winAudioSetMuted(True)
        ret = _msgBox.exec_()
        self.winAudioSetMuted(False)

        return ret

    def informationDialog(self, message, title = "Information", informativeText = None, host = None):
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

        self.winAudioSetMuted(True)
        ret = _msgBox.exec_()
        self.winAudioSetMuted(False)

        return ret

    def unsavedQuestionDialog(self, message, title = "Unsaved", informativeText = None, host = None, buttons = {}, noDiscard = False):
        _msgBox = QtWidgets.QMessageBox(host)
        _msgBox.setIcon(QtWidgets.QMessageBox.Question)
        _msgBox.setWindowTitle(title)
        _msgBox.setText(message)
        if informativeText is not None:
            _msgBox.setInformativeText(informativeText)

        if not noDiscard:
            _msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        else:
            _msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel)
        _msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)

        if buttons and isinstance(buttons, dict):
            for key, val in buttons.items():
                _msgBox.button(key).setText(val)

        # Get height and width
        _h = _msgBox.height()
        _w = _msgBox.width()
        _msgBox.setGeometry(0, 0, _w, _h)

        moveToCentre(_msgBox)

        # mb.setTextFormat(Qt.RichText)
        # mb.setDetailedText(message)

        # _msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.winAudioSetMuted(True)
        ret = _msgBox.exec_()
        self.winAudioSetMuted(False)

        return ret

    # https://doc.qt.io/qt-5/qprogressdialog.html
    def progressDialog(self, host = None, title = "Progress", labelText = None, cancelButtonText = "Cancel", range = (0, 100)):
        # QProgressDialog::QProgressDialog(const QString &labelText, const QString &cancelButtonText, int minimum, int maximum, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())
        # NOTE: DOES NOT EXEC
        pDialog = QtWidgets.QProgressDialog(labelText, cancelButtonText, range[0], range[1], host)

        pDialog.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.CustomizeWindowHint)

        pDialog.setWindowTitle(title)
        pDialog.setWindowModality(QtCore.Qt.WindowModal)

        # Get height and width
        _h = pDialog.height()
        _w = pDialog.width()
        pDialog.setGeometry(0, 0, _w, _h)

        moveToCentre(pDialog)

        self.lastPDialogUpdate = datetime.datetime.now()

        return pDialog

    operationDone = QtCore.pyqtSignal()
    def on_operationDone(self):
        self.informationDialog(message = "Operation Completed!", title = "Done!", host = self)

        if self.stageControl.musicProcess and self.stageControl.musicProcess.isAlive():
            try:
                self.stageControl.musicProcess.terminate()
            except Exception as e:
                self.logconsole("{}: {}".format(type(e).__name__, e))

    picConvWarn = QtCore.pyqtSignal('QString', 'QString')
    # [str, str]
    def on_picConvWarn(self, message, error):
        return self.criticalDialog(message = message, title = "PicConv Error!", informativeText = error, host = self)

# Status Bar

class aboutPopUp(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initUI()

    def initUI(self):
        # x, y, w, h
        self.setGeometry(0, 0, 250, 200)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # WidgetAttribute.
        self.setWindowTitle("About")
        moveToCentre(self)

        self._main_layout = QtWidgets.QVBoxLayout()
        # setContentsMargins(left, top, right, bottom)
        self._main_layout.setContentsMargins(10, 10, 10, 10)

        one = QtWidgets.QLabel("Made by")
        one.setAlignment(QtCore.Qt.AlignCenter)
        two = QtWidgets.QLabel("Sun Yudong, Wu Mingsong\n2019")
        two.setAlignment(QtCore.Qt.AlignCenter)
        ema = QtWidgets.QLabel()

        dianyous = [
            ["sunyudong", "outlook.sg"],
            ["mingsongwu", "outlook.sg"]
        ]

        ema.setText("<a href=\"mailto:{}\" title=\"Please don't spam us thanks\">sunyudong [at] outlook [dot] sg</a><br/><a href=\"mailto:{}\" title=\"Please don't spam us thanks\">mingsongwu [at] outlook [dot] sg</a>".format(*map("@".join, dianyous)))
        ema.setTextFormat(QtCore.Qt.RichText)
        ema.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        ema.setOpenExternalLinks(True)
        ema.setAlignment(QtCore.Qt.AlignCenter)

        thr = QtWidgets.QLabel("NUS Nanomaterials Lab")
        thr.setAlignment(QtCore.Qt.AlignCenter)

        self._main_layout.addWidget(one)
        self._main_layout.addWidget(two)
        self._main_layout.addWidget(ema)
        self._main_layout.addWidget(thr)

        self.setLayout(self._main_layout)

class SettingsScreen(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.microGUIParent = self.parentWidget()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        # x, y ,w, h
        self.setGeometry(0, 0, 500, 300)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        moveToCentre(self)

        self.makeUI()
        self.loadSettings()
        self.initEventListeners()

    def makeUI(self):
        self._main_layout = QtWidgets.QGridLayout()

        # Optomechanical
        _servos = QtWidgets.QGroupBox("Optomechanical")
        _servos_layout = QtWidgets.QGridLayout()

        self._shutterAbsoluteMode  = QtWidgets.QCheckBox("Use Absolute Mode for Shutter")
        self._powerAbsoluteMode    = QtWidgets.QCheckBox("Use Absolute Mode for Power")
        _shutterChannel_label_main = QtWidgets.QLabel("Shutter Channel")
        _shutterChannel_label_left = QtWidgets.QLabel("Left")
        _shutterChannel_label_righ = QtWidgets.QLabel("Right")
        _shutterChannel_label_main.setAlignment(QtCore.Qt.AlignTop)
        _shutterChannel_label_left.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        _shutterChannel_label_righ.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._shutterChannel       = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._shutterChannel.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self._shutterChannel.setRange(0, 1)
        self._shutterChannel.setSingleStep(1)
        self._shutterChannel.setPageStep(1)
        self._shutterChannel.setTickInterval(1)
        # WE USE THIS WORKAROUND OF SETTING 0 TO 1 BECAUSE MOUSEEVENTS ARE NOT AFFECTED BY ABOVE SETTINGS

        # addWidget(QWidget * widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        _servos_layout.addWidget(self._shutterAbsoluteMode, 0, 0, 1, 3)
        _servos_layout.addWidget(self._powerAbsoluteMode, 1, 0, 1, 3)
        _servos_layout.addWidget(_shutterChannel_label_main, 2, 0, 2, 1)
        _servos_layout.addWidget(self._shutterChannel, 2, 1, 1, 2)
        _servos_layout.addWidget(_shutterChannel_label_left, 3, 1, 1, 1)
        _servos_layout.addWidget(_shutterChannel_label_righ, 3, 2, 1, 1)

        _servos_layout.setColumnStretch(0, 2)
        _servos_layout.setColumnStretch(1, 1)
        _servos_layout.setColumnStretch(2, 1)

        _servos.setLayout(_servos_layout)
        # / Optomechanical

        # Stage Configuration
        # These are the initialization settings and does not affect the current session!
        _stage = QtWidgets.QGroupBox("Stage Settings")
        _stage_layout = QtWidgets.QGridLayout()

        _stage_xlim_label = QtWidgets.QLabel("X-Limits")
        self._stage_xlim_lower = QtWidgets.QLineEdit()
        self._stage_xlim_lower.setValidator(QtGui.QDoubleValidator()) # Accept any Double
        self._stage_xlim_upper = QtWidgets.QLineEdit()
        self._stage_xlim_upper.setValidator(QtGui.QDoubleValidator()) # Accept any Double

        _stage_ylim_label = QtWidgets.QLabel("Y-Limits")
        self._stage_ylim_lower = QtWidgets.QLineEdit()
        self._stage_ylim_lower.setValidator(QtGui.QDoubleValidator()) # Accept any Double
        self._stage_ylim_upper = QtWidgets.QLineEdit()
        self._stage_ylim_upper.setValidator(QtGui.QDoubleValidator()) # Accept any Double

        self._noHome = QtWidgets.QCheckBox("Do not home stage on start")

        _note = QtWidgets.QLabel("Limits and Homing Settings take effect only after app restart!\nStage will be initialised in the center of the limits")
        _note.setStyleSheet("color: red;")

        self._invertx = QtWidgets.QCheckBox("Invert Horizontal")
        self._inverty = QtWidgets.QCheckBox("Invert Vertical")

        _stage_layout.addWidget(_stage_xlim_label, 0, 0)
        _stage_layout.addWidget(self._stage_xlim_lower, 0, 1)
        _stage_layout.addWidget(QtWidgets.QLabel("to"), 0, 2)
        _stage_layout.addWidget(self._stage_xlim_upper, 0, 3)
        _stage_layout.addWidget(_stage_ylim_label, 1, 0)
        _stage_layout.addWidget(self._stage_ylim_lower, 1, 1)
        _stage_layout.addWidget(QtWidgets.QLabel("to"), 1, 2)
        _stage_layout.addWidget(self._stage_ylim_upper, 1, 3)
        _stage_layout.addWidget(self._noHome, 2, 0, 1, 4)
        _stage_layout.addWidget(_note, 3, 0, 1, 4)
        _stage_layout.addWidget(self._invertx, 4, 0, 1, 2)
        _stage_layout.addWidget(self._inverty, 4, 2, 1, 2)

        # TODO: Add some way of moving dx and dy

        _stage.setLayout(_stage_layout)
        # / Stage Configuration

        # Audio
        _audio = QtWidgets.QGroupBox("Audio")
        _audio_layout = QtWidgets.QVBoxLayout()

        self._disableFinishTone = QtWidgets.QCheckBox("Disable Finish Tone")
        # WE USE THIS WORKAROUND OF SETTING 0 TO 1 BECAUSE MOUSEEVENTS ARE NOT AFFECTED BY ABOVE SETTINGS

        # addWidget(QWidget * widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        _audio_layout.addWidget(self._disableFinishTone)

        _audio.setLayout(_audio_layout)
        # / Audio

        # Labels and warnings
        _persistent = QtWidgets.QLabel("These settings persists across launches! Refer to documentation for more information.")
        # / Labels and warnings

        # Buttons
        self._buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.RestoreDefaults | QtWidgets.QDialogButtonBox.Close)
        # / Buttons

        self._main_layout.addWidget(_servos, 0, 0, 1, 1)
        self._main_layout.addWidget(_audio, 1, 0, 1, 1)
        self._main_layout.addWidget(_stage, 0, 1, 2, 1)
        self._main_layout.addWidget(_persistent, 2, 0, 1, 2)
        self._main_layout.addWidget(self._buttonBox, 3, 0, 1, 2)

        self._main_layout.setColumnStretch(0, 1)
        self._main_layout.setColumnStretch(1, 1)

        self.setLayout(self._main_layout)

    def initEventListeners(self):
        self._buttonBox.rejected.connect(self.closeCheck)
        self._buttonBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(self.reset)
        self._buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)

    @property
    def set_shutterChannel(self):
        # THIS is gonna be abit confusing argh
        return servos.Servo.LEFTCH if self._set_shutterChannel == 0 else servos.Servo.RIGHTCH

    @set_shutterChannel.setter
    def set_shutterChannel(self, x):
        self._set_shutterChannel = 0 if x == servos.Servo.LEFTCH else 1

    def loadSettings(self):
        self.microGUIParent.qsettings.sync()

        self.set_shutterAbsoluteMode = self.microGUIParent.qsettings.value("shutter/absoluteMode", True, type = bool)
        self.set_shutterChannel      = self.microGUIParent.qsettings.value("shutter/channel", servos.Servo.RIGHTCH, type = int)
        self.set_powerAbsoluteMode   = self.microGUIParent.qsettings.value("power/absoluteMode", False, type = bool)
        self.set_invertx             = self.microGUIParent.qsettings.value("stage/invertx", False, type = bool)
        self.set_inverty             = self.microGUIParent.qsettings.value("stage/inverty", False, type = bool)
        self.set_stageConfig         = self.microGUIParent.qsettings.value("stage/config", None, type = dict) # Should be a dictionary
        self.set_noHome              = self.microGUIParent.qsettings.value("stage/noHome", False, type = bool)
        self.set_noFinishTone        = self.microGUIParent.qsettings.value("audio/noFinishTone", True, type = bool)

        # Update the GUI with the settings
        self._shutterAbsoluteMode.setChecked(self.set_shutterAbsoluteMode)
        self._powerAbsoluteMode.setChecked(self.set_powerAbsoluteMode)
        self._shutterChannel.setValue(self._set_shutterChannel) # we use the _ value to get 0 and 1
        self._invertx.setChecked(self.set_invertx)
        self._inverty.setChecked(self.set_inverty)
        self._disableFinishTone.setChecked(self.set_noFinishTone)

        if not self.set_stageConfig:
            self.set_stageConfig = {
                "xlim" : mstage.DEFAULT_XLIM ,
                "ylim" : mstage.DEFAULT_YLIM
            }
        self._stage_xlim_lower.setText(str(self.set_stageConfig["xlim"][0]))
        self._stage_xlim_upper.setText(str(self.set_stageConfig["xlim"][1]))
        self._stage_ylim_lower.setText(str(self.set_stageConfig["ylim"][0]))
        self._stage_ylim_upper.setText(str(self.set_stageConfig["ylim"][1]))

    def getStageConfigFromGUI(self):
        try:
            return {
                "xlim" : [float(self._stage_xlim_lower.text()), float(self._stage_xlim_upper.text())] ,
                "ylim" : [float(self._stage_ylim_lower.text()), float(self._stage_ylim_upper.text())]
            }
        except ValueError as e:
            return None


    def settingsEdited(self):
        return not (self.set_shutterAbsoluteMode == (not not self._shutterAbsoluteMode.checkState()) and \
                    self._set_shutterChannel     == self._shutterChannel.value() and \
                    self.set_powerAbsoluteMode   == (not not self._powerAbsoluteMode.checkState()) and \
                    self.set_invertx             == (not not self._invertx.checkState()) and \
                    self.set_inverty             == (not not self._inverty.checkState()) and \
                    self.set_stageConfig         == self.getStageConfigFromGUI() and \
                    self.set_noHome              == (not not self._noHome.checkState()) and \
                    self.set_noFinishTone        == (not not self._disableFinishTone.checkState())
        )

    def closeCheck(self):
        if self.settingsEdited():
            # Alert saying changes not saved
            ret = self.microGUIParent.unsavedQuestionDialog(message = "Settings Changed", informativeText = "Save or Discard?\nClick Cancel to go back.", title = "Unsaved settings", host = self)

            if ret == QtWidgets.QMessageBox.Save:
                self.apply(noDialog = False)
                return self.close()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.microGUIParent.setOperationStatus("Changed settings discarded! Ready.")
                return self.close()
        else:
            self.microGUIParent.setOperationStatus("Ready.")
            return self.close()

    def reset(self):
        self._shutterAbsoluteMode.setChecked(True)
        self._powerAbsoluteMode.setChecked(False)
        self._shutterChannel.setValue(servos.Servo.RIGHTCH) # This is fine since its = 1

        self._stage_xlim_lower.setText(str(mstage.DEFAULT_XLIM[0]))
        self._stage_xlim_upper.setText(str(mstage.DEFAULT_XLIM[1]))
        self._stage_ylim_lower.setText(str(mstage.DEFAULT_YLIM[0]))
        self._stage_ylim_upper.setText(str(mstage.DEFAULT_YLIM[1]))

        self._invertx.setChecked(False)
        self._inverty.setChecked(False)
        self._disableFinishTone.setChecked(True)

    def apply(self, noDialog = False):
        # TODO: Check for sane stage config values
        newStageConfig = self.getStageConfigFromGUI()
        if newStageConfig is None:
            return self.microGUIParent.criticalDialog(message = "Error parsing Stage limits!", host = self)
        elif newStageConfig["xlim"][0] >= newStageConfig["xlim"][1] or newStageConfig["ylim"][0] >= newStageConfig["ylim"][1]:
            return self.microGUIParent.criticalDialog(message = "Stage lower limit must be strictly lower than higher limit!", host = self)

        self._set_shutterChannel = self._shutterChannel.value() # Convert to PAN values
        self.microGUIParent.qsettings.setValue("shutter/channel", self.set_shutterChannel)

        self.microGUIParent.qsettings.setValue("shutter/absoluteMode", not not self._shutterAbsoluteMode.checkState())
        self.microGUIParent.qsettings.setValue("power/absoluteMode", not not self._powerAbsoluteMode.checkState())
        self.microGUIParent.qsettings.setValue("stage/invertx", not not self._invertx.checkState())
        self.microGUIParent.qsettings.setValue("stage/inverty", not not self._inverty.checkState())
        self.microGUIParent.qsettings.setValue("stage/noHome", not not self._noHome.checkState())
        self.microGUIParent.qsettings.setValue("stage/config", newStageConfig) # Should be a dictionary

        self.microGUIParent.qsettings.setValue("audio/noFinishTone", not not self._disableFinishTone.checkState())

        self.microGUIParent.qsettings.sync()

        # Set the settings in the main GUI also
        # We do this after sync because invertCheck() calls sync as well
        self.microGUIParent._SL_invertx_checkbox.setChecked(not not self._invertx.checkState())
        self.microGUIParent._SL_inverty_checkbox.setChecked(not not self._inverty.checkState())
        self.microGUIParent.invertCheck() # This will auto update the necessary variables

        # Update the servos absoluteMode
        self.microGUIParent.stageControl.controller.shutter.absoluteMode = (not not self._shutterAbsoluteMode.checkState())
        self.microGUIParent.stageControl.controller.powerServo.absoluteMode = (not not self._powerAbsoluteMode.checkState())
        self.microGUIParent.stageControl.controller.shutter.channel = self.set_shutterChannel
        self.microGUIParent.stageControl.controller.powerServo.channel = self.set_shutterChannel * -1

        # Update the finish tone
        self.microGUIParent.stageControl.noFinishTone = (not not self._disableFinishTone.checkState())

        # Reload from memory
        self.loadSettings()
        self.microGUIParent.setOperationStatus("Settings saved. Ready.")

        if not noDialog:
            self.microGUIParent.informationDialog(message = "Settings saved successfully.", title="Yay!", host = self)

def main(**kwargs):
    # https://stackoverflow.com/a/1857/3211506
    # Windows = Windows, Linux = Linux, Mac = Darwin
    # For setting icon on Windows
    if platform.system() == "Windows":
        # https://stackoverflow.com/a/1552105/3211506
        myappid = u'NUS.Nanomaterials.MicroGUI.0.10a' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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


# ARCHIVE CODE
# def moveToCentre(QtObj):
#     # Get center of the window and move the window to the centre
#     # Remember to setGeometry of the object first
#     # https://pythonprogramminglanguage.com/pyqt5-center-window/
#     _qtRectangle = QtObj.frameGeometry()
#     _centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
#     _qtRectangle.moveCenter(_centerPoint)
#     QtObj.move(_qtRectangle.topLeft())

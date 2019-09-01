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

import platform, ctypes # For Windows Icon

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import stagecontrol
import servos
from micron import Stage as mstage # for default x and y lims

from extraFunctions import moveToCentre

class MicroGui(QtWidgets.QMainWindow):
    def __init__(self, devMode = False, noHome = False):
        super().__init__()

        self.micronInitialized = False
        self.currentStatus = ""
        self.devMode = devMode

        self.noHome = noHome

        self.customicon = os.path.join(base_dir, 'icons', 'guimicro.svg')

        # symboldefs
        self.MICROSYMBOL = u"\u00B5"

        self.KEYSTROKE_TIMEOUT = 10 # ms
        # Default based on 100ums / 10um
        # need to change on speed and interval change

        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 800, 600) # x, y, w, h

        moveToCentre(self)

        self.setWindowTitle('Micos Stage Controller MARK II 0.10a')
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
        self.initializeDevice()
        self.initEventListeners()
        self.recalculateARValues()

        # Set to the last menu item
        self.showPage(self.main_widget.count() - 1)

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

        self.logconsole("Settings Loaded:\n\tShutterAbsolute = {}\n\tShutterChannel = {}\n\tPowerAbsolute = {}\n\tInvert-X = {}\n\tInvert-Y = {}\n\tStageConfig = {}\n\tnoHome = {}".format(
            self.set_shutterAbsoluteMode ,
            self.set_shutterChannel      ,
            self.set_powerAbsoluteMode   ,
            self.set_invertx             ,
            self.set_inverty             ,
            self.set_stageConfig         ,
            self.noHome                  ,
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

    def KeyboardInterruptHandler(self, signal = None, frame = None):
        # 2 args above for use with signal.signal

        self.setOperationStatus("^C Detected: Aborting the FIFO stack. Shutter will be closed as part of the aborting process.")

        if not self.devMode:
            self.stageControl.controller.shutter.close()
            self.stageControl.controller.abort()

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
                    self.stageControl = stagecontrol.StageControl(noCtrlCHandler = True, devMode = True, GUI_Object = self)

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
                        )

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

            # Clean up unneeded settings

            del self.set_shutterChannel
            del self.set_shutterAbsoluteMode
            del self.set_powerAbsoluteMode
            del self.set_invertx
            del self.set_inverty
            del self.set_stageConfig

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
        _modes = [
            QtWidgets.QPushButton("Draw &Picture") ,
            QtWidgets.QPushButton("&Array Raster") ,
            QtWidgets.QPushButton("Single &Raster") ,
            QtWidgets.QPushButton("&Stage Movement")
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

        if page == 3:
            self.updatePositionDisplay()

# Shutter Control layout

    @make_widget_from_layout
    def create_shutter_control(self, widget):
        _shutter_layout = QtWidgets.QHBoxLayout()

        # Shutter controls
        self._shutter_label = QtWidgets.QLabel("Shutter Controls")
        self._shutter_state = QtWidgets.QLabel() # Change color
        self._open_shutter  = QtWidgets.QPushButton("&Open")
        self._close_shutter = QtWidgets.QPushButton("&Close")

        self._shutter_state.setStyleSheet("QLabel { background-color: #DF2928; }")
        self._shutter_state.setAlignment(QtCore.Qt.AlignCenter)

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

        # Start button

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

        self._SR_raster_style = QtWidgets.QLabel("Filled square\nStepping along y-axis")
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
        # / Settings

        _single_raster_layout.addWidget(_SR_settings)

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

        self._AR_raster_style = QtWidgets.QLabel("Filled square\nStepping along y-axis")
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

        _drawpic_layout.addWidget(QtWidgets.QLabel("Draw Pic Layout"))

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

        # SHUTTER
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

        # return QtWidgets.QWidget.eventFilter(self, source, evt)
        return super(QtWidgets.QWidget, self).eventFilter(source, evt)

# Custom functions
    def homeStage(self):
        if not self.devMode:
            self.setOperationStatus("Homing stage...If any error arises, abort immediately with Ctrl + C")
            self.stageControl.controller.homeStage()
            self.setOperationStatus("Home stage finished")
        else:
            self.setOperationStatus("devMode, not homing...")

    def cardinalMoveStage(self, dir):
        # Get the distance
        dist = float(self._SL_step_size.text())
        vel  = float(self._SL_velocity.text())

        # Move the stage
        if not self.devMode:
            self.moveStage(dir, distance = dist, velocity = vel)

    def moveStage(self, dir, distance, velocity):
        # dir is a (dx, dy) tuple/vector that defines the direction that gets multiplied by distance
        if sum(map(abs, dir)) > 1:
            _mag = math.sqrt(dir[0]**2 + dir[1]**2)
            dir = (dir[0] / _mag , dir[1] / _mag)

        if not self.cardinalStageMoving:
            self.cardinalStageMoving = True

            if self.stageControl.controller.velocity != velocity:
                # We reset the velocity if it is different
                self.stageControl.controller.setvel(velocity)

            self.stageControl.controller.rmove(x = dir[0] * distance * self.stageControl.noinvertx, y = dir[1] * distance * self.stageControl.noinverty)
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
                self._AR_raster_style.setText("Filled {}\nStepping along x-axis".format(indiv_type))
                self._AR_step_size.setReadOnly(False)
                self._AR_step_size.setStyleSheet("background-color: none; color: #000;")
            elif step_along_y:
                self._AR_raster_style.setText("Filled {}\nStepping along y-axis".format(indiv_type))
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

                self.setOperationStatus("Starting Array Raster...")

                self.stageControl.arrayraster(
                    xDist      = size[1],         yDist      = size[0],
                    xGap       = x_spac,          yGap       = y_spac,
                    nrows      = y_rows,          ncols      = x_cols,
                    inivel     = vel_0,           inipower   = pow_0,
                    x_isVel    = x_isPow ^ 1,     y_isVel    = y_isPow ^ 1,
                    xincrement = x_incr,          yincrement = y_incr,
                    rasterSettings = rsSettings,
                    returnToOrigin = returnToOrigin
                )
            elif startRaster:
                # Alert got error
                self.criticalDialog(message = "Error in array raster settings.\nPlease check again!", host = self)

# Helper functions
    def setOperationStatus(self, status, printToTerm = True, **printArgs):
        self.currentStatus = status
        if printToTerm:
            print("[{}]".format(datetime.datetime.now().time()), status, **printArgs)
        # Do some updating of the status bar
        self._statusbar_label.setText(status)

    def logconsole(self, status):
        print("[{}]".format(datetime.datetime.now().time()), status)

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

        _msgBox.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        return _msgBox.exec_()

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

        # _msgBox.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        return _msgBox.exec_()

    def unsavedQuestionDialog(self,message, title = "Unsaved", informativeText = None, host = None):
        _msgBox = QtWidgets.QMessageBox(host)
        _msgBox.setIcon(QtWidgets.QMessageBox.Question)
        _msgBox.setWindowTitle(title)
        _msgBox.setText(message)
        if informativeText is not None:
            _msgBox.setInformativeText(informativeText)

        _msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        _msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)

        # Get height and width
        _h = _msgBox.height()
        _w = _msgBox.width()
        _msgBox.setGeometry(0, 0, _w, _h)

        moveToCentre(_msgBox)

        # mb.setTextFormat(Qt.RichText)
        # mb.setDetailedText(message)

        # _msgBox.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        return _msgBox.exec_()

# Status Bar

class aboutPopUp(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initUI()

    def initUI(self):
        # x, y, w, h
        self.setGeometry(0, 0, 250, 200)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
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
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

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

        # Labels and warnings
        _persistent = QtWidgets.QLabel("These settings persists across launches! Refer to documentation for more information.")
        # / Labels and warnings

        # Buttons
        self._buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.RestoreDefaults | QtWidgets.QDialogButtonBox.Close)
        # / Buttons

        self._main_layout.addWidget(_servos, 0, 0)
        self._main_layout.addWidget(_stage, 0, 1)
        self._main_layout.addWidget(_persistent, 1, 0, 1, 2)
        self._main_layout.addWidget(self._buttonBox, 2, 0, 1, 2)

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

        # Update the GUI with the settings
        self._shutterAbsoluteMode.setChecked(self.set_shutterAbsoluteMode)
        self._powerAbsoluteMode.setChecked(self.set_powerAbsoluteMode)
        self._shutterChannel.setValue(self._set_shutterChannel) # we use the _ value to get 0 and 1
        self._invertx.setChecked(self.set_invertx)
        self._inverty.setChecked(self.set_inverty)

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
                    self.set_noHome              == (not not self._noHome.checkState()) \
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

    def apply(self, noDialog = False):
        # TODO: Check for sane stage config values
        newStageConfig = self.getStageConfigFromGUI()
        if newStageConfig is None:
            return self.microGUIParent.criticalDialog(message = "Error parsing Stage limits!", host = self)
        elif newStageConfig["xlim"][0] >= newStageConfig["xlim"][1] or newStageConfig["ylim"][0] >= newStageConfig["ylim"][1]:
            return self.microGUIParent.criticalDialog(message = "Stage lower limit must be strictly lower than higher limit!", host = self)

        self.set_shutterChannel = self._shutterChannel.value() # Convert to PAN values
        self.microGUIParent.qsettings.setValue("shutter/channel", self.set_shutterChannel)

        self.microGUIParent.qsettings.setValue("shutter/absoluteMode", not not self._shutterAbsoluteMode.checkState())
        self.microGUIParent.qsettings.setValue("power/absoluteMode", not not self._powerAbsoluteMode.checkState())
        self.microGUIParent.qsettings.setValue("stage/invertx", not not self._invertx.checkState())
        self.microGUIParent.qsettings.setValue("stage/inverty", not not self._inverty.checkState())
        self.microGUIParent.qsettings.setValue("stage/noHome", not not self._noHome.checkState())
        self.microGUIParent.qsettings.setValue("stage/config", newStageConfig) # Should be a dictionary

        self.microGUIParent.qsettings.sync()

        # Set the settings in the main GUI also
        # We do this after sync because invertCheck() calls sync as well
        self.microGUIParent._SL_invertx_checkbox.setChecked(not not self._invertx.checkState())
        self.microGUIParent._SL_inverty_checkbox.setChecked(not not self._inverty.checkState())
        self.microGUIParent.invertCheck() # This will auto update the necessary variables

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

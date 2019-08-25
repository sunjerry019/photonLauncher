# also using qt designer to get quick visual preview of how the window should look like. Please install qt designer to open the .ui file. It CAN be converted to python code, but its like a translated-from-c++ version and very inelegant. Trying to define the functions individually for easier debugging/edits.
# WMS's attempt at starting the graphical user interface effort for the benefit of future members of the Nanomaterials lab ("if only everything can be done with a single click of a single button")


# from PyQt4 import QtCore, QtGui

def stageInit(self):
	self.home_position = QtWidgets.QPushButton("Move to absolute home (0,0)")
    self.set_origin = QtWidgets.QPushButton("Set as (0,0)")

    self.velocity = QtWidgets.QLineEdit()
    self.velocity.setValidator(QtGui.QIntValidator(0,1000))
    self.velocity.setFont(QtGui.QFont("Arial",20))

    self.step_size = QtWidgets.QLineEdit()
    self.step_size.setValidator(QtGui.QIntValidator(0.5,1000))
    self.step_size.setFont(QtGui.QFont("Arial",20))

    # need to link to stagecontrol to read position of controllers
    self.lcdx = QtWidgets.QLCDNumber()
    self.lcdy = QtWidgets.QLCDNumber()

    self.stage_layout = QtWidgets.QGridLayout()
    self.stage_layout.addWidget(self.home_position)
    self.stage_layout.addWidget(self.set_origin)
    self.stage_layout.addWidget(self.velocity)
    self.stage_layout.addWidget(self.step_size)
    self.stage_layout.addWidget(self.lcdx)
    self.stage_layout.addWidget(self.lcdy)

    # self.stage_layout.addWidget(self.stage_layout)

    self.stage_widget = QtWidgets.QWidget()


# MENU

        file_menu.triggered[QtWidgets.QAction].connect(self.processtrigger)

    def processtrigger(self,q):
        print(q.text()+" is triggered")
"""
from the comments of stepmotor2.c:
   go num pos                  travels motor num to a given position
                               number of steps
   set num [pos]               sets absolute pos  of motor num
   init num [volts [maxspeed]] initialize, and switch on
   [on|off] num                switch motor num on
   exit                        leave program
   setvolt num [volt]          set voltage of motor num
   setspeed num [speed]        set speed of motor num
   reset
   break
   vmode num                   set in move mode
   pmode num                   set in pos mode
   limit num [limitmode]       toggle limit switches; 0 is default which
                               means limit swithches are ignored
"""
import subprocess


class MotorController(subprocess.Popen):
    """
    Object to interact with Owis sm40 PCI card through the stepmotor2 program.
    """
    cmd = '/home/qitlab/programs/owis2/apps/stepmotor2'

    def __init__(self):
        subprocess.Popen.__init__(self, self.cmd,
                                  stderr=subprocess.STDOUT,
                                  stdin=subprocess.PIPE)

    def __del__(self):
        self.write('exit')
        subprocess.Popen.__del__(self)

    def write(self, opts):
        self.stdin.write(opts+'\n')


class Axes():
    """
    Objects used to control each individual motor
    """

    def __init__(self, driver, axes_id, voltage=6):
        self.driver = driver
        self.axes_id = axes_id
        self.set_voltage(voltage)
        self.on()

    def on(self):
        """
        Locks the magnet in the stepper motor
        """
        self.driver.write('on {0}'.format(self.axes_id))

    def off(self):
        """
        Unlocks the magnet in the stepper motor
        """
        self.driver.write('off {0}'.format(self.axes_id))

    def go(self, position):
        """
        Go to absolute position
        """
        self.driver.write('go {0} {1}'.format(self.axes_id, position))

    def set_voltage(self, voltage):
        self.driver.write('setvolt {0} {1}'.format(self.axes_id, voltage))

    # def get_position(self):
    #     self.driver.write('pos? {0};'.format(self.axes_id))
    #     return self.driver.readline().strip()

    def set_pos_counter(self, abs_pos):
        """
        Current position is set to given abs_ps
        """
        self.driver.write('set {0} {1}'.format(self.axes_id, abs_pos))


class LinearAxes(Axes):
    """
    Wrapping the serial interface of a linear axes
    """

    steps_per_mm = 3200

    def go_mm(self, value):
        position = int(self.steps_per_mm*value)
        self.go(position)

    def set_pos_counter_mm(self, abs_mm):
        position = int(self.steps_per_mm*abs_mm)
        self.set_pos_counter(position)

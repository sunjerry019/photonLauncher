"""
written by Mathias Seidler, 16.6.14, Singapore
## V0 created Mon, 16 Jun 2014
    * implemented basic functionality
    * only rotating axes implemented

2015.04.23 A.C. added new classes for linear motor and DTM40


"""

import glob

import serial
import time

# Global parameter, it affects all the axis
g_speed = 600


class MotorController(serial.Serial):
    """
    MotorController is the controller of the motors.
    It provides axes objects, which can be requested
    via make_...._axes functions.
    It manages the driver and globas commands,
    concering all axes connected to this Controller
    It is wrapping serial commands to the motor driver

        * make_...... will return an instance of an axes
                      For every type of axes there is a make_... method.

    """

    def __init__(self, device_path=None, baudrate=4800, timeout=1):
        if device_path is None:
            device_path = glob.glob('/dev/serial/by-id/*USB-Serial_Controller*')[0]
        try:
            serial.Serial.__init__(self, device_path, baudrate)
            self.timeout = timeout
        except OSError:
            print('The indicated device cannot be found')
        self.set_speed_for_all_motors(g_speed)

    def make_rotating_axes(self, axes_id):
        """
        Returns a rotating axes motor instance
        """
        return RotatingAxes(self, axes_id)

    def make_linear_axes(self, axes_id):
        return LinearAxes(self, axes_id)

    def make_dtm40(self, axes_id):
        return DTM40(self, axes_id)

    def halt_all_motors(self):
        self.write('break;')

    def get_idn(self):
        self.write('*IDN?;')
        return self.readline().strip()

    def set_speed_for_all_motors(self, speed):
        self.write('setspeed {0};'.format(speed))


class Axes:
    """
    Wrapping the serial interface of a motor axis
    """

    motor_volt = 3000

    def __init__(self, driver, axes_id, voltage=motor_volt):
        self.driver = driver
        self.axes_id = axes_id
        self.set_voltage(voltage)
        self.on()

    def on(self):
        """
        Locks the magnet in the stepper motor
        """
        self.driver.write('on {0};'.format(self.axes_id))

    def off(self):
        """
        Unlocks the magnet in the stepper motor
        """
        self.driver.write('off {0};'.format(self.axes_id))

    def go(self, position):
        """
        Go to absolute position
        """
        self.driver.write('go {0} {1};'.format(self.axes_id, position))

    def set_voltage(self, voltage):
        self.driver.write('setvolt {0} {1};'.format(self.axes_id, voltage))

    def get_position(self):
        self.driver.write('pos? {0};'.format(self.axes_id))
        return self.driver.readline().strip()

    def set_pos_counter(self, abs_pos):
        """
        Current position is set to given abs_ps
        """
        self.driver.write('set {0} {1};'.format(self.axes_id, abs_pos))

    def go_wait(self, position):
        """
        Send the move command to the motor and polls the motor position
        until the motor reaches the desired position.

        :param position: desired position in steps
        """
        self.go(position)
        while self.get_position() != position:
            time.sleep(.005)


class RotatingAxes(Axes):
    """
    Wrapping the serial interface for the rotary motor
    DRTM 40 (Waveplate holder motor)
    http://qoptics.quantumlah.org/wiki/index.php/Waveplate/Rotation_motor_resolution

    # notes
    600 steps = 45 degrees
    voltage = 3000
    speed = 600
    """
    # Typical values for some of the parameters
    # of the rotation stages from owis
    steps_per_degree = float(600)/45

    def go_deg(self, degrees):
        """
        Use this if you want to use degrees instead of motorsteps.
        The motor steps are rounded to int,
        this could introduce some inaccuracy
        :param degrees: desired position in degrees
        """
        position = int(self.steps_per_degree*degrees)  # rounded position
        self.go(position)

    def set_pos_counter_degrees(self, abs_degrees):
        position = int(self.steps_per_degree*abs_degrees)
        self.set_pos_counter(position)


class DTM40(Axes):
    """
    Wrapping the serial interface of the DTM40 (Spectrometer motor)
    http://qoptics.quantumlah.org/wiki/index.php/Waveplate/Rotation_motor_resolution

    # notes
    2160 steps = 45 degrees
    voltage = 900
    speed = 600
    """
    # Typical values for some of the parameters
    # of the rotation stages from owis
    steps_per_degree = float(2160)/45
    motor_volt = 900

    def go_deg(self, degrees):
        """
        Use this if you want to use degrees instead of motorsteps.
        The motor steps are rounded to int,
        this could introduce some inaccuracy
        :param degrees: desired position in degrees
        """
        position = int(self.steps_per_degree*degrees)  # rounded position
        self.go(position)

    def set_pos_counter_degrees(self, abs_degrees):
        position = int(self.steps_per_degree*abs_degrees)
        self.set_pos_counter(position)


class LinearAxes(Axes):
    """
    Wrapping the serial interface of a linear axes
    """

    steps_per_mm = 3200

    def go_mm(self, value):
        position = int(self.steps_per_mm*value)
        self.set_go(position)

    def set_pos_counter_mm(self, abs_mm):
        position = int(self.steps_per_mm*abs_mm)
        self.set_pos_counter(position)

    def go_wait_mm(self, value):
        position = int(self.steps_per_mm*value)
        self.go_wait(position)

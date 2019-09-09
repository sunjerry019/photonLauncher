#!/usr/bin/env python3

# Python secondary Helper to send differentiated PWM signals to control power and shutter servos serving different experimental purposes

# Additional servo = laser power adjustments, via mounting a rotation graduated neutral density filter (in documentation) we can vary laser power with rotation of filter.
# We are probably using one of two kinds of servos: SG90 9g, and SG90 9g 360. All PWM generated will have positive (polarity = True) voltage, unless inversion is needed for weird computer soundcards.
# SG90 9g has a 180 degree range, and uses PWM pulses as signals, so the duty cycle of the 50Hz signal gives the ABSOLUTE position of the shaft (motor will try to move to position as long as pulse duration is long enough)
# SG90 9g 360 is a modified version of SG90 9g, and uses PWM signals as SPEED indicators, where DURATION and SPEED will determine the precise RELATIVE movement from any position.

# Duty cycle ratios of interest for the servos for 50Hz signal:
# SG90 9g -> 0.15, 0.1, 0.05
# SG90 9g 360 -> 0.075 (static), 0.080 (minimum for movement in one direction), 0.070 (minimum for movement in the other)


# Made 2019, Wu Mingsong, Sun Yudong
# mingsongwu [at] outlook [dot] sg, sunyudong [at] outlook [dot] sg,

###
from pwmaudio import Pulsegen

import time

class Servo():
    LEFTCH = -1
    RIGHTCH = 1
    DEFAULT_DURATION = 400

    def __init__(self, absoluteMode = False, channel = -1):
        print('\n\nABSOLUTE MODE IS', absoluteMode,'\n')

        self.channel = channel

        print('Channel:',self.human_channel)

        self.absoluteMode = absoluteMode

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
        if channel == self.LEFTCH:
            self.human_channel = "Left Channel"
        elif channel == self.RIGHTCH:
            self.human_channel = "Right Channel"
        else:
            self.human_channel = "Pan = {}".format(channel)

    # The most general format for PWM signal control
    def absolute(self, duty, polarity = True, freq = 50, duration = DEFAULT_DURATION):
        with Pulsegen(duty, polarity, freq, duration, pan = self.channel) as p:
            p.playpulse()

    def __enter__(self):
        #self.close()
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.close()

class Shutter(Servo):
    NONABSOLUTE_DURATION = 100

    @property
    def duration(self):
        return self.DEFAULT_DURATION if self.absoluteMode else self.NONABSOLUTE_DURATION

    def __init__(self, GUI_Object = None, quietLog = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.GUI_Object = GUI_Object
        self.quietLog = quietLog

        self.homeclose() if not self.absoluteMode else self.close()
        self.isOpen = False

    ## Shutter servo functions
    # This is the "over extended" range of 180 degree servo (>180 degrees). Reserved for closed state, where 180 degrees would be open, ready for 180-0 degrees scanning
    def close(self, shutter_state_label = None):
        self.absolute(0.15) if self.absoluteMode else self.absolute(0.09, duration = self.NONABSOLUTE_DURATION)

        if self.GUI_Object is not None and not self.quietLog:
            self.GUI_Object.setOperationStatus("Closing Shutter")
        else:
            print("Closing Shutter")

        self.isOpen = False

        if shutter_state_label is None and self.GUI_Object is not None:
            shutter_state_label = self.GUI_Object._shutter_state

        if shutter_state_label is not None:
            # Qt QLabel Object
            shutter_state_label.setStyleSheet("QLabel { background-color: #00A151; color: #fff; }")
            shutter_state_label.setText("Closed")

        return True

    def open(self, shutter_state_label = None):
        self.absolute(0.1) if self.absoluteMode else self.absolute(0.06, duration = self.NONABSOLUTE_DURATION)

        if self.GUI_Object is not None and not self.quietLog:
            self.GUI_Object.setOperationStatus("Opening Shutter")
        else:
            print("Opening Shutter")

        self.isOpen = True

        if shutter_state_label is None and self.GUI_Object is not None:
            shutter_state_label = self.GUI_Object._shutter_state

        if shutter_state_label is not None:
            shutter_state_label.setStyleSheet("QLabel { background-color: #DF2928; color: #fff; }")
            shutter_state_label.setText("Opened")

        return True

    # This is for the continuous rotation servo motor shutters. Provides a homing function: motor rotates untill axle hits a physical block where it will stall temporarily. It then rotates in the other direction to closed position.
    def homeclose(self):
        self.absolute(0.085, duration = 1400)
        time.sleep(1)
        self.absolute(0.06, duration = 300)
        return True

class Power(Servo):
    ## Power servo functions, assume servo is 360 version, non absolute positioning.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._displacement = 0

    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, displacement):
        difference = displacement - self._displacement
        if isinstance(difference, int) or (isinstance(difference, float) and number.is_integer()):
            if difference != 0:
                self.powerstep(abs(difference), direction = (difference > 0))
        else:
            # We need difference to be an integer
            raise RuntimeException("Displacement must be an integer")

    def powerstep(self, number):
        if not (isinstance(number, int) or (isinstance(number, float) and number.is_integer())):
            raise RuntimeException("Displacement must be an integer")

        if number < 0:
            for i in range(-1 * number):
                self.absolute(0.07, duration = 130)
                self._displacement += 1
                time.sleep(0.5)
        else:
            for i in range(number):
                self.absolute(0.079, duration = 210)
                self._displacement -= 1
                time.sleep(0.5)



if __name__ == '__main__':
    with Servo(channel = Servo.LEFTCH, absoluteMode = False) as s:
        print("\n\nUse s as Shutter()\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

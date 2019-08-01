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
    def absolute(self, duty, polarity = True, freq = 50, duration = 400):
        with Pulsegen(duty, polarity, freq, duration, pan = self.channel) as p:
            p.playpulse()

    def __enter__(self):
        #self.close()
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.close()

class Shutter(Servo):
    def __init__(self, GUI_Object = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.GUI_Object = GUI_Object

        self.homeclose() if not self.absoluteMode else self.close()
        self.isOpen = False

    ## Shutter servo functions
    # This is the "over extended" range of 180 degree servo (>180 degrees). Reserved for closed state, where 180 degrees would be open, ready for 180-0 degrees scanning
    def close(self, shutter_state_label = None):
        self.absolute(0.15) if self.absoluteMode else self.absolute(0.09, duration = 100)

        if self.GUI_Object is not None:
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
        self.absolute(0.1) if self.absoluteMode else self.absolute(0.06, duration = 100)

        if self.GUI_Object is not None:
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
    ## Power servo functions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # incremental step scan from one position to another for ND filter rotation control.
    def scan(self, p1, p2, increment_level):
        try:
            if (isinstance(p1, float) and isinstance(p2, float)) or ("." in str(p1) and "." in str(p2)):
                val1, val2 = float(p1), float(p2) if (isinstance(p1, str) or isinstance(p2, str)) else p1, p2
                val1, val2 = int(round(val1)), int(round(val2))
                print(val1, "_", val2, "I rounded to nearest integers!")
            else:
                val1, val2 = p1, p2 if (isinstance(p1, int) and isinstance(p2, int)) else int(p1), int(p2)
                print(val1, "_", val2, "Integers accepted.")

        except ValueError:
            print("Did you input a NUMBER?")

        # for ABSOLUTEMODE: as convention, lets take position 0 (0.15 duty) as closed, position 1 - position n as the increments from 180 degrees to 0.
        if self.absolute == True:
            if val1 < val2:
                for i in range(val1,val2+1):
                    dc = 0.1 - (0.002)*(i-1)
                    self.absolute(dc)
                    print("DUTY CYCLE = ", dc)
            else:
                for i in range(val1,val2+1):
                    dc = 0.017 + (0.002)*(i-1)
                    self.absolute(dc)
                    print("DUTY CYCLE = ", dc)

        # for nonABSOLUTE 360 servo:
        # else:

if __name__ == '__main__':
    with Shutter(channel = Servo.LEFTCH, absoluteMode = True) as s:
        print("\n\nUse s as Shutter()\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

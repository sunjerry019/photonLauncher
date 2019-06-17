#!/usr/bin/env python3

# Python Helper to control an optical shutter

# Current setup involves sending a mono audio PWM signal from the left (or right) channel to control a microservo
# We use a USB soundcard/default audio jack to output audio waveform, but since it is usually 2V peak, we need an Op-Amp circuit to boost to ~5V
# The other mono channel is left for playing an alarm sound when rastering is almost done
# Please check documentation for USB powered circuit powering servo and op amp circuit

# Made 2019, Wu Mingsong, Sun Yudong
# mingsongwu [at] outlook [dot] sg, sunyudong [at] outlook [dot] sg,

# WAV files are favoured as signal sources as they are lossless as compared to MP3
# Each WAV file actually contain the data for the rest of the positions as well, no risk of lost data.
# 1ms and 2ms duty cycle are reserved for on and off for the shutter servo since they are orthogonal positions to each other.
# Additional servo = laser power adjustments, via mounting a wheeled neutral density filter (in documentation) we can vary laser power with rotation of filter.

# playsound is an independent python package for sound playing
import playsound
import time
import glob

class Shutter():
    def __init__(self):
        self.close()
        self.isOpen = False

    def close(self):
        # print("Closing Shutter")
        playsound.playsound('sound/position1_1.0msduty.wav')
        self.isOpen = False
        return True

    def open(self):
        # print("Opening Shutter")
        playsound.playsound('sound/position11_2.0msduty.wav')
        self.isOpen = True
        return True

# incremental step control (absolute position) for ND filter rotation control
    def abpos(self, p):
        try:
            if "." in p:
                val = float(p)
                val = int(round(val))
                print(val, "Yes, user input is a float number.")
            else:
                val = int(p)
                print(val, "Yes, input string is an Integer.")
        except ValueError:
            print("Did you input a NUMBER? \n For reference, here are the possible positions: \n Position 1 = 1.0ms duty cycle \n Position 1 = 1.0ms duty cycle \n Position 2 = 1.1ms duty cycle \n Position 3 = 1.2ms duty cycle \n Position 4 = 1.3ms duty cycle \n Position 5 = 1.4ms duty cycle \n Position 6 = 1.5ms duty cycle \n Position 7 = 1.6ms duty cycle \n Position 8 = 1.7ms duty cycle \n Position 9 = 1.8ms duty cycle \n Position 10 = 1.9ms duty cycle \n Position 11 = 2.0ms duty cycle \n Position 12 = 3.0ms duty cycle \n")
        for i in range(1,val):
            n = glob.glob('sound/position{}_*'.format(val))
            print('Affirmative, now playing', n[0], '...done.')
            playsound.playsound(n[0])

    def pulse(self, lag):
        self.close()
        self.open()
        time.sleep(lag*0.001)
        self.close()


    def __enter__(self):
        self.close()
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.close()

if __name__ == '__main__':
    with Shutter() as s:
        print("\n\ns = Shutter();\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

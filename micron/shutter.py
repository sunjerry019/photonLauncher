#!/usr/bin/env python3

# Python Helper to control an optical shutter

# Current setup involves sending a mono audio PWM signal from the left (or right) channel to control a microservo
# We use a USB soundcard to output audio waveform, but since it is usually 2V peak, we need an Op-Amp circuit to boost to ~5V
# The other mono channel is left for playing an alarm sound when rastering is almost done
# Please check documentation for USB powered circuit powering servo and op amp circuit

# Made 2019, Sun Yudong, Wu Mingsong
# sunyudong [at] outlook [dot] sg, mingsongwu [at] outlook [dot] sg

# WAV files are favoured as signal sources as they are lossless as compared to MP3

# playsound is an independent python package for sound playing
import playsound
import time

class Shutter():
    def __init__(self):
        self.close()
        self.isOpen = False

    def close(self):
        # print("Closing Shutter")
        playsound.playsound('sound/position2_1msduty.wav')
        self.isOpen = False
        return True

    def open(self):
        # print("Opening Shutter")
        playsound.playsound('sound/position1_0.5msduty.wav')
        self.isOpen = True
        return True

    def out(self, offset):
        n = round(offset)
        playsound.playsound('sound/position{}_{}msduty.wav'.format(n,n*0.5))

    def pulse(self, time):
        self.close()
        self.open()
        time.sleep(time*0.001)
        self.close()

    def

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

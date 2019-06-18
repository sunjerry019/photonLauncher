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

# playsound is an independent python package for sound playing, while pydub uses either ffmpeg or pysound
import playsound
import time
from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.playback import play

class wmsPulse(SignalGenerator):
    def __init__(self, duty = 0.1, freq = 50, **kwargs):
        super().__init__(**kwargs)
        self.freq = freq
        self.duty_cycle = duty

    def generate(self):
        sample_n = 0

        # in samples
        cycle_length = self.sample_rate / float(self.freq)
        pulse_length = cycle_length * self.duty_cycle

        while True:
            if (sample_n % cycle_length) < pulse_length:
                yield 1.0

            else:
                yield 0
            sample_n += 1

    def audiomechano(self, duty, freq = 50, duration = 400):
        sound = wmsPulse(duty, freq)
        sound_segment = sound.to_audio_segment(duration)
        play(sound_segment)

pwm = wmsPulse()

class Shutter():
    def __init__(self):
        self.close()
        self.isOpen = False

    # absolute positioning depending on duty cycle, effective range -> 0.017 to 0.1, sweeps 180 degrees.
    def absolute(self, duty_cycle):
        pwm.audiomechano(duty_cycle)

    # This is the "over extended" range of servo (>180 degrees). Reserved for closed state, where 180 degrees would be open, ready for 180-0 degrees scanning
    def close(self):
        print("Closing Shutter")
        self.absolute(0.15)
        #playsound.playsound('sound/position1_1.0msduty.wav')
        self.isOpen = False
        return True

    def open(self):
        print("Opening Shutter")
        # provisional lag since keyboard strokes send a pulse to causing incomplete shutter opening
        time.sleep(0.5)
        self.absolute(0.1)
        #playsound.playsound('sound/position1_1.0msduty.wav')
        self.isOpen = True
        return True

# incremental step scan from one position to another for ND filter rotation control.
# as convention, lets take position 0 (0.15 duty) as closed, position 1 - position n as the increments from 180 degrees to 0.
    def scan(self, p1, p2):
        try:
            if "." in str(p1) and "." in str(p2):
                val1, val2 = float(p1), float(p2)
                val1, val2 = int(round(val1)), int(round(val2))
                print(val1, "_", val2, "I rounded to nearest integers!")
            else:
                val1, val2 = int(p1), int(p2)
                print(val1, "_", val2, "Integers accepted.")
        except ValueError:
            print("Did you input a NUMBER?)
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
            # n = glob.glob('sound/position{}_*'.format(i))
            # print('Affirmative, now playing', n[0], '...done.')
            # playsound.playsound(n[0])

    def flicker(self, lag):
        self.close()
        self.open()
        time.sleep(lag*0.001)
        self.close()


    def __enter__(self):
        #self.close()
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.close()

if __name__ == '__main__':
    with Shutter() as s:
        print("\n\ns = Shutter();\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

#!/usr/bin/env python3

# Python Helper to control an optical shutter

# Current setup involves sending a mono audio PWM signal from the left (or right) channel to control a microservo
# We use a USB soundcard/default audio jack to output audio waveform, but since it is usually 2V peak, we need an Op-Amp circuit to boost to ~5V
# The other mono channel is left for playing an alarm sound when rastering is almost done
# Please check documentation for USB powered circuit powering servo and op amp circuit

# Made 2019, Wu Mingsong, Sun Yudong
# mingsongwu [at] outlook [dot] sg, sunyudong [at] outlook [dot] sg,

# WAV files are favoured as signal sources as they are lossless as compared to MP3
# Additional servo = laser power adjustments, via mounting a rotation graduated neutral density filter (in documentation) we can vary laser power with rotation of filter.
# We are probably using one of two kinds of servos: SG90 9g, and SG90 9g 360, where the polarity parameter provides for potential 360 degree range for the latter. Else, all PWM generated will have positive (polarity = True) voltage.
# Sound player module is simpleaudio, which is cross platform, dependency free. It is nested in play(sound_segment) and plays the audio file created in situ before the entire Pulsegen class destructs after each audio command. Wholesome, organic, grass-fed audio solution...
# For playing saved .wav files, we should use python sounddevices to choose the output device first

import time
from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.playback import play

class Pulsegen(SignalGenerator):

    def __init__(self, duty, polarity = True, freq = 50, duration = 400, **kwargs):
        super().__init__(**kwargs)
        self.freq = freq
        self.duty = duty
        self.polarity = polarity
        self.duration = duration

    def generate(self):
        sample_n = 0

        # in samples
        cycle_length = self.sample_rate / float(self.freq)
        pulse_length = cycle_length * self.duty

        while True:
            if (sample_n % cycle_length) < pulse_length:
                if self.polarity == True:
                    yield 1.0
                else:
                    yield -1.0
            else:
                yield 0
            sample_n += 1

    def playpulse(self):
        sound_segment = self.to_audio_segment(self.duration)
        play(sound_segment)

    def __enter__(self):
        print('\n\nPulse generator initialising...done\n\n')
        return self

    def __exit__(self, e_type, e_val, traceback):
        print('\n\n Pulse generator self destructing...done\n\n')

class Shutter():
    def __init__(self):
        self.close()
        self.isOpen = False

    def absolute(self, duty, polarity, freq = 50, duration = 400):
        with Pulsegen(duty, polarity, freq, duration) as p:
            p.playpulse()

    # This is the "over extended" range of 180 degree servo (>180 degrees). Reserved for closed state, where 180 degrees would be open, ready for 180-0 degrees scanning
    def close(self):
        self.absolute(0.15, 1)
        print("Closing Shutter")
        self.isOpen = False
        return True

    def open(self):
        print("Opening Shutter")
        self.absolute(0.1, 1)
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
            print("Did you input a NUMBER?")
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
        time.sleep(lag / 1000)
        self.close()


    def __enter__(self):
        #self.close()
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.close()

if __name__ == '__main__':
    with Shutter() as s:
        print("\n\nUse s as Shutter()\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

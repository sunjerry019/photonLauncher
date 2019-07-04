#!/usr/bin/env python3

# Python Helper to control an optical shutter

# Current setup involves sending a mono audio PWM signal from the left (or right) channel to control a microservo
# We use a USB soundcard/default audio jack to output audio waveform, but since it is usually 2V peak DC, we need an Op-Amp circuit to boost to ~5V
# The other mono channel is left for playing an alarm sound when rastering is almost done
# Please check documentation for USB powered circuit powering servo and op amp circuit

# WAV files are favoured as signal sources as they are lossless as compared to MP3
# Additional servo = laser power adjustments, via mounting a rotation graduated neutral density filter (in documentation) we can vary laser power with rotation of filter.
# We are probably using one of two kinds of servos: SG90 9g, and SG90 9g 360. All PWM generated will have positive (polarity = True) voltage, unless inversion is needed for weird computer soundcards.
# SG90 9g has a 180 degree range, and uses PWM pulses as signals, so the duty cycle of the 50Hz signal gives the ABSOLUTE position of the shaft (motor will try to move to position as long as pulse duration is long enough)
# SG90 9g 360 is a modified version of SG90 9g, and uses PWM signals as SPEED indicators, where DURATION and SPEED will determine the precise RELATIVE movement from any position.

# Duty cycle ratios of interest for the servos for 50Hz signal:
# SG90 9g -> 0.15, 0.1, 0.05
# SG90 9g 360 -> 0.075 (static), 0.080 (minimum for movement in one direction), 0.070 (minimum for movement in the other)

# Sound player module fallback is ffmpeg, but for windows systems it is better to install PYAUDIO, since it does not need to access restricted folders to generate a temporary wav file for playing.

# To install pyaudio, some helper packages are needed first: libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg. Hopefully this means it plays the audio file created in situ before the entire Pulsegen class destructs after each audio command. Wholesome, organic, grass-fed audio solution...

# For playing saved .wav files, we should use python sounddevices to choose the output device first

# Made 2019, Wu Mingsong, Sun Yudong
# mingsongwu [at] outlook [dot] sg, sunyudong [at] outlook [dot] sg,

###
from ctypes import *
from contextlib import contextmanager
import time
from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.playback import play


## removing buggy/useless ALSA pyaudio errors. Does not affect audio output
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def noALSAerror():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
##

class Pulsegen(SignalGenerator):

    PANLEFT = -1
    PANRIGHT = 1

    def __init__(self, duty, polarity = True, freq = 50, duration = 400, pan = -1, **kwargs):
        super().__init__(**kwargs)
        self.freq = freq
        self.duty = duty
        self.polarity = polarity
        self.duration = duration

        ## pan function is volume equaliser: -1 = 100% left, 1 = 100% right
        self.pan = pan

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
        ## pan function is volume equaliser: -1 = 100% left, 1 = 100% right
        sound_segment = sound_segment.pan(self.pan)
        ## setting channels instead is possible, but using stereo output effectively sends mono signal through both channel contacts = stereo output
        #sound_segment = sound_segment.set_channels(1)
        with noALSAerror():
            play(sound_segment)

    def setPan(self, pan):
        self.pan = pan

    def __enter__(self):
        print('\nPulse generator initialising...done\n')
        return self

    def __exit__(self, e_type, e_val, traceback):
        print('\nPulse generator self destructing...done')



class Shutter():
    LEFTCH = -1
    RIGHTCH = 1

    def __init__(self, absoluteMode = False, channel = -1):
        print('\n\nABSOLUTE MODE IS', absoluteMode,'\n')

        self.channel = channel

        print('Channel: ', self.human_channel)

        self.absoluteMode = absoluteMode
        self.homeclose() if not self.absoluteMode else self.close()
        self.isOpen = False

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

    # This is the "over extended" range of 180 degree servo (>180 degrees). Reserved for closed state, where 180 degrees would be open, ready for 180-0 degrees scanning
    def close(self):
        self.absolute(0.15) if self.absoluteMode else self.absolute(0.09, duration = 100)
        print("Closing Shutter")
        self.isOpen = False
        return True

    def open(self):
        self.absolute(0.1) if self.absoluteMode else self.absolute(0.06, duration = 100)
        print("Opening Shutter")
        self.isOpen = True
        return True

    # This is for the continuous rotation servo motor shutters. Provides a homing function: motor rotates untill axle hits a physical block where it will stall temporarily. It then rotates in the other direction to closed position.
    def homeclose(self):
        self.absolute(0.085, duration = 1400)
        time.sleep(1)
        self.absolute(0.06, duration = 300)
        return True

# incremental step scan from one position to another for ND filter rotation control.
# as convention, lets take position 0 (0.15 duty) as closed, position 1 - position n as the increments from 180 degrees to 0.
    def scan(self, p1, p2):
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
    with Shutter(channel = Shutter.LEFTCH, absoluteMode = True) as s:
        print("\n\nUse s as Shutter()\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

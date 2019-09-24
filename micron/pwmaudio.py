#!/usr/bin/env python3

# Python primary Helper to generate PWM audio signals to control a servos

# Current setup involves sending a mono audio PWM signal from the left (or right) channel to control a servo
# We use a USB soundcard/default audio jack to output audio waveform, but since it is usually 2V peak DC, we need an Op-Amp circuit to boost to ~5V
# Please check documentation for USB powered circuit powering servo and op amp circuit

# WAV files are favoured as signal sources as they are lossless as compared to MP3

# Sound player module fallback is ffmpeg, but for windows systems it is better to install PYAUDIO, since it does not need to access restricted folders to generate a temporary wav file for playing.

# To install pyaudio, some helper packages are needed first: libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg. Hopefully this means it plays the audio file created in situ before the entire Pulsegen class destructs after each audio command. Wholesome, organic, grass-fed audio solution...

# For playing saved .wav files, we should use python sounddevices to choose the output device first

# Made 2019, Wu Mingsong
# mingsongwu [at] outlook [dot] sg

###
from ctypes import *
from contextlib import contextmanager
import time
from pydub import AudioSegment
from pydub.generators import SignalGenerator
# from pydub.playback import play
from extraFunctions import play

import os, sys

SHOWERROR = False


## removing buggy/useless ALSA pyaudio errors. Does not affect audio output.
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def noALSAerror():
    if not SHOWERROR:
        # stackoverflow.com/a/36966379
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        os.close(devnull)

        try:
            yield
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
    else:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
##

class Pulsegen(SignalGenerator):

    PANLEFT = -1
    PANRIGHT = 1

    def __init__(self, duty, polarity = True, freq = 51, duration = 400, pan = -1, **kwargs):
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
        # print('\nPulse generator initialising...done\n')
        return self

    def __exit__(self, e_type, e_val, traceback):
        # print('\nPulse generator self destructing...done')
        pass

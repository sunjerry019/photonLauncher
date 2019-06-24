#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.generators import Sine
from pydub.playback import play
import random2

c3, c3sharp, d3, d3sharp, e3, f3, f3sharp, g3, g3sharp, a3, a3sharp, b3, c4, c4sharp, d4, d4sharp, e4, f4, f4sharp, g4, g4sharp, a4, a4sharp, b4, c5, c5sharp, d5, d5sharp, e5, f5, f5sharp, g5, g5sharp, a5, a5sharp, b5, c6, c6sharp, d6, d6sharp, e6 =  130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51

C2majbasschord = [130.81, 164.81, 82.41, 98.00, 130.81]
Cpent = [c3, d3, e3, g3, a3, c4, d4, e4, g4, a4, c5, d5, e5, g5, a5, c6, d6, e6]
Cblues = [c3, d3sharp, f3, f3sharp, g3, a3sharp, c4, d4sharp, f4, f4sharp, g4, a4sharp, c5, d5sharp, f5, f5sharp, g5, a5sharp, c6, d6sharp]


# the most basic melody with pentatonics scale should have: tempo, rhythmic forms (triplets, quavers, rests, etc), repetition, where the last 3 can be done randomly within the score.

# triplet riff for testing. works pretty well.
sound = Sine(freq = c4).to_audio_segment(duration=270/3)+Sine(freq = d4).to_audio_segment(duration=270/3)+Sine(freq = e4).to_audio_segment(duration=270/3)

for x in range(25):
    n = random2.randint(0,14)
    #allegretto speed
    sound += Sine(freq = Cpent[n]).to_audio_segment(duration=270)
    if x % 8 == 0:
        sound += sound

play(sound)



























#

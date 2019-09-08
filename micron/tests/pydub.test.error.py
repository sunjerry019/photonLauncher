#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.playback import play

A = AudioSegment.from_mp3("test.mp3")  # perhaps 3 minutes long
B = AudioSegment.from_mp3("test2.mp3") # perhaps a shutdown tone

try:
    play(A)
except KeyboardInterrupt as e:
    pass

play(B)

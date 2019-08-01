#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.generators import Sine
from pydub.playback import play
import random2

# equal tempered standard piano tuning note frequencies
c3, c3sharp, d3, d3sharp, e3, f3, f3sharp, g3, g3sharp, a3, a3sharp, b3, c4, c4sharp, d4, d4sharp, e4, f4, f4sharp, g4, g4sharp, a4, a4sharp, b4, c5, c5sharp, d5, d5sharp, e5, f5, f5sharp, g5, g5sharp, a5, a5sharp, b5, c6, c6sharp, d6, d6sharp, e6 =  130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51

# 15 notes
Cpent = [c3, d3, e3, g3, a3, c4, d4, e4, g4, a4, c5, d5, e5, g5, a5]
# 18 notes
Cblues = [c3, d3sharp, f3, f3sharp, g3, a3sharp, c4, d4sharp, f4, f4sharp, g4, a4sharp, c5, d5sharp, f5, f5sharp, g5, a5sharp]


# the most basic melody with pentatonics scale should have: tempo, rhythmic forms (triplets, quavers, rests, etc), ornaments, repetition, where the last 4 can be done randomly within the score.

# timbre, stacking harmonics together
def marimba(note, duration):

    #sound = Sine(freq = note-5).to_audio_segment(duration = duration/5).overlay(Sine(freq = (note-5)*4).to_audio_segment(duration = duration/5, volume = -35), crossfade = crossfd).overlay(Sine(freq = (note-5)*10).to_audio_segment(duration = duration/5, volume = -40), crossfade = crossfd)

    sound = (Sine(freq = note).to_audio_segment(duration = duration)).overlay(Sine(freq = note*4).to_audio_segment(duration = duration, volume = -35)).overlay(Sine(freq = note*10).to_audio_segment(duration = duration, volume = -40))

    return sound

def pure(note, duration):
    sound = Sine(freq = note).to_audio_segment(duration = duration)
    return sound

# lento
tempo = 300
# around 30 is good
probability_unity = 40
scale = Cpent
repetition_rate = 13
tonegen = marimba
sound = tonegen(0,tempo)
crossfd = 30

for x in range(30):

    # random rhythm class selector
    r = random2.randint(0,probability_unity)

    # random origin note selector
    n = random2.randint(0,int(len(scale)) - 1)

    # 0th class: single notes
    if r < probability_unity - 12:
        sound = sound.append(tonegen(scale[n],tempo), crossfade = crossfd)

    # 1st class: ascending triplets
    elif r == probability_unity - 0:
        if n >= int(len(scale)) - 2:
            sound = sound.append(tonegen(scale[n-2], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n], tempo / 3), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+2], tempo / 3), crossfade = crossfd)

    # 2nd class: descending triplets
    elif r == probability_unity - 1:
        if n <= 1:
            sound = sound.append(tonegen(scale[n+2], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n], tempo / 3), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-2], tempo / 3), crossfade = crossfd)

    # 3rd class: standard turns
    elif r == probability_unity - 2:
        if n == 0:
            sound = sound.append(tonegen(scale[n+1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1], tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+2], tempo / 3), crossfade = crossfd)
        elif n == int(len(scale)) - 1:
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)

    # 4th class: reverse turns
    elif r == probability_unity - 3:
        if n == 0:
            sound = sound.append(tonegen(scale[n+2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
        elif n == int(len(scale)) - 1:
            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)


    # 5th class: ascending acciacaturas
    elif r == probability_unity - 4:
        if n == int(len(scale)) - 1:
            sound = sound.append(tonegen(scale[n-1],tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],(tempo *2) / 3), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],(tempo *2) / 3), crossfade = crossfd)

    # 6th class: descending acciacaturas
    elif r == probability_unity - 5:
        if n == 0:
            sound = sound.append(tonegen(scale[n+1],tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],(tempo *2) / 3), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 3), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],(tempo *2) / 3), crossfade = crossfd)

    # 7th class: ascending scales
    elif r == probability_unity - 6:
        for s in range(0,int(len(scale))):
            sound = sound.append(tonegen(scale[s],tempo / 2), crossfade = crossfd)

    # 8th class: descending scales
    elif r == probability_unity - 7:
        for s in range(int(len(scale)),-1):
            sound = sound.append(tonegen(scale[s],tempo / 2), crossfade = crossfd)

    # 9th class: pause
    elif r == probability_unity - 8:
        sound = sound.append(tonegen(0,tempo), crossfade = crossfd)

    # 10th class: ascending in broken thirds
    elif r == probability_unity - 9:
        if n >= int(len(scale)) - 5:
            sound = sound.append(tonegen(scale[n-5],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-4],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)

            sound = sound.append(tonegen(scale[n-3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)

        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+3],tempo / 2), crossfade = crossfd)

            sound = sound.append(tonegen(scale[n+2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+4],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+5],tempo / 2), crossfade = crossfd)

    # 11th class: descending in broken thirds
    elif r == probability_unity - 10:
        if n < 5:
            sound = sound.append(tonegen(scale[n+5],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+4],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+2],tempo / 2), crossfade = crossfd)

            sound = sound.append(tonegen(scale[n+3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)

        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-3],tempo / 2), crossfade = crossfd)

            sound = sound.append(tonegen(scale[n-2],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-4],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-3],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-5],tempo / 2), crossfade = crossfd)

    # 11th class: slow upper trill
    elif r == probability_unity - 11:
        if n == int(len(scale)) - 1:
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)

    # 12th class: slow lower trill
    elif r == probability_unity - 12:
        if n == 0:
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n+1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
        else:
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n],tempo / 2), crossfade = crossfd)
            sound = sound.append(tonegen(scale[n-1],tempo / 2), crossfade = crossfd)

    # Provides stacking repitition for *some* structure
    if x % repetition_rate == 0 and x > 0:
        sound = sound.append(sound)

play(sound)

# hi

























#

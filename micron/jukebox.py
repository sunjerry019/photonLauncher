#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.generators import SignalGenerator
from pydub.generators import Sine
from pydub.playback import play
import random2

from pwmaudio import noALSAerror


# the most basic melody with pentatonics SCALE should have: TIMBRE, TEMPO, RHYTHMic forms (triplets, quavers, rests, etc), ornaments, repetition, where the last 4 can be done randomly within the score.

# by default, this music is in duple time.


class JukeBox():

    def __init__(self, tempo = 300, length = 40, scale = 'cpent', playmusic = False):
        self.scale(scale = scale)
        self.tempo = tempo
        self.length = length
        print("Loading Melodies")
        self.melodygen(tempo = self.tempo, length = self.length)

        if playmusic:
            self.playmusic()

    def melodygen(self, tempo, length, profile = 'random', p_unity = 40, repetition_rate = 13, crossfd = 30):

        self.sound = self.notegen(0,tempo)
        rhythmbox = ['single', 'up_triplet', 'down_triplet', 'turn', 'reverse_turn', 'up_accia', 'down_accia', 'up_scale', 'down_scale', 'up_thirds', 'down_thirds', 'lower_thrill_slow','upper_thrill_slow']

        if profile == 'random':
            for x in range(length):

                # random rhythm class selector
                r = random2.randint(0,p_unity)
                # random origin note selector
                n = random2.randint(0,int(len(self.scale)) - 1)

                if r >= len(rhythmbox):
                    self.rhythmgen(rclass = 'single', note_index = n, tempo = tempo, crossfd = crossfd)
                else:
                    self.rhythmgen(rclass = rhythmbox[r], note_index = n, tempo = tempo, crossfd = crossfd)

                # Provides stacking repitition for *some* structure
                if x % repetition_rate == 0 and x > 0:
                    self.sound = self.sound.append(self.sound)

        elif profile == 'alarm':
            for k in range(length):
                self.rhythmgen(rclass = 'up_triplet', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'up_triplet', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'pause', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'down_triplet', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'down_triplet', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'pause', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'down_thirds', note_index = 4, tempo = tempo, crossfd = crossfd)
                self.rhythmgen(rclass = 'pause', note_index = 4, tempo = tempo, crossfd = crossfd)
        return self.sound

    def playmusic(self):
        print('Now playing: Debussys greatest hits')
        with noALSAerror():
            play(self.sound)

    def notegen(self, note, duration, timbre = 'marimba'):

    #sound = Sine(freq = note-5).to_audio_segment(duration = duration/5).overlay(Sine(freq = (note-5)*4).to_audio_segment(duration = duration/5, volume = -35), crossfade = crossfd).overlay(Sine(freq = (note-5)*10).to_audio_segment(duration = duration/5, volume = -40), crossfade = crossfd)
        if timbre == 'marimba':

            self.sound = (Sine(freq = note).to_audio_segment(duration = duration)).overlay(Sine(freq = note*4).to_audio_segment(duration = duration, volume = -35)).overlay(Sine(freq = note*10).to_audio_segment(duration = duration, volume = -40))

        elif timbre == 'pure':
            self.sound = Sine(freq = note).to_audio_segment(duration = duration)

        return self.sound

    def scale(self, scale):
        # equal tempered standard piano tuning note frequencies
        c3, c3sharp, d3, d3sharp, e3, f3, f3sharp, g3, g3sharp, a3, a3sharp, b3, c4, c4sharp, d4, d4sharp, e4, f4, f4sharp, g4, g4sharp, a4, a4sharp, b4, c5, c5sharp, d5, d5sharp, e5, f5, f5sharp, g5, g5sharp, a5, a5sharp, b5, c6, c6sharp, d6, d6sharp, e6 =  130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51

        if scale == 'cpent':
        # 15 notes
            self.scale = [c3, d3, e3, g3, a3, c4, d4, e4, g4, a4, c5, d5, e5, g5, a5]

        elif scale == 'cblues':
        # 18 notes
            self.scale = [c3, d3sharp, f3, f3sharp, g3, a3sharp, c4, d4sharp, f4, f4sharp, g4, a4sharp, c5, d5sharp, f5, f5sharp, g5, a5sharp]

    def rhythmgen(self, rclass, note_index, tempo, crossfd = 30):

        if rclass == 'single':
            self.sound = self.sound.append(self.notegen(self.scale[note_index] , tempo), crossfade = crossfd)

        elif rclass == 'up_triplet':
            if note_index >= int(len(self.scale)) - 2:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index], tempo / 3), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2], tempo / 3), crossfade = crossfd)

        elif rclass == 'down_triplet':
            if note_index <= 1:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index], tempo / 3), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2], tempo / 3), crossfade = crossfd)

        elif rclass == 'turn':
            if note_index == 0:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1], tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2], tempo / 3), crossfade = crossfd)
            elif note_index == int(len(self.scale)) - 1:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)

        elif rclass == 'reverse_turn':
            if note_index == 0:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
            elif note_index == int(len(self.scale)) - 1:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)

        elif rclass == 'up_accia':
            if note_index == int(len(self.scale)) - 1:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],(tempo *2) / 3), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],(tempo *2) / 3), crossfade = crossfd)

        elif rclass == 'down_accia':
            if note_index == 0:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],(tempo *2) / 3), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 3), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],(tempo *2) / 3), crossfade = crossfd)

        elif rclass == 'up_scale':
            for s in range(0,int(len(self.scale))):
                self.sound = self.sound.append(self.notegen(self.scale[s],tempo / 2), crossfade = crossfd)

        elif rclass == 'down_scale':
            for s in range(int(len(self.scale)),-1):
                self.sound = self.sound.append(self.notegen(self.scale[s],tempo / 2), crossfade = crossfd)

        # 10th class: ascending in broken thirds
        elif rclass == 'up_thirds':
            if note_index >= int(len(self.scale)) - 5:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-5],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-3],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-4],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2],tempo / 2), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+3],tempo / 2), crossfade = crossfd)

                self.sound = self.sound.append(self.notegen(self.scale[note_index+2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+4],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+3],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+5],tempo / 2), crossfade = crossfd)

        elif rclass == 'down_thirds':
            if note_index < 5:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+5],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+3],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+4],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2],tempo / 2), crossfade = crossfd)

                self.sound = self.sound.append(self.notegen(self.scale[note_index+3],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)

            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-3],tempo / 2), crossfade = crossfd)

                self.sound = self.sound.append(self.notegen(self.scale[note_index-2],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-4],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-3],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-5],tempo / 2), crossfade = crossfd)

        elif rclass == 'upper_thrill_slow':
            if note_index == int(len(self.scale)) - 1:
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)

        elif rclass == 'lower_thrill_slow':
            if note_index == 0:
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index+1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
            else:
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index],tempo / 2), crossfade = crossfd)
                self.sound = self.sound.append(self.notegen(self.scale[note_index-1],tempo / 2), crossfade = crossfd)

        elif rclass == 'pause':
            self.sound = self.sound.append(self.notegen(0,tempo*4), crossfade = crossfd)

        return self.sound


    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

if __name__ == '__main__':
    with JukeBox() as juke:
        print("\n\nUse juke as JukeBox()\n\n")
        # import pdb; pdb.set_trace()
        import code; code.interact(local=locals())

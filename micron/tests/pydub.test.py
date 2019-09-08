#!/usr/bin/env python3

from pydub import AudioSegment

def play(seg):
    import pyaudio
    from pydub.utils import make_chunks

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)

    try:
        # break audio into half-second chunks (to allows keyboard interrupts)
        i = 0
        for chunk in make_chunks(seg, 500):
            print("Chunking :", i, end="\r")
            stream.write(chunk._data)
            i += 1
    # except:
    #     # We catch ALL exceptions and interrupts and raise it
    #     print("interrupted")
    #     raise
    finally:
        print("CLEANING UP")
        stream.stop_stream()
        stream.close()

        p.terminate()


song = AudioSegment.from_mp3("test.mp3")

try:
    play(song)
except:
    pass

print("Ok")
play(song)

# REFERENCES:
# https://www.oipapio.com/question-1169116
# https://github.com/jiaaro/pydub/blob/master/pydub/playback.py

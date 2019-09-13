#!/usr/bin/env python3

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pydub import AudioSegment
from pydub.playback import play

# https://stackoverflow.com/a/43727046
def main():
    song = AudioSegment.from_mp3("beep.mp3")

    global sess, vol

    play(song)
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        # if session.Process:
        #   print(session.Process.name())
        if session.Process and session.Process.name() == "python.exe":
            sess = session
            vol = sess._ctl.QueryInterface(ISimpleAudioVolume)
            print("volume.GetMasterVolume(): %s" % vol.GetMasterVolume())
            vol.SetMasterVolume(0, None)

    play(song)
    vol.SetMasterVolume(1, None)
    play(song)



if __name__ == "__main__":
    main()
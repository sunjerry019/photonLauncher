#!/usr/bin/env python3

import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

from PyQt5 import QtCore, QtGui, QtWidgets

def moveToCentre(QtObj, host = None):
    # https://stackoverflow.com/a/42326134/3211506
    if host is None:
        host = QtObj.parentWidget()

    if host:
        hostRect = host.frameGeometry()
        QtObj.move(hostRect.center() - QtObj.rect().center())
    else:
        screenGeometry = QtWidgets.QDesktopWidget().availableGeometry()
        try:
            ObjWidth = QtObj.width()
            ObjHeight = QtObj.height()
        except TypeError as e:
            ObjWidth = QtObj.width
            ObjHeight = QtObj.height

        _x = (screenGeometry.width() - ObjWidth) / 2;
        _y = (screenGeometry.height() - ObjHeight) / 2;
        QtObj.move(_x, _y);

# Rewritten play function
# We enforce PyAudio
# https://github.com/jiaaro/pydub/pull/421
# NOTE: REMOVE IF PR IS MERGED AND DEPLOYED

from pydub.utils import make_chunks
from pydub.playback import play as pydub_play

def _play_with_pyaudio(seg):
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)

    # Just in case there were any exceptions/interrupts, we release the resource
    # So as not to raise OSError: Device Unavailable should play() be used again
    try:
        # break audio into half-second chunks (to allows keyboard interrupts)
        for chunk in make_chunks(seg, 500):
            stream.write(chunk._data)
    finally:
        stream.stop_stream()
        stream.close()

        p.terminate()

def play(audio_segment):
    try:
        _play_with_pyaudio(audio_segment)
        return
    except ImportError:
        pass
    else:
        return

    pydub_play(audio_segment)



# https://stackoverflow.com/a/325528/3211506
import threading, time, ctypes, inspect

def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class ThreadWithExc(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        if not hasattr(self, 'my_tid'):
            self.my_tid = self._get_my_tid()
        _async_raise( self.my_tid, exctype )

    def terminate(self):
        if self.isAlive() and (not hasattr(self, 'terminateRequested') or not self.terminateRequested):
            self.terminateRequested = True
            self.raiseExc(SystemExit)
            self.join()

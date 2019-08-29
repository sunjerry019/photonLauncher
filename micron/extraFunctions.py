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

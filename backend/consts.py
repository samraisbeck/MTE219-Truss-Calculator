# File to store constants in
import os
from PySide import QtGui

# Component and truss constants
beamUltNorm = 17100000/1.5 #safety factor
beamUltShear = 930000 #originally 2 MPa
pinUltShear = 23000000
pinMaxM = 0.368
dowelDiam = 0.003175
genThick = 0.0032 #general thickness of the balsa wood
E = 3600000000
pi = 3.14159265359
memDens = 133
jointDens = 650

# Type of popup
INFO = 0
WARN = 1
ERR = 2
YES_NO = 3

# File saving outcomes
SAVED = 0
NO_SAVE = 1
SAVE_CANCEL = 2

# General title font
titleFont = QtGui.QFont()
titleFont.setBold(True)
titleFont.setPointSize(15)


alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
LOGGER = 'TrussCalc.SRaisbeck'

# Group 24 - MODS Project: Failure Analysis
# Based on theoretical/experimental values
"""
By Sam Raisbeck - Updated June 16, 2017

This program is meant for calculating the failure modes and corresponding
loads for a crane design (MTE 219 @ UW). Currently, you must enter in the values
below for member length, width, etc. Soon a GUI will be added making this
easier.
It's easy to create members, just add in the correct values. To create joints,
the members must be added to the joints such that they are in order of
appearance when viewing the structure from the side. It does not matter which
side it is viewed from, just stay consistent. This is so that pin-shear
calculations can be done easily.
Currently there is no feature implemented to do a pin-shear for more than 3-
member joints. This is because you would need to know the geometry with angles.
It can be done, it just would add more attributes to the members, and also would
require consistency with reference angles and stuff like that.

***Update July 5 2017
Added a very simple GUI structure, not yet functional for adding custom
members, but the general structure is there. The only thing to do is to
basically get the AddMember button working, which won't be hard...but the
joints might take some tricky GUI work. I'm thinking of adding in just a list
of members that you can select for each joint.

"""

# Note: every value is in SI (kg, N, m, Pa etc)
from backend.consts import *
from backend.structAnalysis import StructAnalysis
from backend.loadAndSave import LoadAndSave
from backend.components import Member, Joint
import os, sys
from PySide import QtGui, QtCore

RESULTS = ''

class TrussCalc(QtGui.QMainWindow):
    def __init__(self):
        super(TrussCalc, self).__init__()
        self.memsListNew = []
        self.jointsListNew = []
        self.specs = ['Name', 'H-H Length', 'Width', 'Thickness', 'Force', 'Hole-Edge Dist', 'Hole Support(s)', 'Compression', 'Box Beam']
        self._initUI()

    def _initUI(self):
        self.mainGrid = QtGui.QGridLayout()
        self.mainGrid.addWidget(self._trussSpecs(), 0, 0)
        self.mainGrid.addWidget(self._actionControl(), 1, 0)
        self.resize(500,250)
        self.show()
        Qw = QtGui.QWidget()
        Qw.setLayout(self.mainGrid)
        self.setCentralWidget(Qw)
        self.setWindowTitle('Truss Failure Analysis - Sam Raisbeck 2017')

    def _trussSpecs(self):
        Qw = QtGui.QWidget()
        grid = QtGui.QGridLayout()

        for i in range(len(self.specs)):
            mid = len(self.specs)/2
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(QtGui.QLabel(self.specs[i], parent=self))
            edit = QtGui.QLineEdit()
            edit.setPlaceholderText(self.specs[i]+'...')
            hbox.addWidget(edit)
            if i <= mid:
                grid.addLayout(hbox, i, 0)
            else:
                grid.addLayout(hbox, i%mid, 1)
        Qw.setLayout(grid)
        return Qw


    def _actionControl(self):
        Qw = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        buttonAddMember = QtGui.QPushButton('Add Member', parent=self)
        layout.addWidget(buttonAddMember)
        buttonAddMember.clicked.connect(self.addMember)
        buttonCalculate = QtGui.QPushButton('Calculate!', parent=self)
        layout.addWidget(buttonCalculate)
        buttonCalculate.clicked.connect(self.calculate)

        Qw.setLayout(layout)
        return Qw

    def addMember(self):
        pass

    def calculate(self):
        if len(self.memsListNew) == 0:
            self.memsListNew = memsList
            self.jointsListNew = jointsList
            print 'here'
        RESULTS = StructAnalysis(self.memsListNew, self.jointsListNew).calcAll()
        print RESULTS



# Member(name, hole-hole length, endWidth, thickness, compression bool,
#        internal force, hole distance from edge, boxBeam?, holeSupport)
AD = Member('AD', 0.3, 0.0112, 0.0112, True, 2, 0.004, box = True)
CD = Member('CD', 0.2062, 0.00838, 0.0032, False, 2.062, 0.01, holeSupport = 3)
AC = Member('AC', 0.1118, 0.0075, 0.0067, True, 1.118, 0.004)
AB = Member('AB', 0.05, 0.00818, 0.0032, False, 0.5, 0.009)
BC = Member('BC', 0.1, 0.00838, 0.0032, False, 3, 0.01, holeSupport = 3)
Rc = Member('Rc', 0, 0, 0, False, 3, 0)
Ra = Member('Ra', 0, 0, 0, True, 3.041, 0)
P = Member('P', 0, 0, 0, False, 1, 0)

A = Joint('A', [Rc, AD, AC, AB])
B = Joint('B', [BC, Ra, AB])
C = Joint('C', [CD, BC, AC])
D = Joint('D', [CD, AD, P])

memsList = [AB, AC, CD, AD, BC, Rc, Ra, P]
jointsList = [A, B, C, D]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = TrussCalc()
    app.exec_()
    save = raw_input("Would you like to save your results? (Y/N): ")
    if (save == 'y') or (save == 'Y'):
        name = raw_input('Enter a name for this design: ')
        filename = name
        directory = mainDir+os.sep+'designs'
        fileExists = True
        fileCopy = 0
        while os.path.isfile(directory+os.sep+filename+'.txt'):
            fileCopy += 1
            filename = name+'('+str(fileCopy)+')'
        fileHandler = LoadAndSave(directory)
        fileHandler.save(filename, RESULTS, mw.memsListNew, mw.jointsListNew)

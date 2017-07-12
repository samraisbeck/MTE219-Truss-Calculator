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
from backend import colorCmdHandler
import os, sys, math
from PySide import QtGui, QtCore
from widgets.popUps import PopUp
from widgets.widgetHelp import WidgetHelp
from widgets.widgetDevelopment import WidgetDevelopment
from widgets.widgetResults import WidgetResults
import logging

logger = logging.getLogger(LOGGER)

RESULTS = ''

class TrussCalc(QtGui.QMainWindow):
    def __init__(self):
        super(TrussCalc, self).__init__()
        self.memsListNew = []
        self.jointsListNew = []
        self._mIndex = -1
        self._jIndex = -1
        self.specs = ['Name', 'H-H Length', 'Width', 'Thickness', 'Force', 'Hole-Edge Dist', 'Hole Support(s)', 'Compression', 'Box Beam']
        self.tips = ['Name should be two letters corresponding to the end joints (i.e AD)', 'Distance between the centers of the holes on each end', 'Width of the member',\
                     'Thickness of the member', 'Force relative to the applied load', 'Distance from the center of the hole to the end edge of the member', \
                     'Number of added hole supports (this is 0 if none are glued on)', 'Is the member under compression?', 'Is the member a box beam?']
        self.specInfo = []
        self.jointInfo = []
        self.selectedJoints = []
        self.createJointButton = None
        self.creatingJoint = False
        self.specGrid = None
        self.fName = 'unknown'
        self.askSave = False
        self._initLogger()
        self._initUI()
# Set up mIndex with decorators so that as soon as it's changed, we can update
# the seek buttons, rather than having them update all over the place.
    @property
    def mIndex(self): return self._mIndex

    @mIndex.setter
    def mIndex(self, val):
        self._mIndex = val
        self.buttonSeekRight.setEnabled(self._mIndex < len(self.memsListNew)-1)
        self.buttonSeekLeft.setEnabled(self._mIndex > 0)
        self.createJointButton.setEnabled(self._mIndex > 0)
        # We can use the mIndex setter function to also update the info
        # on the other tab.
        self.widgetResults.updateInfo(self.memsListNew, self.jointsListNew)

    @property
    def jIndex(self): return self._jIndex

    @jIndex.setter
    def jIndex(self, val):
        self._jIndex = val
        self.clearJointsButton.setEnabled(self._jIndex >= 0)
        # We can use the jIndex setter function to also update the info
        # on the other tab.
        self.widgetResults.updateInfo(self.memsListNew, self.jointsListNew)

    def _initLogger(self):
        root_logger = logging.getLogger()
        stderr_log_handler = colorCmdHandler.ColorStreamHandler()
        root_logger.addHandler(stderr_log_handler)

        formatter = logging.Formatter('\n%(levelname)-s message from %(filename)s - %(message)s\n')
        root_logger.setLevel(logging.DEBUG)
        stderr_log_handler.setFormatter(formatter)
        stderr_log_handler.setLevel(logging.INFO)

    def _initUI(self):
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self._mainTab(), 'Designer')
        self.tabs.addTab(self._resultsTab(), 'Components/Results')
        self.resize(500,250)
        self.show()
        Qw = QtGui.QWidget()
        self.setCentralWidget(self.tabs)
        self.setWindowTitle('Truss Failure Analysis - Sam Raisbeck 2017')
        self.updateStatus('Add some members.')
        self._createToolbar()

    def _mainTab(self):
        self.mainGrid = QtGui.QGridLayout()
        title1 = QtGui.QLabel('Member Specifications', parent=self)
        title1.setFont(titleFont)
        title2 = QtGui.QLabel('Joint Specifications', parent=self)
        title2.setFont(titleFont)
        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.VLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.mainGrid.addWidget(title1, 0, 0, alignment=QtCore.Qt.AlignHCenter)
        self.mainGrid.addWidget(separator, 0, 1, 2, 1)
        self.mainGrid.addWidget(title2, 0, 2, alignment=QtCore.Qt.AlignHCenter)
        self.mainGrid.addWidget(self._trussSpecs(), 1, 0)
        self.mainGrid.addWidget(self._jointSpecs(), 1, 2)
        self.mainGrid.addWidget(self._actionControl(), 2, 0, 1, 3)
        Qw = QtGui.QWidget()
        Qw.setLayout(self.mainGrid)
        return Qw

    def _resultsTab(self):
        self.widgetResults = WidgetResults(parent=None)
        return self.widgetResults

    def _trussSpecs(self):
        Qw = QtGui.QWidget()
        self.specGrid = QtGui.QGridLayout()
        mid = len(self.specs)/2
        for i in range(len(self.specs)):
            hbox = QtGui.QHBoxLayout()
            if self.specs[i] == 'Compression' or self.specs[i] == 'Box Beam':
                checkbox = QtGui.QCheckBox(self.specs[i], parent=self)
                checkbox.setToolTip(self.tips[i])
                self.specInfo.append(checkbox)
                hbox.addWidget(checkbox)
                #hbox.setAlignment(checkbox, QtCore.Qt.AlignHCenter)
            else:
                hbox.addWidget(QtGui.QLabel(self.specs[i], parent=self))
                edit = QtGui.QLineEdit()
                self.specInfo.append(edit)
                edit.setPlaceholderText(self.specs[i]+'...')
                edit.setToolTip(self.tips[i])
                hbox.addWidget(edit)
            if i <= mid:
                self.specGrid.addLayout(hbox, i, 0)
            else:
                self.specGrid.addLayout(hbox, i%(mid+1), 1)
        memButtons1, memButtons2 = self._memButtons()
        self.specGrid.addLayout(memButtons1, len(self.specs)%(mid+1), 1)
        self.specGrid.addLayout(memButtons2, len(self.specs)%(mid+1)+1, 0, 1, 2)
        Qw.setLayout(self.specGrid)
        return Qw

    def _memButtons(self):
        smallBox1 = QtGui.QHBoxLayout()
        buttonAddMember = QtGui.QPushButton('Add Member', parent=self)
        smallBox1.addWidget(buttonAddMember)
        buttonAddMember.clicked.connect(self.addMember)
        buttonFixMember = QtGui.QPushButton('Edit Member', parent=self)
        smallBox1.addWidget(buttonFixMember)
        buttonFixMember.clicked.connect(self.fixMember)

        smallBox2 = QtGui.QHBoxLayout()
        self.buttonSeekLeft = QtGui.QPushButton('Previous', parent=self)
        self.buttonSeekLeft.setEnabled(False)
        smallBox2.addWidget(self.buttonSeekLeft)
        self.buttonSeekLeft.clicked.connect(self.seekLeft)
        self.buttonSeekRight = QtGui.QPushButton('Next', parent=self)
        self.buttonSeekRight.setEnabled(False)
        smallBox2.addWidget(self.buttonSeekRight)
        self.buttonSeekRight.clicked.connect(self.seekRight)

        return smallBox1, smallBox2

    def _jointSpecs(self):
        Qw = QtGui.QWidget()
        grid = QtGui.QGridLayout()
        self.jointGrid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel('Name', parent=self),0,0)
        edit = QtGui.QLineEdit()
        edit.setPlaceholderText('Joint name...')
        self.jointInfo.append(edit)
        grid.addWidget(edit, 0, 1)
        jointButtons1, jointButtons2 = self._jointButtons()
        grid.addWidget(jointButtons1, 0, 2)
        grid.addWidget(jointButtons2, 0, 3)
        #self.jointGrid.addWidget(QtGui.QLabel('Available Members', parent=self), 1, 0, 1, 2)
        for i in range(4):
            for j in range(5):
                memButton = QtGui.QPushButton('  ', parent=self)
                memButton.setEnabled(False)
                self.connect(memButton, QtCore.SIGNAL('pressed()'), self.appendJoint)
                self.jointGrid.addWidget(memButton, i, j)
                self.jointInfo.append(memButton)
        grid.addLayout(self.jointGrid, 1, 0, 1, 4)
        Qw.setLayout(grid)
        return Qw

    def _jointButtons(self):
        self.createJointButton = QtGui.QPushButton('Begin Joint Creation', parent=self)
        self.createJointButton.setMinimumWidth(round(0.2*self.width()))
        self.createJointButton.clicked.connect(self.jointCreationClicked)
        self.createJointButton.setEnabled(False)

        self.clearJointsButton = QtGui.QPushButton('Clear Joints', parent=self)
        self.clearJointsButton.setMinimumWidth(round(0.15*self.width()))
        self.clearJointsButton.clicked.connect(self.clearJoints)
        self.clearJointsButton.setEnabled(False)

        return self.createJointButton, self.clearJointsButton

    def _actionControl(self):
        Qw = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        buttonViewComponents = QtGui.QPushButton('View Components', parent=self)
        layout.addWidget(buttonViewComponents)
        buttonViewComponents.clicked.connect(self.viewComponents)
        buttonCalculate = QtGui.QPushButton('Calculate!', parent=self)
        layout.addWidget(buttonCalculate)
        buttonCalculate.clicked.connect(self.calculate)

        Qw.setLayout(layout)
        return Qw

    def _createToolbar(self):
        m = QtGui.QMenu('File', parent=self)
        option = QtGui.QAction('Save', m)
        option.setShortcut('Ctrl+S')
        option.setStatusTip('Save the design and results as a text file.')
        option.triggered.connect(self.saveDesign)
        m.addAction(option)

        option = QtGui.QAction('Load', m)
        option.setShortcut('Ctrl+L')
        option.setStatusTip('Load a design and its results from a previously saved file.')
        option.triggered.connect(self.loadDesign)
        m.addAction(option)

        m.addSeparator()

        option = QtGui.QAction('New', m)
        option.setShortcut('Ctrl+N')
        option.setStatusTip('Clear the current design and begin from scratch.')
        option.triggered.connect(self.newDesign)
        m.addAction(option)

        self.menuBar().addMenu(m)

        m = QtGui.QMenu('About', parent=self)
        option = QtGui.QAction('Help', m)
        option.setShortcut('Ctrl+H')
        option.setStatusTip('Basic help.')
        option.triggered.connect(self.showHelp)
        m.addAction(option)

        option = QtGui.QAction('Development', m)
        option.setStatusTip('Basic help.')
        option.triggered.connect(self.showDevelopment)
        m.addAction(option)

        self.menuBar().addMenu(m)

    def saveDesign(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save your file', os.path.dirname(os.path.abspath(__file__))+os.sep+'designs', 'Text Documents (*.txt)')
        if not filename[0] == '':
            try:
                handler = LoadAndSave(os.path.dirname(filename[0]))
                handler.save(filename[0], RESULTS, mw.memsListNew, mw.jointsListNew)
                self.askSave = False
                self.fName = os.path.splitext(os.path.basename(filename[0]))[0]
                logger.info('File saved to '+filename[0])
                return SAVED
            except:
                PopUp('ERROR: Something went wrong while saving.', ERR, self)
                logger.error('Something went wrong while saving.')
                return SAVE_CANCEL
        else:
            logger.warning('Nothing was saved...')
            return SAVE_CANCEL

    def loadDesign(self):
        if self.askSave:
            if self.savePrompt() == SAVE_CANCEL:
                query = PopUp('Nothing was saved, are you sure you want to continue?', YES_NO, self)
                if query.reply == QtGui.QMessageBox.No:
                    return
        loadFile = QtGui.QFileDialog.getOpenFileName(self, 'Select a file to load', os.path.dirname(os.path.abspath(__file__))+os.sep+'designs', 'Text Documents (*.txt)')
        if not loadFile[0] == '':
            try:
                self.fName = os.path.splitext(os.path.basename(loadFile[0]))[0]
                handler = LoadAndSave(os.path.dirname(loadFile[0]))
                loadedMems, loadedJoints = handler.load(loadFile[0])
                self.memsListNew, self.jointsListNew = loadedMems, loadedJoints
                self.mIndex = len(self.memsListNew)-1
                self.jIndex = len(self.jointsListNew)-1
                self.setMemTextBoxes()
                for i in range(len(self.memsListNew)):
                    self.jointInfo[i+1].setText(self.memsListNew[i].n)
                    self.jointInfo[i+1].setEnabled(True)
                for button in self.jointInfo[self.mIndex+2:]:
                    if not button.isEnabled():
                        break
                    button.setEnabled(False)
                    button.setText(' ')
                self.askSave = False
            except:
                PopUp('ERROR: Something went wrong while loading.')
                logger.error('Something went wrong while loading.')
        else:
            logger.warning('Nothing was loaded...')

    def newDesign(self):
        # Empty the lists
        if self.askSave:
            if self.savePrompt() == SAVE_CANCEL:
                query = PopUp('Nothing was saved, are you sure you want to continue?', YES_NO, self)
                if query.reply == QtGui.QMessageBox.No:
                    return
        self.memsListNew = []
        self.jointsListNew = []
        self.jIndex = -1
        self.mIndex = -1
        # Set each textbox and checkbox to blank
        for i in range(len(self.specs)):
            if type(self.specInfo[i]) == QtGui.QLineEdit:
                self.specInfo[i].setText('')
            else:
                self.specInfo[i].setChecked(False)
        # Set joint name textbox to blank, disable and clear member buttons
        self.jointInfo[0].setText('')
        for button in self.jointInfo[1:]:
            if not button.isEnabled():
                break
            button.setText('  ')
            button.setEnabled(False)
        self.fName = 'unknown'

    def showHelp(self):
        WidgetHelp(parent=self)

    def showDevelopment(self):
        WidgetDevelopment(parent=self)

    def savePrompt(self):
        query = PopUp('Design not saved! Do you want to save?', YES_NO, self)
        if query.reply == QtGui.QMessageBox.Yes:
            return self.saveDesign()
        else:
            return NO_SAVE

    def seekLeft(self):
        self.mIndex -= 1
        self.setMemTextBoxes()

    def seekRight(self):
        self.mIndex += 1
        self.setMemTextBoxes()

    def setMemTextBoxes(self):
        member = self.memsListNew[self.mIndex]
        self.specInfo[0].setText(member.n)
        self.specInfo[1].setText(str(member.l))
        self.specInfo[2].setText(str(member.w))
        self.specInfo[3].setText(str(member.t))
        self.specInfo[4].setText(str(member.f))
        self.specInfo[5].setText(str(member.holeDist))
        self.specInfo[6].setText(str(member.holeSup-1))
        if member.comp:
            self.specInfo[7].setChecked(True)
        else:
            self.specInfo[7].setChecked(False)
        if member.isBox:
            self.specInfo[8].setChecked(True)
        else:
            self.specInfo[8].setChecked(False)


    def jointCreationClicked(self):
        if not self.creatingJoint:
            self.creatingJoint = True
            logger.info('Now creating joint...')
            self.createJointButton.setText('Add New Joint')
            self.updateStatus('Select the members on the joint, order matters (see Help).')
        else:
            try:
                if len(self.selectedJoints) < 2:
                    raise
                newJoint = Joint(self.jointInfo[0].text(), self.selectedJoints)
                self.jointsListNew.append(newJoint)
                self.jIndex += 1
                self.askSave = True
                logger.info('Created joint: '+str(newJoint))
            except:
                PopUp('ERROR: Joint must have at least 2 members attached!', ERR, self)
                logger.error('Joint must have at least 2 members attached!')
            for button in self.jointInfo[1:]:
                if button.text() == '  ':
                    break
                elif not button.isEnabled():
                    button.setEnabled(True)
            self.creatingJoint = False
            self.createJointButton.setText('Begin Joint Creation')
            self.selectedJoints = []
            self.updateStatus('Add some members or joints.')
        self.clearJointsButton.setEnabled(not self.creatingJoint)

    def clearJoints(self):
        self.jointsListNew = []
        self.jIndex = -1
        logger.info('List of joints has been cleared.')

    def addMember(self):
        try:
            newMember = Member(self.specInfo[0].text(), float(self.specInfo[1].text()), float(self.specInfo[2].text()),
                               float(self.specInfo[3].text()), self.specInfo[7].isChecked(), float(self.specInfo[4].text()),
                               float(self.specInfo[5].text()), box=self.specInfo[8].isChecked(), holeSupport=int(self.specInfo[6].text()))
            self.memsListNew.append(newMember)
            self.mIndex = len(self.memsListNew)-1
            #Adding the corresponding button for the joint-building tool
            self.jointInfo[self.mIndex+1].setText(newMember.n)
            self.jointInfo[self.mIndex+1].setEnabled(True)
            if len(self.jointsListNew) > 1:
                self.updateStatus('Add some members or joints.')
            self.askSave = True
            logger.info('Added member with data: '+str(newMember))
        except:
            PopUp("ERROR: Check the entries you have made, they should all be numbers, except the name...", ERR, self)
            logger.error("Check the entries you have made, they should all be numbers, except the name...")

    def fixMember(self):
        try:
            oldMember = self.memsListNew[self.mIndex]
            fixedMember = Member(self.specInfo[0].text(), float(self.specInfo[1].text()), float(self.specInfo[2].text()),
                               float(self.specInfo[3].text()), self.specInfo[7].isChecked(), float(self.specInfo[4].text()),
                               float(self.specInfo[5].text()), box=self.specInfo[8].isChecked(), holeSupport=int(self.specInfo[6].text()))
            self.memsListNew[self.mIndex] = fixedMember
            # Here, we check if the member edited was part of any joints, and if so,
            # make sure that joint is updated to use the newly edited member
            if oldMember.n != fixedMember.n:
                self.jointInfo[self.mIndex+1].setText(fixedMember.n)
            for i in range(len(self.jointsListNew)):
                for m in range(len(self.jointsListNew[i].members)):
                    if self.jointsListNew[i].members[m].n == oldMember.n:
                        self.jointsListNew[i].members[m] = fixedMember

            # Here is the only time we need to update info when mIndex and jIndex aren't changing
            self.widgetResults.updateInfo(self.memsListNew, self.jointsListNew)
            self.askSave = True
            logger.info('Updated the following member:\n'+str(oldMember)+'\nto\n'+str(fixedMember))
        except:
            PopUp("ERROR: Check the entries you have made, they should all be numbers, except the name...", ERR, self)
            logger.error("Check the entries you have made, they should all be numbers, except the name...")

    def appendJoint(self):
        if not self.creatingJoint and self.createJointButton.isEnabled():
            PopUp('WARNING: You must press "Begin Joint Creation" then select the joints!', WARN, self)
            logger.warning('You must press "Begin Joint Creation" then select the joints!')
            return
        button = self.sender()
        text = button.text()
        button.setEnabled(False)
        for mem in self.memsListNew:
            if mem.n == text:
                self.selectedJoints.append(mem)
                break

    def viewComponents(self):
        print 'List of members:'
        for i in self.memsListNew:
            print i
        if self.memsListNew == []:
            print 'Currently no members!'
        print '\nList of joints:'
        for i in self.jointsListNew:
            print i
        if self.jointsListNew == []:
            print 'Currently no joints!'
        self.tabs.setCurrentIndex(1)

    def calculate(self):
        if self.validate():
            RESULTS = StructAnalysis(self.memsListNew, self.jointsListNew).calcAll()
            logger.info('Here are the results: \n\n'+RESULTS)
            self.tabs.setCurrentIndex(1)
            self.widgetResults.addResults("Results for design '"+self.fName+"':\n\n"+RESULTS)

    def validate(self):
        """Extremely small validation"""
        if len(self.jointsListNew) > len(self.memsListNew):
            PopUp('ERROR: Can\'t have more joints than members in a valid design.', ERR, self)
            logger.error('Can\'t have more joints than members in a valid design.')
            return False
        if len(self.jointsListNew) <= 2 or len(self.memsListNew) <= 2:
            PopUp('ERROR: There must be at least 3 members (and therefore 3 joints) for the design to possibly be valid.', ERR, self)
            logger.error('There must be at least 3 members (and therefore 3 joints) for the design to possibly be valid.')
            return False
        for mem in self.memsListNew:
            if mem.w != 0:
                occur = 0
                for joint in self.jointsListNew:
                    if mem in joint.members:
                        occur += 1
                if occur != 2:
                    PopUp('Error: Each member must connect to two joints, and only two joints.\nThis does not include external forces!', ERR, self)
                    logger.error('Each member must connect to two joints, and only two joints.\nThis does not include external forces!')
                    return False
        return True

    def updateStatus(self, msg):
        self.statusBar().showMessage(msg)

    def closeEvent(self, event):
        if self.askSave:
            if self.savePrompt() == SAVE_CANCEL:
                query = PopUp('Nothing was saved, are you sure you want to continue?', YES_NO, self)
                if query.reply == QtGui.QMessageBox.No:
                    event.ignore()
                    return
        super(TrussCalc, self).closeEvent(event)


# Member(name, hole-hole length, endWidth, thickness, compression bool,
#        internal force, hole distance from edge, boxBeam?, holeSupport)
# AD = Member('AD', 0.3, 0.0112, 0.0112, True, 2, 0.004, box = True)
# CD = Member('CD', 0.2062, 0.00838, 0.0032, False, 2.062, 0.01, holeSupport = 3)
# AC = Member('AC', 0.1118, 0.0075, 0.0067, True, 1.118, 0.004)
# AB = Member('AB', 0.05, 0.00818, 0.0032, False, 0.5, 0.009)
# BC = Member('BC', 0.1, 0.00838, 0.0032, False, 3, 0.01, holeSupport = 3)
# Rc = Member('Rc', 0, 0, 0, False, 3, 0)
# Ra = Member('Ra', 0, 0, 0, True, 3.041, 0)
# P = Member('P', 0, 0, 0, False, 1, 0)

# A = Joint('A', [Rc, AD, AC, AB])
# B = Joint('B', [BC, Ra, AB])
# C = Joint('C', [CD, BC, AC])
# D = Joint('D', [CD, AD, P])

# memsList = [AB, AC, CD, AD, BC, Rc, Ra, P]
# jointsList = [A, B, C, D]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = TrussCalc()
    app.exec_()

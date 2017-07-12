from PySide import QtGui, QtCore
from backend.helpers import ifThen
from backend.consts import *

class WidgetResults(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WidgetResults, self).__init__(parent)
        self.results = 'No results to show yet!'
        self.designInfo = 'No design information to show yet!'

        self._initUI()

    def _initUI(self):
        grid = QtGui.QGridLayout()
        label = QtGui.QLabel('Design Components', self)
        label.setFont(titleFont)
        grid.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignHCenter)
        label = QtGui.QLabel('Calculation Results (in Newtons)', self)
        label.setFont(titleFont)
        grid.addWidget(label, 0, 1, alignment=QtCore.Qt.AlignHCenter)
        grid.addWidget(label, 0, 1, alignment=QtCore.Qt.AlignHCenter)
        self._resultsBox = QtGui.QTextEdit(self.results, self)
        self._resultsBox.setReadOnly(True)
        self._designInfoBox = QtGui.QTextEdit(self.designInfo, self)
        self._designInfoBox.setReadOnly(True)
        grid.addWidget(self._resultsBox, 1, 1)
        grid.addWidget(self._designInfoBox, 1, 0)
        self.setLayout(grid)

    def addResults(self, resultsText):
        self._resultsBox.setText(resultsText)

    def updateInfo(self, mems, joints):
        mText = ifThen(mems == [], 'Currently no members!', 'Current members: \n')
        jText = ifThen(joints == [], 'Currently no joints!', 'Current joints: \n')
        for m in mems:
            mText += str(m)+'\n'

        for j in joints:
            jText += str(j)+'\n'
        self._designInfoBox.setText(mText+'\n'+jText)

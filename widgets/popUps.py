from PySide import QtGui, QtCore
from backend.consts import *
from backend.helpers import ifThen

class PopUp(object):
    def __init__(self, text, kind=INFO, parent=None):
        self.text = text
        self.kind = kind
        self.parent = parent
        self.reply = self._initMsg()

    def _initMsg(self):
        if self.kind in [INFO, WARN, ERR]:
            msgBox = ifThen([self.kind == INFO, self.kind == WARN, self.kind == ERR],
            [QtGui.QMessageBox(QtGui.QMessageBox.Information, 'Info', self.text, parent=self.parent),
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Warning', self.text, parent=self.parent)],
            QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', self.text, parent=self.parent))
            msgBox.exec_()
        else:
            return QtGui.QMessageBox.question(self.parent, 'Question', self.text, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

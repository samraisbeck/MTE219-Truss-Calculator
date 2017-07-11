from PySide import QtGui, QtCore

class WidgetResults(QtGui.QWidget):
    def __init__(self, parent=None, res=''):
        super(WidgetResults, self).__init__(parent)
        self.results = res

        self._initUI()

    def _initUI(self):
        grid = QtGui.QGridLayout()
        self._resultsBox = QtGui.QTextEdit(self.results, self)
        self._resultsBox.setReadOnly(True)
        grid.addWidget(self._resultsBox)
        self.setLayout(grid)

    def addResults(self, resultsText):
        self._resultsBox.setText(resultsText)

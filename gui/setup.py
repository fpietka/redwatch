from PyQt4 import QtCore, QtGui
from redmine.api import Api, ApiException


class SetupWindow(QtGui.QWidget):
    def __init__(self, app):
        super(SetupWindow, self).__init__()
        self._app = app
        #creation of the UI
        self.initUI()
        self._setWindowInfos()
        self.show()

    #define window informations
    def _setWindowInfos(self):
        self.setGeometry(0, 0, 400, 150)
        self.setFixedSize(400, 150)
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        self.setWindowTitle('Initial setup')

    def initUI(self):
        layout = QtGui.QGridLayout()

        self._resultLabel = QtGui.QLabel()
        self._resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._resultLabel.setText('Set URL and API key')

        urlLabel = QtGui.QLabel('URL')
        self._urlField = QtGui.QLineEdit()
        self._urlField.returnPressed.connect(self._saveAction)

        apikeyLabel = QtGui.QLabel('API key')
        self._apikeyField = QtGui.QLineEdit()
        self._apikeyField.returnPressed.connect(self._saveAction)

        saveButton = QtGui.QPushButton('Save')
        saveButton.clicked.connect(self._saveAction)

        layout.addWidget(self._resultLabel, 1, 0, 1, 2)
        layout.addWidget(urlLabel, 2, 0)
        layout.addWidget(self._urlField, 2, 1)
        layout.addWidget(apikeyLabel, 3, 0)
        layout.addWidget(self._apikeyField, 3, 1)
        layout.addWidget(saveButton, 4, 1)

        self.setLayout(layout)

    def _saveAction(self):
        url = self._urlField.text()
        apikey = self._apikeyField.text()
        if not url:
            self._resultLabel.setText("Please provide an URL")
        elif not apikey:
            self._resultLabel.setText("Please provide an API key")
        else:
            try:
                self._app._settings.setValue('redmineUrl', url)
                self._app._settings.setValue('redmineApiKey', apikey)
                result = Api().statuses()
                self.emit(QtCore.SIGNAL('FirstSetupOk'))
                self.close()
            except ApiException, e:
                self._resultLabel.setText(e.message)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


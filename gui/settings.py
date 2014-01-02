# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import core.settings as settings
import core.consts as consts
import re
from redmine.api import Api, ApiException
from math import floor


class SettingsWindow(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.initUi()
        self.setWindowTitle('Settings')
        self.show()

    def initUi(self):
        layout = QtGui.QGridLayout()

        appSettings = settings.AppSettings()
        self.fields = {}

        s = 0
        for i in consts.settings.keys():
            label = QtGui.QLabel(appSettings.label(i))
            widget = SettingsFieldFactory.createField(
                self,
                appSettings.type(i),
                appSettings.value(i)
            )

            if widget is not None:
                layout.addWidget(label, s, 0)
                if hasattr(widget, 'widget'):
                    for i, w in enumerate(widget.widget, 1):
                        layout.addWidget(w, s, i)
                else:
                    layout.addWidget(widget, s, 1)
                s += 1

                self.fields[i] = widget

        saveButton = QtGui.QPushButton('Save')
        saveButton.clicked.connect(self.saveSettings)
        cancelButton = QtGui.QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)

        layout.addWidget(saveButton, s, 0)
        layout.addWidget(cancelButton, s, 1)

        self.setLayout(layout)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def saveSettings(self):
        appSettings = settings.AppSettings()
        for i in self.fields:
            appSettings.setValue(i, self.fields[i].value())
        self.close()


class ColorSettingsWindow(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.initUi()
        self.setWindowTitle('Color settings')
        self.show()

    def initUi(self):
        layout = QtGui.QGridLayout()
        appSettings = settings.AppSettings()
        self.position = 0
        self.fields = {}

        self.addStatusesColor(layout)

        saveButton = QtGui.QPushButton('Save')
        saveButton.clicked.connect(self.saveSettings)
        cancelButton = QtGui.QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)

        layout.addWidget(saveButton, self.position, 0)
        layout.addWidget(cancelButton, self.position, 1)

        self.setLayout(layout)

    def addStatusesColor(self, layout):
        sysSettings = settings.SystemSettings()
        for status in sysSettings.value('issue_statuses'):
            label = QtGui.QLabel(status['name'])
            if sysSettings.value('status_colors'):
                color = sysSettings.value('status_colors')[status['name']]
            else:
                color = None
            widget = SettingsFieldFactory.createField(
                self,
                'color',
                color,
                status['name']
            )
            self.fields[label] = widget
            layout.addWidget(widget, floor(self.position / 2), self.position % 2)
            self.position += 1

    def saveSettings(self):
        sysSettings = settings.SystemSettings()
        colors = dict()
        for field in self.fields:
            colors[field.text()] = self.fields[field].value()
        sysSettings.setValue('status_colors', colors)
        self.close()


class SetupWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SetupWindow, self).__init__(parent)
        self.app = QtGui.QApplication.instance()
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
        self.setWindowIcon(QtGui.QIcon(consts.mainIcon))

    def initUI(self):
        layout = QtGui.QGridLayout()

        self._resultLabel = QtGui.QLabel()
        self._resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._resultLabel.setText('Set URL and API key')

        urlLabel = QtGui.QLabel('URL')
        self._urlField = QtGui.QLineEdit()
        self._urlField.setText(self.app._settings.value('redmineUrl'))
        self._urlField.returnPressed.connect(self._saveAction)

        apikeyLabel = QtGui.QLabel('API key')
        self._apikeyField = QtGui.QLineEdit()
        self._apikeyField.setText(self.app._settings.value('redmineApiKey'))
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
                self.app._settings.setValue('redmineUrl', url)
                self.app._settings.setValue('redmineApiKey', apikey)
                result = Api().statuses()
                self.emit(QtCore.SIGNAL('FirstSetupOk'))
                self.close()
            except Exception, e:
                # empty settings
                self.app._settings.setValue('redmineUrl', '')
                self.app._settings.setValue('redmineApiKey', '')
                self._resultLabel.setText(e.message)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


class SettingsFieldFactory:

    @staticmethod
    def createField(window, fieldType, value=None, name=''):
        if fieldType == consts.SETTINGS_TYPE_COLOR:
            field = ColorPickerWidget(value, name)
        elif fieldType == consts.SETTINGS_TYPE_BOOLEAN:
            field = BooleanWidget()
            if value:
                field.setCheckState(QtCore.Qt.Checked)
            else:
                field.setCheckState(QtCore.Qt.Unchecked)
        elif fieldType == consts.SETTINGS_TYPE_INT:
            field = IntWidget(str(value))
        else:
            field = None
        return field


class BooleanWidget(QtGui.QCheckBox):
    def value(self):
        if self.checkState() == QtCore.Qt.Checked:
            return True
        else:
            return False


class IntWidget(QtGui.QLineEdit):
    def value(self):
        try:
            return int(self.text())
        except ValueError:
            return 1


class ColorPickerWidget(QtGui.QPushButton):
    def __init__(self, value=None, name=''):
        super(ColorPickerWidget, self).__init__(value)

        self.name = name
        if not value:
            value = '#fdf6e3'

        self.changeColor(QtGui.QColor(value))

        self.clicked.connect(self.selectColor)

    def to_rgb(self, color):
        """
        Return list of RGB (base 16) values from hexadecimal #rrggbb
        """
        return map(lambda x: int(str(x), 16), filter(None, re.split(r'\#(\w{2})(\w{2})(\w{2})', color)))

    def selectColor(self):
        colorDial = QtGui.QColorDialog(QtGui.QColor(self._value), self)
        for index, color in enumerate(consts.COLORS):
            colorDial.setCustomColor(index, QtGui.qRgb(color[0], color[1], color[2]))
        colorDial.colorSelected.connect(self.changeColor)
        colorDial.show()

    def changeColor(self, color):
        self._value = color.name()
        self.setText(self.name)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(self._value))

        self.setPalette(palette)
        # change button style
        color = self.to_rgb(str(self._value))

        brightness = ((color[0] * 299) + (color[1] * 587) + (color[2] * 114)) / 1000
        if brightness < 125:
            textcolor = "#ffffff"
        else:
            textcolor = "#000000"

        self.setObjectName('color-button')
        self.setStyleSheet('QPushButton#color-button { background: ' + self._value + '; color: ' + textcolor + '}')

    def value(self):
        return self._value

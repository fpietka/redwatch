# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import core.settings as settings
import core.consts as consts
import re

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

            if widget != None:
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


class SettingsFieldFactory:

    @staticmethod
    def createField(window, fieldType, value = ''):
        if fieldType == consts.SETTINGS_TYPE_COLOR:
            field = ColorPickerWidget(value)
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
    def __init__(self, value):
        super(ColorPickerWidget, self).__init__(value)

        color = map(lambda x: int(str(x), 16), filter(None, re.split(r'\#(\w{2})(\w{2})(\w{2})', value)))

        brightness = ((color[0] * 299) + (color[1] * 587) + (color[2] * 114)) / 1000
        if brightness < 125:
            textcolor = "#ffffff"
        else:
            textcolor = "#000000"

        self.setObjectName('color-button')
        self.setStyleSheet('QPushButton#color-button { background: ' + value + '; color: ' + textcolor + '}')

        self.changeColor(QtGui.QColor(value))

        self.clicked.connect(self.selectColor)

    def selectColor(self):
        colorDial = QtGui.QColorDialog(QtGui.QColor(self._value), self)
        for index, color in enumerate(consts.COLORS):
            colorDial.setCustomColor(index, QtGui.qRgb(color[0], color[1], color[2]))
        colorDial.colorSelected.connect(self.changeColor)
        colorDial.show()

    def changeColor(self, color):
        self._value = color.name()
        self.setText(color.name())
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(self._value))
        self.setPalette(palette)

    def value(self):
        return self._value

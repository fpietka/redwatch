# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import core.consts as consts


class SystemSettings(QtCore.QSettings):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SystemSettings, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(SystemSettings, self).__init__(self.IniFormat,
            self.UserScope, consts.company, consts.appname)
        self.name = consts.appname

    def __getattr__(self, name):
        if not self.contains(name):
            return None
        return self.value(name)

    def intValue(self, name):
        if not self.contains(name):
            return None
        return int(self.value(name).toInt()[0])

    def setValue(self, key, value):
        value = str(value)
        super(SystemSettings, self).setValue(key, value)

    def stringValue(self, name):
        if not self.contains(name):
            return None
        return str(self.value(name).toString())


class AppSettings(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppSettings, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self._settings:
            self._settings = SystemSettings()

    def __getattr__(self, name):
        if not consts.settings.has_key(name):
            return None

        if self._settings.contains(name):
            if consts.settings[name]['type'] == consts.SETTINGS_TYPE_COLOR:
                return getattr(self._settings, name).toString()
            elif consts.settings[name]['type'] == consts.SETTINGS_TYPE_BOOLEAN:
                return getattr(self._settings, name).toBool()
            elif consts.settings[name]['type'] == consts.SETTINGS_TYPE_INT:
                return getattr(self._settings, name).toInt()[0]
        else:
            return consts.settings[name]['value']

    def value(self, key):
        return self.__getattr__(key)

    def label(self, key):
        if not consts.settings.has_key(key):
            return None

        return consts.settings[key]['label']

    def type(self, key):
        if not consts.settings.has_key(key):
            return None

        return consts.settings[key]['type']

    def setValue(self, key, value):
        self._settings.setValue(key, value);


class SettingsException(Exception):
    pass

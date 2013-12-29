# -*- coding: utf-8 -*-

"""
Extends PyQt4.QtCore.QSettings to get and store python objects
like strings and dictionaries.
"""

from PyQt4 import QtCore
import core.consts as consts
import json


class SystemSettings(QtCore.QSettings):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SystemSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(SystemSettings, self).__init__(self.IniFormat, self.UserScope, consts.company, consts.appname)
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
        """
        Save json data
        """
        if type(value) in (dict, list):
            value = json.dumps(value)
        super(SystemSettings, self).setValue(key, value)

    def value(self, name):
        """
        Try to load json objects from config file
        """
        value = super(SystemSettings, self).value(name)
        if value:
            try:
                return json.loads(value)
            except ValueError:
                return value


class AppSettings(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._settings = SystemSettings()

    def __getattr__(self, name):
        if name not in consts.settings:
            return None

        if self._settings.contains(name):
            if consts.settings[name]['type'] == consts.SETTINGS_TYPE_COLOR:
                return getattr(self._settings, name)
            elif consts.settings[name]['type'] == consts.SETTINGS_TYPE_BOOLEAN:
                return getattr(self._settings, name)
            elif consts.settings[name]['type'] == consts.SETTINGS_TYPE_INT:
                return getattr(self._settings, name)
        else:
            return consts.settings[name]['value']

    def value(self, key):
        return self.__getattr__(key)

    def label(self, key):
        if key not in consts.settings:
            return None

        return consts.settings[key]['label']

    def type(self, key):
        if key not in consts.settings:
            return None

        return consts.settings[key]['type']

    def setValue(self, key, value):
        self._settings.setValue(key, value)


class SettingsException(Exception):
    pass

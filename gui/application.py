# -*- coding: utf8 -*-

import sys

from PyQt4 import QtGui, QtCore

from core.settings import SystemSettings, AppSettings
from gui.settings import SetupWindow
from gui.task import TaskWindow
from redmine.api import Api, ApiException


class Application(QtGui.QApplication):

    def __init__(self, debug=False):
        super(Application, self).__init__(sys.argv)

        self._settings = SystemSettings()

        if not self._settings.value('redmineUrl') or not self._settings.value('redmineApiKey'):
            self.launchSetupWindow()
        else:
            try:
                self.updateStatuses()
                self.launchMainWindow()
            except ApiException:
                self.launchSetupWindow()
        sys.exit(self.exec_())

    def launchMainWindow(self):
        self.widget = TaskWindow()
        self.widget.displayWindow()

    def launchSetupWindow(self):
        # must belong to the application
        self._setupWindow = SetupWindow()
        self.connect(self._setupWindow, QtCore.SIGNAL('FirstSetupOk'), self.launchMainWindow)

    def updateStatuses(self):
        self._settings.setValue('issue_statuses', Api().statuses()['issue_statuses'])

    def setLocked(self, locked):
        self._currentlyChecksVersion = locked

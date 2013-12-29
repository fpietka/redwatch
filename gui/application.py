# -*- coding: utf8 -*-
import sys
from PyQt4 import QtGui, QtCore
#from core.workers import CheckVersionThread
from core.settings import SystemSettings, AppSettings
from gui.task import TaskWindow
from gui.setup import SetupWindow
from redmine.api import Api, ApiException


class Application(QtGui.QApplication):

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        # loads some settings
        self._settings = SystemSettings()
        self._appSettings = AppSettings()

        # XXX is checking version? move that to a thread
        #self.setLocked(False)

        # init the order field and way in the conf
        # XXX might be done in SystemSettings apparently
        if not self._settings.value('defaultTicketsOrderField'):
            self._settings.setValue('defaultTicketsOrderField', {})
        if not self._settings.value('defaultTicketsOrderWay'):
            self._settings.setValue('defaultTicketsOrderWay', {})

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
        #self.checkVersion(True)
        self.widget = TaskWindow()
        self.widget.displayWindow()

    def launchSetupWindow(self):
        # must belong to the application
        self._setupWindow = SetupWindow()
        self.connect(self._setupWindow, QtCore.SIGNAL('FirstSetupOk'), self.launchMainWindow)

    def updateStatuses(self):
        self._settings.setValue('issue_statuses', Api().statuses()['issue_statuses'])

    # XXX following code to a thread

    def checkVersion(self, automatic=False):
        # XXX handle with thread
        if self._currentlyChecksVersion:
            return
        self._cv = CheckVersionThread(self, automatic)
        self.connect(self._cv, QtCore.SIGNAL('versionCheck'), self.checkVersionResult)
        self._cv.start()

        self.setLocked(True)

    def setLocked(self, locked):
        self._currentlyChecksVersion = locked

    def checkVersionResult(self, title='', message=''):
        if title != '' and message != '':
            QtGui.QMessageBox.information(self.widget, title, message)

        self.setLocked(False)
        self.disconnect(self._cv, QtCore.SIGNAL('versionCheck'), self.checkVersionResult)

# -*- coding: utf-8 -*-

"""
Background worker threads.
"""

import sys
from time import sleep, time, strftime
from datetime import datetime
from PyQt4 import QtCore, QtGui
import core.consts as consts
import urllib2, httplib

from TasksManagement import TasksManagement

from redmine.ticket import Ticket

from core.settings import SettingsException


class WorkerTasks(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)

        self._parent = parent
        self.exiting = False

        self.interval = float(self._parent._appSettings.refresh_interval)

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        while not self.exiting:
            sleep(self.interval)
            self.emit(QtCore.SIGNAL('refreshSignal'))


class RefreshThread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self._parent = parent

    def run(self):
        # get data asynchronously
        try:
            tabs = TasksManagement.getTicketsIds(self._parent._app)
        except SettingsException:
            tabs = dict()
        data = dict()
        for tab, tickets in tabs.iteritems():
            data[tab] = Ticket.getTickets(tickets)
        self._parent.data = data
        self.emit(QtCore.SIGNAL('refreshEnds'))

    def __del__(self):
        self.wait()


class CheckVersionThread(QtCore.QThread):

    def __init__(self, parent, automatic):
        QtCore.QThread.__init__(self)
        self._automatic = automatic

    def run(self):
        title = ''
        message = ''
        try:
            #if VersionManager.checkVersion() < 0:
            if False:
                title = "New Version"
                message = "Your version is not the lastest, you can download the last version here: "
                "Windows users: http://apps.maximiles.com/monitor/redmine-tickets-latest.exe"
                "Git users: get the last version of the master branch"
                "Linux users: soon, soon"
            elif not self._automatic:
                title = "No New Version"
                message = "Your version is the lastest available"
        except httplib.HTTPException, e:
            if not self._automatic:
                title = "Version check error"
                message = e.__str__()

        self.emit(QtCore.SIGNAL('versionCheck'), title, message)


    def __del__(self):
        self.wait()

# -*- coding: utf-8 -*-

"""
Background worker threads.
"""

from time import sleep

from PyQt4 import QtCore

from TasksManagement import TasksManagement
from redmine.ticket import Ticket
from core.settings import SettingsException


class WorkerTasks(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self._parent = parent
        self.exiting = False

        interval = self._parent._settings.value('refresh_interval')
        if not interval:
            self.interval = 60
        else:
            self.interval = float(interval)

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
        tabs = TasksManagement.getTicketsIds(self._parent._app)
        data = dict()
        try:
            for tab, tickets in tabs.iteritems():
                tabTickets = Ticket.getTickets(tickets)
                if tab in self._parent.data:
                    data[tab] = dict(self._parent.data[tab].items() + tabTickets.items())
                else:
                    data[tab] = tabTickets
        except:
            self._parent.message = "Error: unable to connect"

        self._parent.data = data
        self.emit(QtCore.SIGNAL('refreshEnds'))

    def __del__(self):
        self.wait()

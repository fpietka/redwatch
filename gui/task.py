# -*- coding: utf8 -*-

import csv

from PyQt4 import QtGui, QtCore

import core.consts as consts
from core.settings import SystemSettings
from core.workers import WorkerTasks, RefreshThread
from gui.systemtray import TaskSystemTrayIcon
from gui.settings import SettingsWindow, ColorSettingsWindow
from gui.menu import ApplicationMenu
from redmine.ticket import Ticket
from gui.taskslist import TasksList
from TasksManagement import TasksManagement


class TaskWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(TaskWindow, self).__init__(parent)
        self._app = QtGui.QApplication.instance()
        # ticket list by tab
        self.tickets = dict()
        # data for tickets
        # XXX empty for now, should be filled by a refresh
        self.data = dict()

    def displayWindow(self):
        self.threads = {
            'refresh_trigger': WorkerTasks(self._app),
            'refresh_signal': RefreshThread(self)
        }
        self.connect(self.threads['refresh_trigger'], QtCore.SIGNAL('refreshSignal'), self.refresh)
        self.threads['refresh_trigger'].start()
        self.connect(self.threads['refresh_signal'], QtCore.SIGNAL('refreshEnds'), self.updateData)
        self._setSystemTrayIcon()
        self._create()
        self._setWindowInfos()
        self._show()

        self.refresh()

    def __del__(self):
        # stop running threads
        for thread in self.threads:
            thread.stop()

    def _setSystemTrayIcon(self):
        self._trayIcon = TaskSystemTrayIcon(QtGui.QIcon(consts.mainIcon), self, self._app)

    def _create(self):
        #shape of the window:
        #A Widget which contains all the elements
        #   In the widget
        #   A tab widget
        #A status bar

        #top menu
        self.setMenuBar(ApplicationMenu(self))

        #main container
        self._tabWidget = QtGui.QTabWidget()
        self._tabWidget.setMovable(True)
        self._tabWidget.currentChanged.connect(self._changeTab)

        self.setCentralWidget(self._tabWidget)
        self.setStatusBar(QtGui.QStatusBar())

    def displayMessage(self, text=''):
        self.statusBar().showMessage(text)

    def _showSettings(self):
        SettingsWindow(self)

    def _showColorSettings(self):
        ColorSettingsWindow(self)

    def _showAbout(self):
        QtGui.QMessageBox.information(self, "About", "You use the version %s of the Redmine Tickets Monitor application" % 'beta')

    def _addNewTab(self, name=False, data=[], header=[]):
        #if the tabname is not given, then, the user triggered the "add tab" action
        #else, the tab is loaded from the settings
        if name is False:
            tabNameResult = True
            while not name or (self.data and name in self.data):
                tabNameResult = QtGui.QInputDialog.getText(self, "Tab name", "Tab name", QtGui.QLineEdit.Normal, "")
                #typed value
                name = str(tabNameResult[0])
                #true if "ok", false if "cancel" or escape
                tabNameResult = tabNameResult[1]
                #if user cancelled the prompt, the action is stopped
                if not tabNameResult:
                    return
                #empty tab name
                if not name:
                    QtGui.QMessageBox.critical(self, "Error", "The tab need a name")
                #already existing tab
                elif self.data and name in self.data:
                    QtGui.QMessageBox.critical(self, "Error", "This tab already exists")
        (orderField, orderWay) = self._getListOrder(name)
        index = self._tabWidget.addTab(TasksList(self, name, data, header, orderField, orderWay), name)
        TasksManagement.addTab(self._app, name)
        self._tabWidget.setCurrentIndex(index)

    def _getListOrder(self, tabName):
        settingsOrderField = self._app._settings.value('defaultTicketsOrderField')
        settingsOrderWay = self._app._settings.value('defaultTicketsOrderWay')

        if not settingsOrderField or tabName not in settingsOrderField:
            orderField = consts.defaultTicketsOrderField
        else:
            orderField = settingsOrderField[tabName]

        if not settingsOrderWay or tabName not in settingsOrderWay:
            orderWay = consts.defaultTicketsOrderWay
        else:
            orderWay = settingsOrderWay[tabName]

        return (orderField, orderWay)

    def _saveTab(self):
        #get the tab name and index
        currentTabIndex = self._tabWidget.currentIndex()
        tabName = str(self._tabWidget.tabText(currentTabIndex))

        fileName = QtCore.QDir.home().absolutePath() + QtCore.QDir.separator() + ("tab_%s.csv" % tabName)
        writer = csv.writer(open(fileName, "wb"))

        csvData = []
        for i in enumerate(self.data[tabName]):
            tmp = []
            for v in i[1].values():
                try:
                    tmp.append(v.encode('utf-8'))
                except:
                    tmp.append(v)
            csvData.append(tmp)

        writer.writerows(csvData)
        QtGui.QMessageBox.information(self, "Tab saved", "The tab %s has been saved in the file %s" % (tabName, fileName))

    def _purgeTickets(self, removeTab=False):
        TasksManagement.purgeTickets(self._app, self._tabWidget.tabText(self._tabWidget.currentIndex()), removeTab)
        self.refresh()

    def _deleteTab(self):
        self._purgeTickets(True)
        self._tabWidget.removeTab(currentTabIndex)

    def _deleteTabs(self):
        TasksManagement.purgeTickets(self._app)
        self._tabWidget.clear()
        self.refresh()

    def _setWindowInfos(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Redwatch')
        self.setWindowIcon(QtGui.QIcon(consts.mainIcon))

    def setWidth(self):
        settings = SystemSettings()
        if not settings.value('windowResizable'):
            currentTab = self._tabWidget.currentWidget()
            if (currentTab):
                tableWidth = currentTab.getTable().width()
                # the width must be changed only if the table is not empty
                if tableWidth > self._tabWidget.currentWidget().layout().margin():
                    self.setFixedWidth(tableWidth + self._tabWidget.currentWidget().layout().margin() * 2)

    def refresh(self):
        self.displayMessage('refreshing tabs ...')
        self.threads['refresh_signal'].start()

    def removeTicket(self, tab, ticket):
        key = (key for key, item in enumerate(self.data[tab]['data']) if item['id'] == ticket).next()
        self.data[tab]['data'].pop(key)
        self.updateData(tab)

    def updateData(self, tab=None):
        # refresh existing tabs name
        tabs = dict()
        nbTabs = self._tabWidget.count()
        for i in range(0, nbTabs):
            tabName = str(self._tabWidget.tabText(i))
            tabs[tabName] = self._tabWidget.widget(i)
        # refresh or create tabs
        if tab:
            if tab in tabs:
                tabs[tab].setData(self.data[tab]['data'], self.data[tab]['header'])
            else:
                self._addNewTab(tab, self.data[tab]['data'], self.data[tab]['header'])
        else:
            for tab, data in self.data.iteritems():
                header = data['header']
                data = data['data']
                if tab in tabs:
                    tabs[tab].setData(data, header)
                else:
                    self._addNewTab(tab, data, header)
        self.displayMessage()
        self.setWidth()

    #event methods

    def _changeTab(self):
        self.setWidth()

    #method to show the elements (tray icon and widget)
    def _show(self):
        self._trayIcon.show()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.hide()
        elif e.key() == QtCore.Qt.Key_F5:
            self.refresh()
        elif e.modifiers() == QtCore.Qt.ControlModifier:
            if e.key() == QtCore.Qt.Key_PageDown:
                # change to previous tab
                if self._tabWidget.currentIndex() < self._tabWidget.count() - 1:
                    self._tabWidget.setCurrentIndex(self._tabWidget.currentIndex() + 1)
            elif e.key() == QtCore.Qt.Key_PageUp:
                # change to next tab
                if self._tabWidget.currentIndex() > 0:
                    self._tabWidget.setCurrentIndex(self._tabWidget.currentIndex() - 1)

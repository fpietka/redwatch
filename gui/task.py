# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

import core.consts as consts
from core.workers import WorkerTasks, RefreshThread
from gui.systemtray import TaskSystemTrayIcon
from gui.settings import SettingsWindow, ColorSettingsWindow
from gui.menu import ApplicationMenu
from redmine.ticket import Ticket
from gui.taskslist import TasksList
from TasksManagement import TasksManagement

import csv


class TaskWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(TaskWindow, self).__init__(parent)

        self._app = QtGui.QApplication.instance()

        #by default the window is displayed, could be moved in conf maybe
        self._displayed = True

        #at the creation of the widget, the tickets list is fetched and
        #saved in the object

        """ticket list by tab"""
        self.tickets = dict()
        """data for tickets"""
        # XXX empty for now, should be filled by a refresh
        self.data = dict()

        # XXX old method to get ticket data
        #self.setData(data)

    def displayWindow(self):
        try:
            self._refreshThread = RefreshThread(self)
            # XXX init refresh thread that will trigger refresh itself
            self.thread = WorkerTasks(self._app)
            self.connect(self.thread, QtCore.SIGNAL('refreshSignal'), self.notifyChanges)
            self.thread.start()
        except Exception, e:
            print('Unable to init Thread')
        #creation of the system tray icon
        self._setSystemTrayIcon()
        #creation fo the window
        self._create()
        #definition if window informations (size, position, title)
        self._setWindowInfos()
        #display the Whole Thing
        self._show()

        self.refresh()

    # stop the thread if the window is closed
    def __del__(self):
        self.thread.stop()

    #creation of the system tray icon
    def _setSystemTrayIcon(self):
        self._trayIcon = TaskSystemTrayIcon(QtGui.QIcon(consts.mainIcon), self, self._app)

    #creation of the system tray icon
    def systemTrayIcon(self):
        return self._trayIcon

    #method which create the UI
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

    #action to add a tab
    def _addNewTab(self, name=False, data=[], header=[]):
        #if the tabname is not given, then, the user triggered the "add tab" action
        #else, the tab is loaded from the settings
        if name is not False:
            newTab = False
        else:
            newTab = True
            tabNameResult = True
            while not name or (self.data and name in self.data):
                tabNameDResult = QtGui.QInputDialog.getText(self, "Tab name", "Tab name", QtGui.QLineEdit.Normal, "")
                #typed value
                name = str(tabNameDResult[0])

                #true if "ok", false if "cancel" or escape
                tabNameResult = tabNameDResult[1]

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
        self._tabWidget.setCurrentIndex(index)

    def _getListOrder(self, tabName):
        settingsOrderField = self._app._settings.value('defaultTicketsOrderField')
        settingsOrderWay = self._app._settings.value('defaultTicketsOrderWay')

        if tabName not in settingsOrderField:
            orderField = consts.defaultTicketsOrderField
        else:
            orderField = settingsOrderField[tabName]

        if tabName not in settingsOrderWay:
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

    #action to delete a tab
    def _deleteTab(self):
        #get the tab name and index
        currentTabIndex = self._tabWidget.currentIndex()
        tabName = str(self._tabWidget.tabText(currentTabIndex))

        #delete the tickets from the settings
        TasksManagement.purgeTickets(self._app, tabName, True)

        #delete the tab
        self._tabWidget.removeTab(currentTabIndex)

        #refresh the display
        self.refresh()

    #action to delete all tabs
    def _purgeTabs(self):
        #delete all tickets from settings
        TasksManagement.purgeTickets(self._app)

        #delete all tabs
        self._tabWidget.clear()

        #refresh the display
        self.refresh()

    #action to empty a tab, without deleting it
    def _purgeTickets(self):
        #delete tickets from settings
        TasksManagement.purgeTickets(self._app, str(self._tabWidget.tabText(self._tabWidget.currentIndex())))

        #refresh display
        self.refresh()

    #define window informations
    def _setWindowInfos(self):
        # default size
        self.setGeometry(300, 300, 600, 600)
        self.setWidth()

        self.setWindowTitle('Redmine tickets')
        self.setWindowIcon(QtGui.QIcon(consts.mainIcon))

    #the width depends on the table width
    def setWidth(self):
        currentTab = self._tabWidget.currentWidget()

        tableWidth = 0
        if (currentTab):
            tableWidth = currentTab.getTable().width()

        #the width must be changed only if the table is not empty
        if tableWidth > 0:
            if not self._app._appSettings.windowResizable:
                self.setFixedWidth(tableWidth + self._tabWidget.currentWidget().layout().margin() * 2)

    #from a tickets list, the tickets infos are fetched, and saved, headers
    #in one side and data in another
    def setData(self, data):
        # XXX old direct method, now use updateData
        for t in data:
            dataRow = Ticket.getTickets(data[t])
            self.header[t] = dataRow['header']
            self.data[t] = dataRow['data']

    def updateData(self):
        # refresh existing tabs name
        tabs = dict()
        nbTabs = self._tabWidget.count()
        for i in range(0, nbTabs):
            tabName = str(self._tabWidget.tabText(i))
            tabs[tabName] = self._tabWidget.widget(i)
        # refresh or create tabs
        for tab, data in self.data.iteritems():
            header = data['header']
            data = data['data']
            if tab in tabs:
                tabs[tab].setData(data, header)
            else:
                self._addNewTab(tab, data, header)

        self.displayMessage()

    #refresh the display
    def refresh(self):
        self.displayMessage('refreshing tabs ...')
        self.connect(self._refreshThread, QtCore.SIGNAL('refreshEnds'), self.updateData)
        self._refreshThread.start()

    #event methods

    def _changeTab(self):
        self.setWidth()

    #method to show the elements (tray icon and widget)
    def _show(self):
        self._trayIcon.show()
        self.show()
        self._displayed = True

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.hide()
            self._displayed = False
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

    def notifyChanges(self):
        self.refresh()

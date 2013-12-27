# -*- coding: utf8 -*-

from PyQt4 import QtGui
import core.consts as consts


class ApplicationMenu(QtGui.QMenuBar):
    def __init__(self, window):
        super(ApplicationMenu, self).__init__(window)

        #exit action
        exitAction = QtGui.QAction(QtGui.QIcon(consts.exitIcon), '&Exit', window)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        #new tab action
        newTabAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&New', window)
        newTabAction.setStatusTip('Create new tab')
        newTabAction.setShortcut('Ctrl+N')
        newTabAction.triggered.connect(window._addNewTab)
        #save current tab action
        saveCurrentTabAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&Save current', window)
        saveCurrentTabAction.setStatusTip('Save current tab to CSV')
        saveCurrentTabAction.setShortcut('Ctrl+S')
        saveCurrentTabAction.triggered.connect(window._saveTab)
        #delete current tab action
        deleteCurrentTabAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&Delete current', window)
        deleteCurrentTabAction.setStatusTip('Delete current tab')
        deleteCurrentTabAction.triggered.connect(window._deleteTab)
        deleteCurrentTabAction.setShortcut('Ctrl+W')
        #purge ticket action
        purgeTicketsAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&Purge current tab', window)
        purgeTicketsAction.setStatusTip('Delete all tickets')
        purgeTicketsAction.triggered.connect(window._purgeTickets)
        #purge tabs action
        purgeTabsAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&Remove all tabs', window)
        purgeTabsAction.setStatusTip('Delete all tabs')
        purgeTabsAction.triggered.connect(window._purgeTabs)
        #settings window action
        showSettingsAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), 'Se&ttings', window)
        showSettingsAction.setStatusTip('Open settings window')
        showSettingsAction.triggered.connect(window._showSettings)
        #about window action
        showAboutAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), '&About', window)
        showAboutAction.setStatusTip('Open about window')
        showAboutAction.triggered.connect(window._showAbout)
        #about window action
        checkVersionAction = QtGui.QAction(QtGui.QIcon(consts.purgeIcon), 'Check &version', window)
        checkVersionAction.setStatusTip('Check if a new version is available')
        checkVersionAction.triggered.connect(window._app.checkVersion)

        fileMenu = self.addMenu('&File')
        fileMenu.addAction(exitAction)

        ticketMenu = self.addMenu('&Tabs')
        ticketMenu.addAction(newTabAction)
        ticketMenu.addAction(saveCurrentTabAction)
        ticketMenu.addSeparator()
        ticketMenu.addAction(purgeTicketsAction)
        ticketMenu.addAction(deleteCurrentTabAction)
        ticketMenu.addSeparator()
        ticketMenu.addAction(purgeTabsAction)

        appMenu = self.addMenu('&App')
        appMenu.addAction(showSettingsAction)
        appMenu.addAction(checkVersionAction)
        appMenu.addAction(showAboutAction)

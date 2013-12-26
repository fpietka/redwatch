# -*- coding: utf8 -*-

from PyQt4 import QtGui

class TaskSystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, widget, app):
        super(TaskSystemTrayIcon, self).__init__(icon, app)

        self._widget = widget

        self._createTrayActions()

        self.activated.connect(self.showApp)
        menu = QtGui.QMenu()
        refreshAction = menu.addAction(self.refreshAction)
        quitAction = menu.addAction(self.quitAction)

        self.setContextMenu(menu)

    def _createTrayActions(self):
        self.refreshAction = QtGui.QAction(self.tr('Refresh'), self,
            triggered=self.refreshClick)
        self.quitAction = QtGui.QAction(self.tr('Quit'), self,
            triggered=QtGui.qApp.quit)

    def refreshClick(self):
        self._widget.refresh()

    def showApp(self, reason):
        if reason != QtGui.QSystemTrayIcon.Trigger:
            return

        if not self._widget._displayed:
            self._widget.show()
            self._widget._displayed = True
        else:
            self._widget.hide()
            self._widget._displayed = False

# -*- coding: utf8 -*-

import operator

from core.settings import AppSettings
from PyQt4 import Qt
#~ from PyQt4.QtCore import QAbstractTableModel
#~ from PyQt4.QtGui import QTableView
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import core.consts as consts

class TasksTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)

        self._parent = parent
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        appSet = AppSettings()

        # XXX Loop over what is defined in consts for now
        # then over what is in the configuration file
        if not index.isValid():
            return None
        elif role == Qt.ForegroundRole:
            if self.arraydata[index.row()]['status_name'] == u'Terminé':
                return QColor(appSet.closedColor)
            else:
                return QColor(appSet.standardForegroundColor)
        elif role == Qt.BackgroundRole:
            if self.arraydata[index.row()]['status_name'] == u'A déployer':
                return QColor(appSet.toPutOnlineColor)
            elif self.arraydata[index.row()]['status_name'] in (u'Garantie', u'Résolu'):
                return QColor(appSet.resolvedColor)
            elif self.arraydata[index.row()]['status_name'] == u'Recette':
                return QColor(appSet.toTestColor)
            elif self.arraydata[index.row()]['status_name'] == u'Cadrage Tech':
                return QColor(appSet.waitingInfosColor)
            elif self.arraydata[index.row()]['status_name'] == '':
                return QColor(appSet.newColor)
            else:
                return QColor(appSet.standardBackgroundColor)
        elif role != Qt.DisplayRole:
            return None

        return self.arraydata[index.row()][self.headerData(index.column())]

    def headerData(self, col, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and len(self.headerdata) > 0:
            return self.headerdata[col]
        return dict()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self._parent._setColSort(Ncol, 'defaultTicketsOrderField')
        self._parent._setColSort(order, 'defaultTicketsOrderWay')

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        try:
            self.arraydata = sorted(self.arraydata, key=operator.itemgetter(self.headerData(Ncol)))
        except IndexError:
            pass
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class TasksTable(QTableView):

    def __init__(self, parent, header, data, orderCol, orderWay):
        super (TasksTable, self).__init__ ()
        self._extraHeader = ['delete']
        self._parent = parent

        self.setSortingEnabled(True)
        self.setData(data, header)

        h = self.horizontalHeader()
        h.setSortIndicator(self._parent._orderCol, self._parent._orderWay)


    def updateWidth(self):
        appSet = AppSettings()
        index = 0
        width = 0
        while self.columnWidth(index) > 0:
            width += self.columnWidth(index) + self.columnSpan(0, index)
            index += 1

        if not appSet.windowResizable:
            self.setFixedWidth(width)

        return self.width()

    def setData(self, data, header):
        self.setHeader(header)

        # XXX might want to trigger that to refresh content
        for row in data:
            row['delete'] = 'delete Row'

        # set the table model
        tm = TasksTableModel(data, self._header, self._parent)
        self.setModel(tm)
        try:
            self.model().sort(self._parent._orderCol, self._parent._orderWay)
        except IndexError:
            pass
        # hide vertical header
        self.verticalHeader().setVisible(False)
        #self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

        # set the minimum size
        #~ self.resizeColumnsToContents()
        self.updateWidth()

    def getData(self, row, col):
        #@TODO call a method from model to get this
        return self.model().arraydata[row][self.model().headerData(col)]

    def setHeader(self, header):
        self._header = header + self._extraHeader

    def getColumnNameFromIndex(self, colIndex):
        return self.model().headerData(colIndex)

    def getColumnIndexFromName(self, colName):
        return self._header.index(colName)

    def keyPressEvent(self, e):
        self._parent.keyPressEvent(e)

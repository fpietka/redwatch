# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
import webbrowser, re
from gui.taskstable import TasksTable
from TasksManagement import TasksManagement


class TasksList(QtGui.QWidget):

    def __init__(self, parent, name, data, header, orderCol=0, orderWay=0):
        super(TasksList, self).__init__()

        self._name = name
        self._parent = parent
        self._orderCol = orderCol
        self._orderWay = orderWay

        self._createUI(data, header)

    def _createUI(self, data, header):
        #vertical layout
        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(10)

        #table
        self._table = TasksTable(self, header, data, self._orderCol, self._orderWay)

        #table events
        self._table.doubleClicked.connect(self._doubleClickedRow)
        self._table.clicked.connect(self._clickedRow)

        #put the table in the layout
        vbox.addWidget(self._table)

        #horizontal layout
        hbox = QtGui.QHBoxLayout()
        #textfield
        self.newTicketField = QtGui.QLineEdit()
        self.newTicketField.returnPressed.connect(self._addTickets)

        #button
        newTicketFieldButton = QtGui.QPushButton('Add Ticket')

        #button event
        newTicketFieldButton.clicked.connect(self._addTickets)

        #add the text field and the button in the horizontal layout
        hbox.addWidget(self.newTicketField)
        hbox.addWidget(newTicketFieldButton)

        #add the horizontal layout in the vertical one
        vbox.addLayout(hbox)

        #define the vertical layout as the widget's layout
        self.setLayout(vbox)

    def getTable(self):
        return self._table


    #events methods

    #method called if a cell is clicked
    def _clickedRow(self, cell):
        #first get the corresponding column
        field = self._table.getColumnNameFromIndex(cell.column())

        #get the ticket number corresponding to the row
        ticketIdToRemove = self._table.getData(cell.row(), self._table.getColumnIndexFromName('id'))
        #if user clicked to delete a row, a confirm message must be displayed
        if field == 'delete' and QMessageBox.warning(
            self,
            "Unfollow ticket",
            "Are you sure you want to stop "
            "to follow this ticket ? (" + str(ticketIdToRemove) + ")",
            "Yes", "No", '',
            1, 1
        ) == 0:
            #try to delete the ticket
            if not TasksManagement.removeTicket(self._parent._app, self._name, ticketIdToRemove):
                self._parent.displayMessage('An error occured...')
            else:
                self._parent.refresh()
                self._parent.displayMessage('Ticket deleted')

    #if a cell is double clicked
    def _doubleClickedRow(self, cell):
        field = self._table.getColumnNameFromIndex(cell.column())
        #if the cell is the url, open it in the default webbrowser
        if field == 'id':
            webbrowser.open(self._parent._app._settings.value('redmineUrl') + 'issues/' + str(cell.data()))

    #if the add tickets button is pressed
    def _addTickets(self):
        #get the text field's value
        enteredValue = self.newTicketField.text()
        #get the tickets number in (a ticket number is a int higher thant 999)
        matches = map(int, re.findall('(\d{4,})', enteredValue))

        #if there is no result, an error message is displayed
        if len(matches) <= 0:
            self._parent.displayMessage('No ticket IDs detected')
        else:
            #else, the tickets are added
            #TasksManagement.addTickets return number of added tickets
            nbAddedTickets = TasksManagement.addTickets(self._parent._app, self._name, matches)
            if nbAddedTickets == 0:
                self._parent.displayMessage('No new ticket IDs added')
                self.newTicketField.setText('')
            else:
                #some tickets have been added, a confirm message is displayed
                #the display is refreshed and the textfield is emptied
                self._parent.refresh()
                self._parent.displayMessage('%s Tickets added' % nbAddedTickets)
                self.newTicketField.setText('')

    def setData(self, data, header):
        self._table.setData(data, header)

    def _setColSort(self, col, type):
        if type not in ('defaultTicketsOrderField', 'defaultTicketsOrderWay'):
            raise Exception

        if type == 'defaultTicketsOrderField':
            self._orderCol = col
        else:
            self._orderWay = col

        settingsCol = self._parent._app._settings.dictValue(type)
        if not settingsCol:
            settingsCol = dict()
        if settingsCol.has_key(self._name):
            settingsCol.pop(self._name)
        settingsCol[self._name] = col
        self._parent._app._settings.setValue(type, settingsCol)

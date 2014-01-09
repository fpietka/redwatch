# -*- coding: utf-8 -*-
from core.settings import SettingsException


class TasksManagement:

    @staticmethod
    def getTicketsIds(app):
        tickets = app._settings.value('tickets')
        if not tickets:
            tickets = dict()
        return tickets

    @staticmethod
    def addTickets(app, tabName, ticketsToAdd):
        # XXX use thread here
        try:
            ticketsIds = TasksManagement.getTicketsIds(app)
            if tabName in ticketsIds:
                nbInitTickets = len(ticketsIds[tabName])
            else:
                ticketsIds[tabName] = []
                nbInitTickets = 0
        except:
            # XXX for now
            ticketsIds = {tabName: list()}

        # quick count for now
        # XXX will have to count only valid ticket added
        before = len(ticketsIds[tabName])
        for ticket in ticketsToAdd:
            ticketsIds[tabName].append(ticket)

        ticketsIds[tabName] = sorted(set(ticketsIds[tabName]))
        app._settings.setValue('tickets', ticketsIds)

        return len(ticketsIds[tabName]) - before

    @staticmethod
    def purgeTickets(app, tabName=None, removeTab=False):
        if tabName is not None:
            ticketsIds = TasksManagement.getTicketsIds(app)
            if not removeTab:
                ticketsIds[tabName] = []
            else:
                ticketsIds.pop(tabName)
        else:
            ticketsIds = {}
        app._settings.setValue('tickets', ticketsIds)

    @staticmethod
    def removeTicket(app, tabName, ticketId):
        ticketsIds = TasksManagement.getTicketsIds(app)
        try:
            ticketsIds[tabName].remove(ticketId)
            app._settings.setValue('tickets', ticketsIds)
            return True
        except:
            return False

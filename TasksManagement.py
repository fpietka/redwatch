# -*- coding: utf-8 -*-
from core.settings import SettingsException


class TasksManagement:

    @staticmethod
    def getTicketsIds(app):
        settings = app._settings.dictValue('tickets')
        if not settings:
            raise SettingsException('No settings found')
        return settings

    @staticmethod
    def addTickets(app, tabName, ticketsToAdd):
        # XXX use thread here
        try:
            ticketsIds = TasksManagement.getTicketsIds(app);
            if ticketsIds.has_key(tabName):
                nbInitTickets = len(ticketsIds[tabName])
            else:
                ticketsIds[tabName] = []
                nbInitTickets = 0
        except:
            # XXX for now
            ticketsIds = {tabName: list()}

        for ticket in ticketsToAdd:
            ticketsIds[tabName].append(ticket)

        ticketsIds[tabName] = sorted(set(ticketsIds[tabName]))
        app._settings.setValue('tickets', ticketsIds)

        return len(ticketsIds[tabName])

    @staticmethod
    def purgeTickets(app, tabName = None, removeTab = False):
        if tabName != None:
            ticketsIds = TasksManagement.getTicketsIds(app);
            if not removeTab:
                ticketsIds[tabName] = []
            else:
                ticketsIds.pop(tabName)
        else:
            ticketsIds = {}
        app._settings.setValue('tickets', ticketsIds)


    @staticmethod
    def removeTicket(app, tabName, ticketId):
        ticketsIds = TasksManagement.getTicketsIds(app);

        try:
            ticketsIds[tabName].remove(str(ticketId))
            app._settings.setValue('tickets', ticketsIds)
            return True
        except:
            return False

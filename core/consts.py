# -*- coding: utf-8 -*-

import os

# settings infos
appname = 'redmine-tickets'
company = 'put-your-company-name-here'

# XXX to configure
redmineApiKey = ""
redmineUrl = ""

rootPath = os.path.join(os.path.dirname(__file__), '..')
mainIcon = rootPath + '/resources/redmine_fluid_icon.png'
exitIcon = rootPath + '/resources/redmine_fluid_icon.png'
purgeIcon = rootPath + '/resources/redmine_fluid_icon.png'

defaultTicketsOrderField = 0
defaultTicketsOrderWay = 1

versionFile = os.path.join(rootPath, 'VERSION')

serverUrls = {}
serverUrls['ticketUrl'] = ""
serverUrls['checkVersion'] = {'host': "", 'uri': ''}

#settings
SETTINGS_TYPE_COLOR = 'color'
SETTINGS_TYPE_BOOLEAN = 'boolean'
SETTINGS_TYPE_INT = 'int'

# period of the watching thread
settings = {}
settings['refresh_interval'] = {'value': 60, 'label': 'Refresh Interval', 'type': SETTINGS_TYPE_INT}

settings['standardBackgroundColor'] = {'value': '#fdf6e3', 'label': 'Standard background Color', 'type': SETTINGS_TYPE_COLOR}
settings['standardForegroundColor'] = {'value': '#073642', 'label': 'Standard foreground Color', 'type': SETTINGS_TYPE_COLOR}


settings['closedColor'] = {'value': '#eee8d5', 'label': 'Closed Color', 'type': SETTINGS_TYPE_COLOR}  # grey on white
settings['toPutOnlineColor'] = {'value': '#dc322f', 'label': 'To put online Color', 'type': SETTINGS_TYPE_COLOR}  # red
settings['resolvedColor'] = {'value': '#859900', 'label': 'Resolved Color', 'type': SETTINGS_TYPE_COLOR}  # green
settings['toTestColor'] = {'value': '#268bd2', 'label': 'To test Color', 'type': SETTINGS_TYPE_COLOR}  # blue
settings['waitingInfosColor'] = {'value': '#b58900', 'label': 'Waiting infos Color', 'type': SETTINGS_TYPE_COLOR}  # yellow
settings['newColor'] = {'value': '#2aa198', 'label': 'new Color', 'type': SETTINGS_TYPE_COLOR}  #light blue

settings['windowResizable'] = {'value': False, 'label': 'Window resizable', 'type': SETTINGS_TYPE_BOOLEAN}

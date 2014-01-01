# -*- coding: utf-8 -*-

import os

# settings infos
appname = 'redmine-tickets'
company = 'nextcode'

rootPath = os.path.join(os.path.dirname(__file__), '..')
mainIcon = rootPath + '/resources/redmine_fluid_icon.png'
exitIcon = rootPath + '/resources/glyphicons_388_exit.png'
purgeIcon = rootPath + '/resources/redmine_fluid_icon.png'

settingsIcon= rootPath + '/resources/glyphicons_280_settings.png'
colorSettingsIcon = rootPath + '/resources/glyphicons_092_tint.png'

defaultTicketsOrderField = 0
defaultTicketsOrderWay = 1

versionFile = os.path.join(rootPath, 'VERSION')

# Solarized color theme
COLORS = (
    (0, 43, 54),
    (7, 54, 66),
    (88, 110, 117),
    (101, 123, 131),
    (131, 148, 150),
    (147, 161, 161),
    (238, 232, 213),
    (253, 246, 227),
    (181, 137, 0),
    (203, 75, 22),
    (220, 50, 47),
    (211, 54, 130),
    (108, 113, 196),
    (38, 139, 210),
    (42, 161, 152),
    (133, 153, 0)
)

#settings
SETTINGS_TYPE_COLOR = 'color'
SETTINGS_TYPE_BOOLEAN = 'boolean'
SETTINGS_TYPE_INT = 'int'

# period of the watching thread
settings = {}
settings['refresh_interval'] = {'value': 60, 'label': 'Refresh Interval', 'type': SETTINGS_TYPE_INT}
settings['windowResizable'] = {'value': False, 'label': 'Window resizable', 'type': SETTINGS_TYPE_BOOLEAN}

#!/usr/bin/python
# -*- coding: utf8 -*-

import sip
# use regular strings
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from gui.application import Application
import os
import sys
import getopt


def usage():
    """
    Display script documentation
    """
    print __doc__


def main(argv):
    # command-line options
    shortOptions = 'd:'
    longOptions = ('debug')

    # handle command-line parameters
    try:
        options, remains = getopt.getopt(argv, shortOptions, longOptions)
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    debug = False
    for opt, arg in options:
        if opt in ('-d', '--debug'):
            debug = True

    app = Application(debug)

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/python
# -*- coding: utf8 -*-

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
    shortOptions = 'v:'
    longOptions = ('verbose')

    # handle command-line parameters
    try:
        options, remains = getopt.getopt(argv, shortOptions, longOptions)
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in options:
        if opt in ('-v', '--verbose'):
            global verbose
            verbose = True

    app = Application()

if __name__ == "__main__":
    main(sys.argv[1:])

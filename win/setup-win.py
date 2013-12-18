#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to build a .exe file on windows.

Install py2exe and run
python -OO win\setup-win.py py2exe
"""

# Dependences

# Add the parent directory to python modules search path.
# This is needed because this build script is in a subdirectory
# (so "from src import *" won't work without this quirck)
import sys,os
sys.path.append(os.path.realpath(os.path.dirname(sys.argv[0]) + '\\..'))

from distutils.core import setup
import py2exe

# le script principal
if __name__ == "__main__":
    setup(
        name="Redmine Tickets",
        description="Redmine tickets application",
        version="",
        windows=[
            {
                "script": "main.py",
                "dest_base": "RedmineTickets",
            }
        ],
        options = {
            "py2exe": {
                "optimize": 2,
                "packages": ["encodings"],
                "includes": [
                    "sip"
                ],
                # this is a workaround msvc dlls problems with
                # python 2.6 . See also the comment in manifest file.
                "dll_excludes": [
                    "MSVCP90.dll",
                ]
            }
        },
        data_files=[
            (
                ".",
                [
                    "win/RedmineTickets.exe.manifest",
                ],
            ),

        ]
    )

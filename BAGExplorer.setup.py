"""
Setup script for BAGExplorer on Mac OS X.

Usage:
    python BAGExplorer.setup.py py2app

The output is BAGExplorer.app, in the dist/ folder.

After running setp.py and verifying the install image, run:
    appdmg spec.json BAGExplorer.dmg
To create dmg install file.  The appdmg utility can be installed from npm.

PyInstaller, for Windows and Linux distribution, does not use setup.py.
"""

from setuptools import setup

APP = ['BAGExplorer.py']
DATA_FILES = []
PLIST = {   "CFBundleDocumentTypes": [ { "CFBundleTypeExtensions": ["bag",],
                                      "CFBundleTypeName": "BAG Data File",
                                      "CFBundleTypeRole": "Viewer"} ],
            "CFBundleIdentifer": "org.hydroffice.bag",
            "CFBundleDisplayName": "BAGExplorer",
            "CFBundleVersion": "0.1.0" }

# ARGV emulation interacts badly with wxPython on Mac... it "eats" events
# when the program starts up and causes windows not to be displayed.
OPTIONS = { 'argv_emulation': False,
            'excludes': ['scipy', 'PyQt4', 'mpi4py'],
            'matplotlib_backends': ['wxagg'],
            'iconfile': 'BAGExplorer.icns',
            'plist': PLIST }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

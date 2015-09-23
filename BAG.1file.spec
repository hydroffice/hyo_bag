# -*- mode: python -*-
from PyInstaller import is_win, is_darwin
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE

import os
import sys


exe_file = 'BAG.out'
if is_win:
    exe_file = 'BAG.exe'
elif is_darwin:
    exe_file = 'BAG'

icon_file = 'BAG.ico'
if is_darwin:
    icon_file = 'BAG.icns'

# hydro-package data
media_tree = Tree('hydroffice/bag/gui/media', prefix='hydroffice/bag/gui/media')
manual_tree = Tree('hydroffice/bag/docs', prefix='hydroffice/bag/docs', excludes=['*.docx',])
# pkg_data = []

# run the analysis
block_cipher = None
a = Analysis(['BAG.py'],
             pathex=[],
             #pathex=[],
             binaries=None,
             datas=None,
             hiddenimports=['netCDF4.utils', 'netcdftime'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)

for d in a.binaries:
    if "system32\\pywintypes34.dll" in d[1]:
        a.binaries.remove(d)
    if "system32\\pywintypes27.dll" in d[1]:
        a.binaries.remove(d)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          media_tree,
          manual_tree,
          name=exe_file,
          debug=False,
          strip=None,
          upx=True,
          console=True, icon=icon_file)
if is_darwin:
    app = BUNDLE(exe,
                 name='BAG.app',
                 icon=icon_file,
                 bundle_identifier=None)

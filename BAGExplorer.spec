# -*- mode: python -*-
a = Analysis(['BAGExplorer.py'],
             pathex=[],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

# The following block is necessary to prevent a hard crash when launching
# the resulting .exe file
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
# hydro-package data
media_tree = Tree('hydroffice/bag/gui/media', prefix='hydroffice/bag/gui/media')
manual_tree = Tree('hydroffice/bag/docs', prefix='hydroffice/bag/docs', excludes=['*.docx',])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          media_tree,
          manual_tree,
          name='BAGExplorer.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False , icon='hydroffice/bag/gui/media/BAGExplorer.ico')

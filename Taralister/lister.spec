# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['lister.py'],
             pathex=['C:\\Users\\Danangjoyoo\\Desktop\\expython\\Taralister'],
             binaries=[],
             datas=[('assets/*.png','assets'),('assets/*.ico','assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pygame'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/pygame/", prefix= "pygame")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/xml/", prefix= "xml")
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TARA-LISTER',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='assets/tl.ico' )

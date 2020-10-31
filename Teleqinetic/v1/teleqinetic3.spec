# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Danangjoyoo\\Desktop\\expython\\Teleqinetic\\v1\\one dir test'],
             binaries=[],
             datas=[('assets/*.ico','assets'),
             		('assets/init/*.png','init'),('assets/init/*.ico','assets'),
             		('assets/main/*.png','main'),
             		('assets/instruction/*.png','instruction')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pygame','qt5','cv2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TeleQinetic',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False, icon='assets/init/logo1.ico' )
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/pygame/", prefix= "pygame")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/cv2/", prefix= "cv2")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/xml/", prefix= "xml")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='TeleQinetic v1.93')

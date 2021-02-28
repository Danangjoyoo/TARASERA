# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['TScanMain.py'],
             pathex=['C:\\Users\\Danangjoyoo\\Desktop\\expython\\Tarascanner\\v0'],
             binaries=[],
             datas=[('assets/*.ico','assets'),('assets/*.png','assets')],
             hiddenimports=['six','csv'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['qt5','cv2','pyzbar','pandas','numpy','pytz','dateutil','six','csv'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TaraScanner',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False, icon='assets/tscan.ico')
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/pyzbar/", prefix= "pyzbar")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/pytz/", prefix= "pytz")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/dateutil/", prefix= "dateutil")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/pandas/", prefix= "pandas")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/numpy/", prefix= "numpy")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/site-packages/cv2/", prefix= "cv2")
a.datas += Tree("E:/Program Files/Python/Python37/Lib/xml/", prefix= "xml")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='TaraScanner v0.2.25')

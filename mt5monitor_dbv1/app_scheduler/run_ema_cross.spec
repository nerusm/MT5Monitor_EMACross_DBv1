# -*- mode: python ; coding: utf-8 -*-


import sys
from os import path
site_packages = next(p for p in sys.path if 'site-packages' in p)
block_cipher = None


a = Analysis(['run_ema_cross.py'],
             pathex=['C:\\Suren\\Projects\\MT5Monitor_EMACross_DBv1\\mt5monitor_dbv1\\app_scheduler'],
             binaries=[],
             datas=[(path.join(site_packages,"tzdata"),"tzdata")],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
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
          name='run_ema_cross',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run_ema_cross')

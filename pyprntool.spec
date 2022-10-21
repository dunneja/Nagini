# -*- mode: python ; coding: utf-8 -*-
# pyinstaller --clean --onefile --icon=icons\printer64.ico prndatac.py functions\__init__.py functions\csvfunc.py functions\dirfunc.py functions\logfunc.py functions\snmpfunc.py
# .\verpatch.exe pyprntool.exe 1.0.0.0 /va /pv 1.0.0.0 /s description "HP Xerox Printer Data Collection Tool" /s product "HP Py Printer Data Collection Tool" /s copyright "Copyright - HP Inc 2022" /s company "HP Inc (UK&I)"

block_cipher = None

a = Analysis(['prngui.py','prndatac.py', 'prnconnc.py', 'functions\\__init__.py', 'functions\\csvfunc.py', 'functions\\csvtable.py', 'functions\\dirfunc.py', 'functions\\logfunc.py', 'functions\\snmpfunc.py'],
             pathex=[],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='prndatac',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icons\\printer64.ico')
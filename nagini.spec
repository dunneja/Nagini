# -*- mode: python ; coding: utf-8 -*-
# pyinstaller --clean --onefile --icon=icons\printer64.ico nagini.py __init__.py __main__.py core\__init__.py  core\prn_connc.py core\prn_datac.py core\prn_snmpc.py functions\__init__.py functions\csv_func.py functions\dir_func.py functions\log_func.py functions\snmp_func.py functions\cfg_func.py gui\__init__.py gui\gui_csv_view.py gui\gui_func.py gui\gui_help.py gui\prntool.py

block_cipher = None


a = Analysis(
    ['nagini.py', '__init__.py', '__main__.py', 'core\\__init__.py', 'core\\prn_connc.py', 'core\\prn_datac.py', 'core\\prn_snmpc.py', 'functions\\__init__.py', 'functions\\csv_func.py', 'functions\\dir_func.py', 'functions\\log_func.py', 'functions\\snmp_func.py', 'functions\\cfg_func.py', 'gui\\__init__.py', 'gui\\gui_csv_view.py', 'gui\\gui_func.py', 'gui\\gui_help.py', 'gui\\gui_prntool.py'],
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
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='nagini',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons\\printer64.ico'],
)

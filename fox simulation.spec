# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[('data.json', '.'), ('simoutput.json', '.'), ('assets/background.png', 'assets'), ('assets/enc1.png', 'assets'), ('assets/enc2.png', 'assets'), ('assets/enc3.png', 'assets'), ('assets/mainbackground.png', 'assets'), ('assets/smalltree.png', 'assets')],
    hiddenimports=['math'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='fox simulation',
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
    icon=['assets/sandy_pines.png'],
)

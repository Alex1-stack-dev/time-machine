# PyInstaller spec to bundle main.py and include the public folder
# Usage: pyinstaller --noconfirm raceclock.spec
# Adjust icon or other options as needed.
# Note: On macOS you may want onefile=False and a --windowed build for app bundle creation.

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
from PyInstaller.utils.hooks import collect_submodules

# Include all package modules from your repo if needed; example below collects submodules
hiddenimports = collect_submodules('pkg_resources') if 'pkg_resources' in collect_submodules.__module__ else []

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # include the UI static files
        ('public', 'public'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='time-machine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # set to True if you want a console
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='time-machine'
)

# PyInstaller spec for building time-machine and updater into standalone .exe files.
# Build: pyinstaller --clean pyinstaller.spec
# This spec builds two EXEs (onefile) using two a-level specs.
block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/splash.png', 'assets')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[]
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
    console=False,
    icon=None
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='time-machine')

# Updater single file
a_up = Analysis(
    ['src/updater.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['psutil'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[]
)
pyz_up = PYZ(a_up.pure, a_up.zipped_data, cipher=block_cipher)
exe_up = EXE(
    pyz_up,
    a_up.scripts,
    [],
    exclude_binaries=True,
    name='time-machine-updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None
)
coll_up = COLLECT(exe_up, a_up.binaries, a_up.zipfiles, a_up.datas, strip=False, upx=True, name='time-machine-updater')

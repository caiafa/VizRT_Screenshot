import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

exe = [Executable(
    script='screenshotMaker.py',
    base=base,
    icon="icon.ico",
    compress=True,
    copyDependentFiles=True,
    appendScriptToExe=False,
    appendScriptToLibrary=False,
)]

setup(name='Screenshot Maker',
      version='0.3',
      description='Screenshot Maker',
      options=options,
      executables=exe, requires=['requests', 'PIL', 'requests', 'PyQt5', 'xlrd', 'cx_Freeze']
      )

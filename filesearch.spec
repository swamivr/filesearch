# PyInstaller spec file for building a standalone filesearch executable.
# Usage:  pyinstaller filesearch.spec

import importlib
import os

pypdf_path = os.path.dirname(importlib.import_module("pypdf").__file__)

a = Analysis(
    ["src/filesearch/__main__.py"],
    pathex=["src"],
    datas=[],
    hiddenimports=["pypdf"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="filesearch",
    debug=False,
    strip=False,
    upx=True,
    console=True,
)

# PyInstaller spec file for building a standalone filesearch executable.
# Usage:  pyinstaller filesearch.spec

a = Analysis(
    ["entry_point.py"],
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

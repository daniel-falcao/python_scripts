"""Builder script to create an executable
for the Receitas project using PyInstaller."""

import os

os.system(
    "pyinstaller --onefile --windowed "
    "--add-data 'parsers:parsers' "
    "app.py"
)

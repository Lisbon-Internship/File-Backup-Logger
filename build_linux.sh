#!/bin/bash
echo "Installing PyInstaller..."
pip install pyinstaller

echo "Building executable for Linux..."
# Note: Linux uses ':' as path separator for --add-data
pyinstaller --noconfirm --onefile --windowed --icon=icon.png --add-data="icon.png:." --add-data="icon.ico:." --name="FileBackupLogger" main.py

echo "Build complete. Executable is located in the 'dist' folder."

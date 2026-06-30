@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable for Windows...
:: Note: Windows uses ';' as path separator for --add-data
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico --add-data "icon.png;." --add-data "icon.ico;." --name="FileBackupLogger" main.py

echo Build complete. Executable is located in the 'dist' folder.
pause

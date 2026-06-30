#!/bin/bash
echo "Installing PyInstaller..."
pip install pyinstaller

echo "Building executable for Linux..."
# Note: Linux uses ':' as path separator for --add-data
pyinstaller --noconfirm --onefile --windowed --icon=icon.png --add-data="icon.png:." --add-data="icon.ico:." --name="FileBackupLogger" main.py

echo "Build complete. Executable is located in the 'dist' folder."

echo "Generating .desktop file..."
APP_DIR="$(pwd)"
EXEC_PATH="$APP_DIR/dist/FileBackupLogger"
ICON_PATH="$APP_DIR/icon.png"
DESKTOP_FILE="FileBackupLogger.desktop"

cat <<EOF > $DESKTOP_FILE
[Desktop Entry]
Version=1.0
Name=File Backup Logger
Comment=A simple file backup utility with GUI
Exec=$EXEC_PATH
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;System;
EOF

chmod +x $DESKTOP_FILE
echo "Desktop file generated: $DESKTOP_FILE"

echo "Installing to ~/.local/share/applications/ so it appears in your app menu..."
mkdir -p ~/.local/share/applications/
cp $DESKTOP_FILE ~/.local/share/applications/
echo "Installation complete! You can now launch it from your Linux application menu."

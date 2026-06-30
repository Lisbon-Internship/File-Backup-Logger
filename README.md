# File Backup Logger

A Python-based utility with a Graphical User Interface (GUI) to back up files and directories with versioning, optional ZIP compression, and logging capabilities.

## Features
- **Object-Oriented Design:** Clean and maintainable codebase.
- **GUI Interface:** Built with Tkinter for easy selection of source and destination folders.
- **Versioning:** Automatically appends timestamps (down to the millisecond) to backup folders or ZIP files (e.g., `backup_project_2026-06-30_143844_789`).
- **Compression:** Option to back up directories as standard copies or ZIP compressed files.
- **Configuration Persistence:** Remembers your last used source, destination, and ZIP preference between runs using a `config.json` file.
- **Logging:** Keeps a detailed record of backups, including file counts and duration, in `backup.log`.

## Requirements
- Python 3.x (Built-in libraries only: `tkinter`, `shutil`, `zipfile`, `json`, `logging`, `datetime`, `threading`)

## Getting Started

1. Clone or download this repository.
2. Ensure you have Python installed on your system. On Linux/macOS, `tkinter` might require a separate installation depending on your distribution (e.g., `sudo apt install python3-tk`).
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Open the application.
2. Click **Browse** next to **Source Directory** to select the folder you want to back up.
3. Click **Browse** next to **Destination Directory** to choose where the backup should be saved.
4. Toggle **Compress to ZIP** if you want the backup to be compressed into a `.zip` archive.
5. Click **Backup Now**.
6. Check `backup.log` in the application directory for a detailed report of the operation.

## Building Executables
You can create standalone executable files (no Python installation required to run) using the provided scripts. These scripts use `pyinstaller` and include the application icon.

**For Linux:**
1. Open a terminal in the project directory.
2. Run `./build_linux.sh`
3. The executable will be generated in the `dist/` folder as `FileBackupLogger`.

**For Windows:**
1. Open a command prompt or PowerShell in the project directory.
2. Run `build_windows.bat`
3. The executable will be generated in the `dist/` folder as `FileBackupLogger.exe`.

## Architecture
- `main.py`: The entry point that initializes the application.
- `gui.py`: Contains the `BackupApp` class handling the Tkinter user interface and user interactions.
- `backup.py`: Contains the `BackupManager` class responsible for copying, zipping, file system interaction, and logging.
- `config.py`: Contains the `ConfigManager` class to load and save user preferences to `config.json`.

## Configuration
All the logs and configuration are stored in `~/.file_backup_logger`

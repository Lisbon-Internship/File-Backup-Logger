import os
import shutil
import zipfile
import logging
from datetime import datetime
import time
from pathlib import Path

# Use the user's home directory for logs
APP_DIR = os.path.join(str(Path.home()), ".file_backup_logger")
os.makedirs(APP_DIR, exist_ok=True)
LOG_FILE = os.path.join(APP_DIR, "backup.log")

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupManager:
    def __init__(self):
        pass

    def _generate_version_name(self):
        """Generates a version string based on current date with milliseconds."""
        # Format: YYYY-MM-DD_HHMMSS_mmm
        now = datetime.now()
        # %f gives microseconds, so we slice to get milliseconds
        ms = now.strftime('%f')[:3]
        return now.strftime(f'%Y-%m-%d_%H%M%S_{ms}')

    def _count_files(self, directory):
        """Counts the total number of files in a directory."""
        total = 0
        for root, _, files in os.walk(directory):
            total += len(files)
        return total

    def perform_backup(self, source, destination, use_zip=False):
        """
        Performs the backup operation.
        Returns a tuple (success: bool, message: str)
        """
        if not source or not os.path.exists(source):
            msg = f"Source directory '{source}' does not exist."
            logging.error(msg)
            return False, msg

        if not destination or not os.path.exists(destination):
            msg = f"Destination directory '{destination}' does not exist."
            logging.error(msg)
            return False, msg

        version_name = self._generate_version_name()
        base_name = os.path.basename(os.path.normpath(source))
        backup_folder_name = f"backup_{base_name}_{version_name}"
        
        target_path = os.path.join(destination, backup_folder_name)

        start_time = time.time()
        file_count = self._count_files(source)

        try:
            if use_zip:
                zip_path = f"{target_path}.zip"
                logging.info(f"Starting ZIP backup of '{source}' to '{zip_path}'")
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Create a relative path for the zip file to avoid absolute paths inside zip
                            rel_path = os.path.relpath(file_path, os.path.dirname(source))
                            zipf.write(file_path, rel_path)
                            
                duration = time.time() - start_time
                msg = f"ZIP Backup completed successfully. Files: {file_count}, Time: {duration:.2f}s"
                logging.info(msg)
                return True, msg
            else:
                logging.info(f"Starting plain copy backup of '{source}' to '{target_path}'")
                shutil.copytree(source, target_path)
                
                duration = time.time() - start_time
                msg = f"Copy Backup completed successfully. Files: {file_count}, Time: {duration:.2f}s"
                logging.info(msg)
                return True, msg

        except PermissionError as e:
            msg = f"Permission denied during backup: {e}"
            logging.error(msg)
            return False, msg
        except Exception as e:
            msg = f"An unexpected error occurred during backup: {e}"
            logging.error(msg)
            return False, msg

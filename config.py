import json
import os
from pathlib import Path

# Use the user's home directory for config
APP_DIR = os.path.join(str(Path.home()), ".file_backup_logger")
os.makedirs(APP_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(APP_DIR, "config.json")

class ConfigManager:
    def __init__(self):
        self.config = {
            "source_dir": "",
            "destination_dir": "",
            "use_zip": False
        }
        self.load_config()

    def load_config(self):
        """Loads configuration from the JSON file."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.config.update(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        """Saves current configuration to the JSON file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

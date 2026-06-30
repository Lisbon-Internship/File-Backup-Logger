import tkinter as tk
from tkinter import filedialog, messagebox
import platform
import os
import sys
from config import ConfigManager
from backup import BackupManager
import threading

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Backup Logger")
        self.root.geometry("500x300")
        
        try:
            if platform.system() == 'Windows':
                self.root.iconbitmap(get_resource_path('icon.ico'))
            else:
                self.icon_img = tk.PhotoImage(file=get_resource_path('icon.png'))
                self.root.iconphoto(True, self.icon_img)
        except Exception as e:
            pass # Ignore if icon is missing

        self.config_manager = ConfigManager()
        self.backup_manager = BackupManager()

        self._setup_ui()
        self._load_preferences()

    def _setup_ui(self):
        # Source Directory
        tk.Label(self.root, text="Source Directory:").pack(pady=(10, 0), padx=10, anchor='w')
        self.source_frame = tk.Frame(self.root)
        self.source_frame.pack(fill='x', padx=10)
        
        self.source_entry = tk.Entry(self.source_frame)
        self.source_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.source_btn = tk.Button(self.source_frame, text="Browse", command=self._browse_source)
        self.source_btn.pack(side='right')

        # Destination Directory
        tk.Label(self.root, text="Destination Directory:").pack(pady=(10, 0), padx=10, anchor='w')
        self.dest_frame = tk.Frame(self.root)
        self.dest_frame.pack(fill='x', padx=10)
        
        self.dest_entry = tk.Entry(self.dest_frame)
        self.dest_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.dest_btn = tk.Button(self.dest_frame, text="Browse", command=self._browse_dest)
        self.dest_btn.pack(side='right')

        # ZIP Checkbox
        self.use_zip_var = tk.BooleanVar()
        self.zip_check = tk.Checkbutton(self.root, text="Compress to ZIP", variable=self.use_zip_var, command=self._save_preferences)
        self.zip_check.pack(pady=10, padx=10, anchor='w')

        # Backup Button
        self.backup_btn = tk.Button(self.root, text="Backup Now", command=self._start_backup, bg="lightblue")
        self.backup_btn.pack(pady=15)

        # Status Label
        self.status_label = tk.Label(self.root, text="Ready", fg="gray")
        self.status_label.pack(side='bottom', pady=10)

    def _load_preferences(self):
        self.source_entry.insert(0, self.config_manager.get("source_dir", ""))
        self.dest_entry.insert(0, self.config_manager.get("destination_dir", ""))
        self.use_zip_var.set(self.config_manager.get("use_zip", False))

    def _save_preferences(self, *args):
        self.config_manager.set("source_dir", self.source_entry.get())
        self.config_manager.set("destination_dir", self.dest_entry.get())
        self.config_manager.set("use_zip", self.use_zip_var.get())

    def _browse_source(self):
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, directory)
            self.defocus_and_save()

    def _browse_dest(self):
        directory = filedialog.askdirectory(title="Select Destination Directory")
        if directory:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, directory)
            self.defocus_and_save()
            
    def defocus_and_save(self):
        self.root.focus_set()
        self._save_preferences()

    def _start_backup(self):
        self._save_preferences()
        source = self.source_entry.get()
        destination = self.dest_entry.get()
        use_zip = self.use_zip_var.get()

        if not source or not destination:
            messagebox.showwarning("Missing Information", "Please select both source and destination directories.")
            return

        self.backup_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Backing up...", fg="blue")
        
        # Run in a separate thread to keep GUI responsive
        threading.Thread(target=self._run_backup_thread, args=(source, destination, use_zip), daemon=True).start()

    def _run_backup_thread(self, source, destination, use_zip):
        success, message = self.backup_manager.perform_backup(source, destination, use_zip)
        
        # Update GUI from main thread
        self.root.after(0, self._backup_complete, success, message)
        
    def _backup_complete(self, success, message):
        self.backup_btn.config(state=tk.NORMAL)
        if success:
            self.status_label.config(text="Backup successful", fg="green")
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(text="Backup failed", fg="red")
            messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()

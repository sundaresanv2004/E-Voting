import os
import platform
import subprocess
import sys
import zipfile
from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, messagebox


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Installer")

        self.progress_label = tk.Label(root, text="Starting installation...")
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

        self.progress_text = tk.Text(root, height=10, wrap='word')
        self.progress_text.pack(fill=tk.BOTH, padx=20, pady=10)

        self.run_installation()

    def log(self, message):
        self.progress_text.insert(tk.END, message + '\n')
        self.progress_text.see(tk.END)
        self.root.update()

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.root.update()

    def run_installation(self):
        threading.Thread(target=self.installation_process).start()

    def installation_process(self):
        try:
            self.log("Determining platform and setting path...")
            if platform.system() == "Windows":
                path = Path(os.getenv('APPDATA')) / 'E-Voting'
            elif platform.system() == 'Darwin':
                path = Path.home() / 'Library' / 'Application Support' / 'E-Voting'
            else:
                self.log("Unsupported platform")
                return

            run_path = path / 'run'
            venv_path = run_path / 'venv'
            requirements_path = Path('requirements.txt')
            app_version = '6.08'
            zip_filename = f"{app_version}.zip"
            zip_path = Path(zip_filename)
            versions_path = path / 'versions'
            extract_to = versions_path / app_version

            self.log("Ensuring the installation path exists...")
            path.mkdir(parents=True, exist_ok=True)

            self.update_progress(10)

            if not run_path.exists():
                self.log("'run' directory does not exist. Creating...")
                run_path.mkdir()
                self.create_virtualenv_and_install_requirements(venv_path, requirements_path)
            else:
                self.log("'run' directory already exists, skipping virtual environment creation.")

            self.update_progress(50)

            self.log("Ensuring the versions path exists...")
            versions_path.mkdir(parents=True, exist_ok=True)

            if extract_to.exists():
                self.log(f"Version {app_version} is already installed.")
                messagebox.showinfo("Already Installed", f"Version {app_version} is already installed.")
            else:
                if zip_path.exists():
                    self.log(f"Extracting {zip_filename} to {extract_to}...")
                    self.extract_and_move_zip(zip_path, extract_to)
                    self.log("Installation completed successfully.")
                    messagebox.showinfo("Success", "Installation completed successfully.")
                else:
                    self.log(f"Zip file {zip_filename} does not exist, skipping extraction.")

            self.update_progress(100)
            self.root.after(2000, self.root.destroy)
        except subprocess.CalledProcessError as e:
            self.log(f"Error during subprocess call: {e}")
            messagebox.showerror("Subprocess Error", f"An error occurred during subprocess execution: {e}")
            self.root.after(2000, self.root.destroy)
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
            self.root.after(2000, self.root.destroy)

    def create_virtualenv_and_install_requirements(self, venv_path, requirements_path):
        self.log(f"Creating virtual environment at {venv_path}...")
        subprocess.check_call([sys.executable, '-m', 'venv', str(venv_path)])
        pip_executable = venv_path / 'bin' / 'pip' if platform.system() == 'Darwin' else venv_path / 'Scripts' / 'pip.exe'

        self.log(f"Installing requirements from {requirements_path}...")
        try:
            subprocess.check_call([str(pip_executable), 'install', '-r', str(requirements_path)])
        except subprocess.CalledProcessError as e:
            self.log(f"Error installing requirements: {e}")
            raise

    def extract_and_move_zip(self, zip_path, extract_to):
        self.log(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        self.log(f"Moving contents from the intermediate extraction folder...")
        intermediate_folder = extract_to / '6.08'
        if intermediate_folder.exists() and intermediate_folder.is_dir():
            for item in intermediate_folder.iterdir():
                target_path = extract_to / item.name
                item.rename(target_path)
            intermediate_folder.rmdir()


if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()

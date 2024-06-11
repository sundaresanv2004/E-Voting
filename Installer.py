import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import zipfile
import shutil

# Determine the OS and set the path
if platform.system() == "Windows":
    os_sys = "Windows"
    path = os.getenv('APPDATA') + r'/E-Voting'
elif platform.system() == 'Darwin':
    os_sys = platform.system()
    path = os.path.expanduser('~') + r"/Library/Application Support/E-Voting"
else:
    raise EnvironmentError("Unsupported platform")

# Set version and paths
version = "6.08"
run_folder = os.path.join(path, 'run')
versions_folder = os.path.join(path, 'versions')
local_zip = '6.08.zip'  # Change this to your actual local zip file path


def check_and_extract_version():
    if not os.path.exists(versions_folder):
        os.makedirs(versions_folder)

    version_folder = os.path.join(versions_folder, version)
    if not os.path.exists(version_folder):
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(versions_folder)
            extracted_folder_name = zip_ref.namelist()[0].split('/')[0]
            os.rename(os.path.join(versions_folder, extracted_folder_name), version_folder)

    # Move the pre-created virtual environment
    run_env_folder = os.path.join(version_folder, 'run')
    if os.path.exists(run_env_folder):
        shutil.move(run_env_folder, run_folder)


def on_install():
    progress.start()
    try:
        check_and_extract_version()
        progress.stop()
        messagebox.showinfo("Success", "Installation completed successfully!")
        root.after(1000, root.destroy)  # Close the window after 1 second
    except Exception as e:
        progress.stop()
        messagebox.showerror("Error", str(e))


# Tkinter GUI setup
root = tk.Tk()
root.title("E-Voting Version-6.08 Test")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="E-Voting Version-6.08 Test").grid(row=0, column=0, columnspan=2, pady=10)

progress = ttk.Progressbar(frame, mode='indeterminate')
progress.grid(row=1, column=0, columnspan=2, pady=10)

install_button = ttk.Button(frame, text="Install", command=on_install)
install_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

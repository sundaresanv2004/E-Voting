import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import zipfile
import shutil
import subprocess

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
requirements_file = 'requirements.txt'  # Change this to your actual requirements.txt file path


def create_virtualenv_and_install():
    # Create run folder and virtual environment
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)
        python_executable = shutil.which("python3" if os_sys != "Windows" else "python")
        if not python_executable:
            raise EnvironmentError("Python executable not found. Please install Python.")
        subprocess.check_call([python_executable, "-m", "venv", run_folder])

    # Determine the pip executable path
    pip_executable = os.path.join(run_folder, 'bin', 'pip') if os_sys != "Windows" else os.path.join(run_folder,
                                                                                                     'Scripts',
                                                                                                     'pip.exe')

    # Verify the pip executable exists
    if not os.path.exists(pip_executable):
        raise FileNotFoundError(f"{pip_executable} not found. Virtual environment may not have been created correctly.")

    # Install requirements
    subprocess.check_call([pip_executable, 'install', '-r', requirements_file])


def check_and_extract_version():
    if not os.path.exists(versions_folder):
        os.makedirs(versions_folder)

    version_folder = os.path.join(versions_folder, version)
    if not os.path.exists(version_folder):
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(versions_folder)
            extracted_folder_name = zip_ref.namelist()[0].split('/')[0]
            os.rename(os.path.join(versions_folder, extracted_folder_name), version_folder)


def on_install():
    progress.start()
    try:
        create_virtualenv_and_install()
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

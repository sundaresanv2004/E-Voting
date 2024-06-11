import os
import platform
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
version_folder = os.path.join(versions_folder, version)

# Function to run main.py
def run_main_py(version_folder):
    main_py_path = os.path.join(version_folder, 'main.py')
    if os.path.exists(main_py_path):
        python_executable = os.path.join(run_folder, 'bin', 'python') if os_sys != "Windows" else os.path.join(run_folder, 'Scripts', 'python.exe')
        if not os.path.exists(python_executable):
            raise FileNotFoundError(f"{python_executable} not found. Virtual environment may not have been created correctly.")
        subprocess.run([python_executable, main_py_path])
    else:
        print("main.py not found in the version folder.")

def main():
    if os.path.exists(version_folder):
        run_main_py(version_folder)
    else:
        print(f"Version folder for version {version} not found.")

if __name__ == "__main__":
    main()

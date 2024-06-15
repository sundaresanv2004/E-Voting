import os
import platform
import subprocess
from pathlib import Path
import sys


def run_main_script():
    app_version = '6.08'  # Specify the app version to run

    # Determine the platform and set paths accordingly
    if platform.system() == "Windows":
        base_path = Path(os.getenv('APPDATA')) / 'E-Voting'
        python_executable = base_path / 'run' / 'venv' / 'Scripts' / 'python.exe'
    elif platform.system() == 'Darwin':
        base_path = Path.home() / 'Library' / 'Application Support' / 'E-Voting'
        python_executable = base_path / 'run' / 'venv' / 'bin' / 'python'
    else:
        print("Unsupported platform")
        return

    current_version_path = base_path / 'versions' / app_version / 'main.py'

    if not current_version_path.exists():
        print(f"main.py not found in {current_version_path}")
        return

    # Run the main.py script using the virtual environment's python executable
    try:
        print(f"Running E-Voting Version: {app_version}...")
        subprocess.check_call([str(python_executable), str(current_version_path)])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running main.py: {e}")


if __name__ == "__main__":
    run_main_script()

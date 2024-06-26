import os
import platform
import subprocess
from pathlib import Path

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
        print(f"Running E-Voting version: {app_version}...")
        result = subprocess.run(
            [str(python_executable), str(current_version_path)],
            capture_output=True,
            text=True
        )
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        result.check_returncode()  # This will raise an exception if the return code is non-zero
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running main.py: {e}")
        print("Error output:", e.stderr)

if __name__ == "__main__":
    run_main_script()

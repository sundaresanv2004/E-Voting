import platform
import os
import pandas as pd

from .local_files_scr import file_path, default_setting_data


path = None
os_sys = None

if platform.system() == "Windows":
    os_sys = "Windows"
    path = os.getenv('APPDATA') + r'/E-Voting'
elif platform.system() == 'Darwin':
    os_sys = platform.system()
    path = os.path.expanduser('~') + r"/E-Voting"


def installation_requirement():
    if not os.path.exists(path + file_path['settings']):
        try:
            os.makedirs(path + r'/data/a')
            os.makedirs(path + r'/data/e')
            os.makedirs(path + r'/data/s')
            os.makedirs(path + r'/server/connection')
            os.makedirs(path + r'/backup')
            settings_ser = pd.Series(default_setting_data)
            settings_ser.to_json(path + file_path['settings'], orient='table', index=True)
            ele_data = pd.DataFrame(columns=['election_name', 'connection_path'])
            ele_data.to_csv(path + file_path['election_data'], index=False)
        except FileExistsError:
            pass


if not os.path.exists(path + file_path['app_data']):
    new_start = True
else:
    new_start = False

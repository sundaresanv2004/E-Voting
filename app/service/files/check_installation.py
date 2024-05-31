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
    path = os.path.expanduser('~') + r"/Library/Application Support/E-Voting"


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
            ele_data_ = pd.DataFrame(columns=['election_name', 'connection_path', 'key_path', 'authenticated'])
            ele_data_.to_csv(path + file_path['election_data'], index=False)
        except FileExistsError:
            pass


def new_start() -> bool:
    try:
        ele_data = pd.read_csv(path + file_path['election_data'])
        if ele_data.empty is True:
            return True
        else:
            setting_ser = pd.read_json(path + file_path['settings'], orient='table')
            auth_status = ele_data[ele_data.election_name == setting_ser.loc['election_name'].values[0]]
            return not auth_status.values[0][3]
    except FileNotFoundError:
        return True

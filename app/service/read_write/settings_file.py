import pandas as pd

from ..scr.check_installation import path
from ..scr.local_files_scr import file_path


def window_resize_change(val):
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    settings_ser.loc['maximized'].values[0] = val
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)


def on_close_change(val):
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    settings_ser.loc['at_close'].values[0] = val
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)


def election_data(file_name, key_path):
    ele_data = pd.read_csv(path + file_path['election_data'])
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    ele_data.loc['a'] = [file_name, key_path]
    settings_ser.loc['election'].values[0] = key_path
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)
    ele_data.to_csv(path + file_path['election_data'], index=False)

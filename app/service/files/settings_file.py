import os

import pandas as pd

from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path


def window_resize_change(val: bool) -> None:
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    settings_ser.loc['maximized'].values[0] = val
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)


def on_close_change(val: bool) -> None:
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    settings_ser.loc['at_close'].values[0] = val
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)


def election_data(file_name, key_path, path_k) -> None:
    ele_data = pd.read_csv(path + file_path['election_data'])
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    ele_data.loc['a'] = [file_name, key_path, path_k, False]
    settings_ser.loc['election_name'].values[0] = file_name
    settings_ser.to_json(path + file_path['settings'], orient='table', index=True)
    ele_data.to_csv(path + file_path['election_data'], index=False)


def delete_election_data() -> None:
    ele_data = pd.read_csv(path + file_path['election_data'], index_col='election_name')
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    files_ = ele_data.loc[settings_ser.loc['election_name'].values[0]].values
    os.remove(files_[0])
    os.remove(files_[1])
    ele_data.drop(settings_ser.loc['election_name'].values[0], axis=0, inplace=True)
    ele_data.to_csv(path + file_path['election_data'], index=True)

    if len(ele_data) > 0:
        settings_ser.loc['election_name'].values[0] = ele_data.index.values[0]
        settings_ser.to_json(path + file_path['settings'], orient='table', index=True)
    else:
        settings_ser.loc['election_name'].values[0] = None
        settings_ser.to_json(path + file_path['settings'], orient='table', index=True)

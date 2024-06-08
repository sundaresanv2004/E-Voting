import json
import os
import shutil
import pandas as pd

from .check_installation import path
from .local_files_scr import file_path


def upload_config_file(file_source_path, file_name) -> None:
    shutil.move(file_source_path, path + file_path['connection'] + f'/{file_name}')


def create_connection_json(config_dict: dict, file_name) -> None:
    json_string = json.dumps(config_dict, indent=4)
    path_t = path + file_path['connection'] + f"/{config_dict['projectId']}_firebaseConfig.json"
    path_k = path + file_path['connection'] + f"/{file_name}"
    with open(path_t, 'w') as json_file:
        json_file.write(json_string)
        json_file.close()

    from .settings_file import election_data
    election_data(config_dict['projectId'], path_t, path_k)


def create_appdata_json() -> None:
    from ..firebase.firestore import read_home_data

    df = pd.DataFrame(read_home_data(), index=[0])
    df.to_json(path + file_path['app_data'], orient='table', index=False)


def create_category() -> None:
    from ..firebase.firestore import read_category_data
    dict_data = read_category_data()
    if len(dict_data) == 0:
        df = pd.DataFrame(columns=['EMPTY TABLE'])
    else:
        df = pd.DataFrame(list(dict_data.values()), index=list(dict_data.keys()))
    df.to_csv(path + file_path['category_data'], index=False)


def create_candidate() -> None:
    from ..firebase.realtime_db import read_candidate
    dict_data = read_candidate()
    if dict_data is None:
        df = pd.DataFrame(columns=['EMPTY TABLE'])
    else:
        df = pd.DataFrame(dict_data.values(), index=list(dict_data.keys()))
    df.to_json(path + file_path['candidate_data'], index=False, orient='table')


def remove_files() -> None:
    try:
        os.remove(path + file_path['category_data'])
        os.remove(path + file_path['candidate_data'])
    except FileNotFoundError:
        pass

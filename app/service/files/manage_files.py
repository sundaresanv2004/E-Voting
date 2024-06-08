import json
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

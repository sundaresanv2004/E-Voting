import json

from .check_installation import path
from .local_files_scr import file_path


def create_connection_json(config_dict: dict) -> None:
    json_string = json.dumps(config_dict, indent=4)
    path_t = path + file_path['connection'] + f"/{config_dict['projectId']}_firebaseConfig.json"
    with open(path_t, 'w') as json_file:
        json_file.write(json_string)

    from .settings_file import election_data
    election_data(config_dict['projectId'], path_t)

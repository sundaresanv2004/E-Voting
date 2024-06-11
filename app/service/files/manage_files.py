import json
import os
import random
import shutil
import string
import uuid
import pandas as pd
from datetime import datetime

from .check_installation import path
from .local_files_scr import file_path
from ..firebase.realtime_db import download_image


def upload_config_file(file_source_path, file_name) -> None:
    shutil.copy(file_source_path, path + file_path['connection'] + f'/{file_name}')
    # shutil.move(file_source_path, path + file_path['connection'] + f'/{file_name}')


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


def create_election_settings() -> None:
    from ..firebase.firestore import read_election_settings
    df = pd.DataFrame(read_election_settings(), index=[0])
    df.to_json(path + file_path['election_settings'], orient='table', index=False)


def vote_setup() -> str:
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    path_election = path + rf"/data/e/{setting_ser.at['election_name', 'values']}"

    if not os.path.exists(path_election):
        os.makedirs(path_election)
        os.makedirs(path_election + r"/vote_data")
        os.makedirs(path_election + r"/images")
        from ..firebase.realtime_db import read_candidate
        from ..firebase.firestore import read_category_data

        candidate_data = read_candidate()
        candidate_df = pd.DataFrame(candidate_data.values(), index=list(candidate_data.keys()))
        candidate_df.to_json(path_election + r'/candidate_data.json', index=False, orient='table')
        candidate_df.reset_index(inplace=True, drop=True)

        category_data = read_category_data()
        category_df = pd.DataFrame(list(category_data.values()), index=list(category_data.keys()))
        category_df.dropna(inplace=True)
        category_df = category_df.astype({'order': int})
        category_df.sort_values(by='order', ascending=True, inplace=True, axis=0, ignore_index=True)
        category_df.to_csv(path_election + r'/category_data.csv', index=False)

        election_log = pd.DataFrame(
            columns=['vote_id', 'file_name', 'active_status', 'upload_status', 'created_on', 'uploaded_on'])
        election_log.to_json(path_election + r'/election_datalog.json', index=False, orient='table')

        for i in range(len(candidate_df)):
            image_path = candidate_df.at[i, 'image']
            download_image(image_path, path_election + rf"/{image_path}")

    election_data_file(path_election)

    return path_election


def election_data_file(path_election: str) -> None:
    election_log = pd.read_json(path_election + r'/election_datalog.json', orient='table')
    category_df = pd.read_csv(path_election + r'/category_data.csv')

    vote_df = pd.DataFrame(columns=category_df['category_name'])
    source = string.ascii_letters + string.digits
    rand = ''.join((random.choice(source)) for _ in range(5))
    vote_id = str(uuid.uuid4())
    vote_df.to_csv(path_election + rf'/vote_data/{rand}.csv', index=False)
    election_log.loc['aa'] = [vote_id, rf'/vote_data/{rand}.csv', True, False,
                              str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), None]
    election_log.to_json(path_election + r'/election_datalog.json', orient='table', index=False)


def vote_end(path_election) -> None:
    election_log = pd.read_json(path_election + r'/election_datalog.json', orient='table')
    df1 = election_log[election_log.active_status == True]
    index_val = df1.index.values[0]
    vote_data_df = pd.read_csv(path_election + election_log.at[index_val, 'file_name'])
    if vote_data_df.empty:
        election_log.at[index_val, 'active_status'] = False
        election_log.at[index_val, 'upload_status'] = True
        election_log.to_json(path_election + r'/election_datalog.json', orient='table', index=False)
    else:
        print(vote_data_df)


def remove_files() -> None:
    try:
        os.remove(path + file_path['category_data'])
        os.remove(path + file_path['candidate_data'])
    except FileNotFoundError:
        pass

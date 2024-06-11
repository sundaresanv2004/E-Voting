import platform
import uuid
from datetime import datetime

import firebase_admin
import pandas as pd
from firebase_admin import firestore

import app.service.firebase.connect_firebase as connect_firebase
from ..files.check_installation import path
from ..files.local_files_scr import file_path
from ..files.manage_files import create_category
from ...functions.dialogs import network_error


def app_data(info_list: list) -> None:
    db = firestore.client()
    dict_data = {
        "institution_name": info_list[0],
        "election_name": info_list[1],
        "created_at": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "app_version": "6.06"
    }

    db.collection('settings').document('appdata').set(dict_data)

    election_dict = {
        "vote_option": False,
        "completed": False,
        "code": None,
        "final_nomination": False,
        "lock_data": False,
        "result": False,
        "created_at": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }

    db.collection('settings').document('election_settings').set(election_dict)


def system_data(status: bool) -> None:
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    db = firestore.client()
    system_info = {
        'name': platform.node(),
        'os': platform.system(),
        'version': platform.release(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'release': platform.release(),
        'machine': platform.machine(),
        "auth_status": status,
        "date_added": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }

    if pd.isna(setting_ser.loc['system_id'].values[0]):
        system_id = str(uuid.uuid4())
        setting_ser.loc['system_id'] = system_id
        setting_ser.to_json(path + file_path['settings'], orient='table', index=True)
    else:
        system_id = setting_ser.loc['system_id'].values[0]

    system_info['system_id'] = system_id
    db.collection('system_data').document(system_id).set(system_info)

    ele_data = pd.read_csv(path + file_path['election_data'], index_col='election_name')
    ele_data.at[connect_firebase.election_name, 'authenticated'] = True
    ele_data.to_csv(path + file_path['election_data'], index=True)


def read_home_data() -> dict:
    db = firestore.client()
    collections = db.collection('settings').document('appdata').get().to_dict()
    return collections


def read_category_data() -> dict:
    db = firestore.client()
    collections = db.collection('category')
    dict1 = {}
    for doc in collections.stream():
        dict1[doc.id] = doc.to_dict()
    return dict1


def read_election_settings() -> dict:
    db = firestore.client()
    collections = db.collection('settings').document('election_settings').get().to_dict()
    return collections


def add_category_data(category) -> None:
    db = firestore.client()
    category_id = str(uuid.uuid4())
    category_dict = {
        'category_id': category_id,
        'category_name': category,
        'order': None,
        'created_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }
    db.collection('category').document(category_id).set(category_dict)

    category_df = pd.read_csv(path + file_path['category_data'])
    if category_df.empty is False:
        category_df.loc[category_id] = category_dict
    else:
        category_df = pd.DataFrame(category_dict, index=[category_df])
    category_df.to_csv(path + file_path['category_data'], index=False)


def update_appdata_name(data: dict) -> None:
    db = firestore.client()
    db.collection('settings').document('appdata').update(data)
    home_data = pd.read_json(path + file_path['app_data'], orient='table')
    home_data.at[0, list(data.keys())[0]] = list(data.values())[0]
    home_data.to_json(path + file_path['app_data'], orient='table', index=False)


def update_election_data(data: list) -> None:
    db = firestore.client()
    category_df = pd.read_csv(path + file_path['category_data'])
    ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')

    category_dict = {}
    for i in range(len(category_df)):
        category_dict[category_df.at[i, 'category_name']] = category_df.at[i, 'category_id']

    for i, n in enumerate(data):
        db.collection('category').document(category_dict[n]).update({'order': i + 1})
        category_dict.pop(n)

    for i in list(category_dict.keys()):
        if i not in data:
            db.collection('category').document(category_dict[i]).update({'order': None})

    election_dict = {
        "final_nomination": True,
        "lock_data": True,
    }
    db.collection('settings').document('election_settings').update(election_dict)
    ele_ser_1.at[0, 'final_nomination'] = True
    ele_ser_1.at[0, 'lock_data'] = True
    ele_ser_1.to_json(path + file_path['election_settings'], orient='table', index=False)
    create_category()


def update_vote_option(value: bool) -> None:
    db = firestore.client()
    ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')

    db.collection('settings').document('election_settings').update({'vote_option': value})
    ele_ser_1.at[0, 'vote_option'] = value
    ele_ser_1.to_json(path + file_path['election_settings'], orient='table', index=False)


def get_system_data() -> pd.DataFrame:
    db = firestore.client()
    collections = db.collection('system_data')
    dict1 = {}
    for doc in collections.stream():
        dict1[doc.id] = doc.to_dict()
    df = pd.DataFrame(list(dict1.values()), index=list(dict1.keys()))
    return df


def update_result() -> None:
    db = firestore.client()
    db.collection('settings').document('election_settings').update({'result': True})

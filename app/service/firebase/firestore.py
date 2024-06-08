import platform
import uuid
from datetime import datetime

import firebase_admin
import pandas as pd
from firebase_admin import firestore

import app.service.firebase.connect_firebase as connect_firebase
from ..files.check_installation import path
from ..files.local_files_scr import file_path
from ...functions.dialogs import network_error


def app_data(info_dict: dict) -> None:
    db = firestore.client()
    db.collection('settings').document('appdata').set(info_dict)

    election_dict = {
        "election-name": info_dict['election_name'],
        "vote_option": False,
        "completed": False,
        "code": None,
        "final_nomination": False,
        "lock_data": False,
        "result": False,
        "created_datetime": info_dict['created_datetime'],
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
    collections = db.collection('general').document('category_data')
    return collections.get().to_dict()


def add_category_data(category) -> None:
    db = firestore.client()
    category_dict = {
        str(uuid.uuid4()): category
    }
    db.collection('general').document('category_data').update(category_dict)

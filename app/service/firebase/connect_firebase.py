import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pandas as pd
import platform
import uuid

from app.functions.dialogs import message_dialogs
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path

new_election = True
connect_server = True
election_name = None
firebase = None


def start_connection():
    global new_election, connect_server, election_name, firebase

    ele_data = pd.read_csv(path + file_path['election_data'])
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    ele_path_data = ele_data[ele_data.election_name == setting_ser.loc['election_name'].values[0]]
    election_name = ele_path_data.values[0][0]

    try:
        with open(ele_path_data.values[0][1], 'r') as file:
            config_dict = json.load(file)
            file.close()
    except FileNotFoundError:
        pass

    try:
        cred = credentials.Certificate(ele_path_data.values[0][2])
        firebase_admin.initialize_app(cred)
        firebase = pyrebase.initialize_app(config_dict)
    except ValueError:
        print("error")

    data = auth.list_users()

    if len(data.users) == 0:
        new_election = False
    else:
        connect_server = False


def delete_firebase_admin_app():
    global new_election, connect_server
    new_election, connect_server = True, True
    app = firebase_admin.get_app()
    firebase_admin.delete_app(app)


def create_user(page, info_dict: dict):
    try:
        auth.create_user(
            email=info_dict['email'],
            password=info_dict['password'],
            display_name=info_dict['username'],
            email_verified=True,
        )
    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        message_dialogs(page, 'EmailAlreadyExistsError')

    ele_data = pd.read_csv(path + file_path['election_data'])
    ele_path_data = ele_data[ele_data.election_name == election_name]
    ele_data.at[ele_path_data.index.values[0], 'authenticated'] = True
    ele_data.to_csv(path + file_path['election_data'], index=False)


def app_data(info_dict: dict) -> None:
    db = firestore.client()
    db.collection('system_data').document('AppData').set(info_dict)


def system_data(status: bool) -> None:
    db = firestore.client()
    system_id = str(uuid.uuid4())
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    setting_ser.loc['system_id'] = system_id

    system_info = {
        'system_id': system_id,
        'name': platform.node(),
        'os': platform.system(),
        'version': platform.release(),
        'architecture': platform.architecture(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'release': platform.release(),
        'machine': platform.machine(),
        "auth_status": status
    }

    setting_ser.to_json(path + file_path['settings'], orient='table', index=True)
    db.collection('system_data').document(system_id).set(system_info)

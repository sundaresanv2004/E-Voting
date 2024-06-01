import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pandas as pd
import platform
import uuid

from app.functions.dialogs import message_dialogs, network_error
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path

new_election = True
connect_server = True
election_name = None
firebase = None
connection_status = False
page_1 = None


def start_connection(page):
    global new_election, connect_server, election_name, firebase, connection_status, page_1

    page_1 = page
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
        connection_status = True
    except ValueError:
        pass

    try:
        data = auth.list_users()
    except Exception as e:
        network_error(page, e)
        breakpoint()

    if len(data.users) == 0:
        new_election = False
    else:
        connect_server = False


def delete_firebase_admin_app():
    global new_election, connect_server, connection_status
    new_election, connect_server, connection_status = True, True, False
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
    except Exception as e:
        network_error(page, e)
        breakpoint()

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
        'platform': platform.platform(),
        'processor': platform.processor(),
        'release': platform.release(),
        'machine': platform.machine(),
        "auth_status": status
    }

    setting_ser.to_json(path + file_path['settings'], orient='table', index=True)
    db.collection('system_data').document(system_id).set(system_info)


def admin_data_email() -> None:
    try:
        user = auth.list_users()
    except Exception as e:
        network_error(page_1, e)
        breakpoint()
    emails = {}
    for user in user.users:
        emails[user.email] = user.uid
    return emails


def update_password(uid, new_password) -> None:
    try:
        auth.update_user(uid, password=new_password)
    except firebase_admin._auth_utils.UserNotFoundError:
        pass
    except Exception as e:
        network_error(page_1, e)
        breakpoint()

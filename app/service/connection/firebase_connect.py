import firebase_admin
from firebase_admin import credentials, auth, firestore
import pandas as pd

from app.functions.dialogs import message_dialogs
from app.service.scr.check_installation import path
from app.service.scr.local_files_scr import file_path

new_election = True
connect_server = True


def start_connection():
    global new_election, connect_server

    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    try:
        cred = credentials.Certificate(settings_ser.loc['election'].values[0])
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass

    data = auth.list_users()

    if len(data.users) == 0:
        new_election = False
    else:
        connect_server = False


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


def app_data(info_dict: dict):
    db = firestore.client()
    db.collection('settings').document('AppData').set(info_dict)

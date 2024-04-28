import firebase_admin
from firebase_admin import credentials, auth
import pandas as pd

from app.functions.dialogs import message_dialogs
from app.service.scr.check_installation import path
from app.service.scr.local_files_scr import file_path


def start_connection():
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    try:
        cred = credentials.Certificate(settings_ser.loc['election'].values[0])
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass


def check_new_file() -> bool:
    data = auth.list_users()
    if data is None:
        return False
    else:
        return True


def check_file_exist() -> bool:
    data = auth.list_users()
    if data is None:
        return True
    else:
        return False


def create_user(page, info_dict: dict):
    try:
        auth.create_user(
            email=info_dict['email'],
            password=info_dict['password'],
            display_name=info_dict['username'],
        )
    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        message_dialogs(page, 'EmailAlreadyExistsError')

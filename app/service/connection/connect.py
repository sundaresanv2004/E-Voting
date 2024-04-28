import firebase_admin
from firebase_admin import credentials
import pandas as pd

from app.service.scr.check_installation import path
from app.service.scr.local_files_scr import file_path


def start_connection():
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')
    try:
        cred = credentials.Certificate(settings_ser.loc['election'].values[0])
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass


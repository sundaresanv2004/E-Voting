import json
import pyrebase
import pandas as pd

from app.functions.dialogs import message_dialogs
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path

new_election = True
connect_server = True


def start_connection():
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')

    with open(setting_ser.loc['election'].values[0], 'r') as file:
        config_dict = json.load(file)
        file.close()

    firebase = pyrebase.initialize_app(config_dict)

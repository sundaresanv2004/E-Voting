import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
import pandas as pd

from app.functions.dialogs import network_error
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path

new_election = True
connect_server = True
election_name = None
firebase = None
connection_status = False


def start_connection(page):
    global new_election, connect_server, election_name, firebase, connection_status, page_1

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

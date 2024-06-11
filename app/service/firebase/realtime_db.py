import uuid
from datetime import datetime

import pandas as pd

import app.service.firebase.connect_firebase as connect_firebase
import app.service.user.login_auth as cc
from app.functions.dialogs import network_error
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path


def read_candidate() -> dict:
    db = connect_firebase.firebase.database()
    all_data = db.child('candidates').get(cc.auth_data['idToken']).val()
    return all_data


def add_image(image_path: str, image_name: str) -> None:
    storage = connect_firebase.firebase.storage()
    storage.child(f"images/{image_name}").put(image_path)


def add_candidate(page, data: list) -> None:
    candidate_id = str(uuid.uuid4())
    data_dict = {
        'candidate_id': candidate_id,
        "name": data[0],
        "category": data[1],
        "image": f"images/{data[2]}",
        'created_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'updated_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }

    try:
        db = connect_firebase.firebase.database()
        db.child("candidates").child(candidate_id).set(data_dict, cc.auth_data['idToken'])
    except Exception as e:
        network_error(page, e, "normal")
        breakpoint()

    add_image(data[3], data[2])

    candidate_df = pd.read_json(path + file_path['candidate_data'], orient='table')
    if candidate_df.empty is False:
        candidate_df.loc[candidate_id] = data_dict
    else:
        candidate_df = pd.DataFrame(data_dict, index=[candidate_id])
    candidate_df.to_json(path + file_path['candidate_data'], index=False, orient='table')


def get_image_url(page, image_name: str) -> str:
    try:
        storage = connect_firebase.firebase.storage()
        return storage.child(image_name).get_url(None)
    except Exception as e:
        network_error(page, e, "normal")
        breakpoint()


def delete_candidate(page, candidate_index) -> None:
    candidate_df = pd.read_json(path + file_path['candidate_data'], orient='table')
    try:
        db = connect_firebase.firebase.database()
        db.child('candidates').child(candidate_df.at[candidate_index, 'candidate_id']).remove(cc.auth_data['idToken'])
    except Exception as e:
        network_error(page, e, "normal")
        breakpoint()

    candidate_df.drop(candidate_index, inplace=True, axis=0)
    candidate_df.to_json(path + file_path['candidate_data'], index=False, orient='table')


def edit_candidate(page, candidate_index: int, candidate_data: list) -> None:
    candidate_df = pd.read_json(path + file_path['candidate_data'], orient='table')
    candidate_id = candidate_df.at[candidate_index, 'candidate_id']

    data_dict = {
        'candidate_id': candidate_id,
        "name": candidate_data[0],
        "category": candidate_data[1],
        'updated_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }
    if candidate_data[2] is not False:
        add_image(candidate_data[3], candidate_data[2])
        data_dict['image'] = f"images/{candidate_data[2]}"
        candidate_df.at[candidate_index, 'image'] = f"images/{candidate_data[2]}"

    try:
        db = connect_firebase.firebase.database()
        db.child('candidates').child(candidate_id).update(data_dict, cc.auth_data['idToken'])
    except Exception as e:
        network_error(page, e, "normal")
        breakpoint()

    candidate_df.at[candidate_index, 'name'] = candidate_data[0]
    candidate_df.at[candidate_index, 'category'] = candidate_data[1]
    candidate_df.at[candidate_index, 'updated_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    candidate_df.to_json(path + file_path['candidate_data'], index=False, orient='table')


def download_image(image_path: str, download_path: str) -> None:
    storage = connect_firebase.firebase.storage()
    storage.child(image_path).download(image_path, download_path)


def vote_set(page, data_dict: dict, path_election) -> None:
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    election_log = pd.read_json(path_election + r'/election_datalog.json', orient='table')
    election_settings = pd.read_json(path + file_path['election_settings'], orient='table')

    try:
        db = connect_firebase.firebase.database()
        if pd.isna(election_log.at[0, 'uploaded_on']):
            db.child("vote_data").child(setting_ser.at['system_id', 'values']).set(data_dict, cc.auth_data['idToken'])
        else:
            db.child("vote_data").child(setting_ser.at['system_id', 'values']).update(data_dict,
                                                                                      cc.auth_data['idToken'])
    except Exception as e:
        network_error(page, e, "vote")
        breakpoint()

    if not election_settings.at[0, 'result']:
        from app.service.firebase.firestore import update_result
        update_result(page)

    election_log.at[0, 'upload_status'] = True
    election_log.at[0, 'uploaded_on'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    election_log.to_json(path_election + r'/election_datalog.json', index=False, orient='table')


def read_vote_data(page) -> pd.DataFrame:
    try:
        db = connect_firebase.firebase.database()
        all_data = db.child('vote_data').get(cc.auth_data['idToken']).val()
        election_df = pd.DataFrame(columns=list(all_data[list(all_data.keys())[0]].keys()))

        for i in list(all_data.keys()):
            temp_dict = {}
            for j in list(all_data[i].keys()):
                temp_dict[j] = all_data[i][j]

            election_df.loc[i] = temp_dict

        election_df.reset_index(inplace=True, drop=True)
        return election_df
    except Exception as e:
        network_error(page, e, "normal")
        breakpoint()

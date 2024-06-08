import uuid
from datetime import datetime

import pandas as pd

import app.service.firebase.connect_firebase as connect_firebase
import app.service.user.login_auth as cc
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path


def read_candidate() -> dict:
    db = connect_firebase.firebase.database()
    all_data = db.child('candidates').get(cc.auth_data['idToken']).val()
    return all_data


def add_image(image_path: str, image_name: str) -> None:
    storage = connect_firebase.firebase.storage()
    storage.child(f"images/{image_name}").put(image_path)


def add_candidate(data: list) -> None:
    db = connect_firebase.firebase.database()
    candidate_id = str(uuid.uuid4())
    data_dict = {
        'candidate_id': candidate_id,
        "name": data[0],
        "category": data[1],
        "image": f"images/{data[2]}",
        'created_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'updated_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }
    db.child("candidates").child(candidate_id).set(data_dict, cc.auth_data['idToken'])

    add_image(data[3], data[2])

    candidate_df = pd.read_json(path + file_path['candidate_data'], orient='table')
    if candidate_df.empty is False:
        candidate_df.loc[candidate_id] = data_dict
    else:
        candidate_df = pd.DataFrame(data_dict, index=[candidate_id])
    candidate_df.to_json(path + file_path['candidate_data'], index=False, orient='table')


def get_image_url(image_name: str) -> str:
    storage = connect_firebase.firebase.storage()
    return storage.child(image_name).get_url(None)

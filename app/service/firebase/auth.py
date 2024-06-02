import firebase_admin
from firebase_admin import auth

from app.functions.dialogs import message_dialogs, network_error


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


def admin_data_email(page) -> dict:
    try:
        user = auth.list_users()
    except Exception as e:
        network_error(page, e)
        breakpoint()
    emails = {}
    for user in user.users:
        emails[user.email] = user.uid
    return emails


def update_password(page, uid, new_password) -> None:
    try:
        auth.update_user(uid, password=new_password)
    except firebase_admin._auth_utils.UserNotFoundError:
        pass
    except Exception as e:
        network_error(page, e)
        breakpoint()

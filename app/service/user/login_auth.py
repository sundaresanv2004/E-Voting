import app.service.firebase.connect_firebase as connection

auth_data = None


def check_login(page, mail_id, password) -> bool:
    global auth_data

    auth = connection.firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email=mail_id, password=password)
        auth_data = user
        from app.service.files.manage_files import create_appdata_json
        create_appdata_json(page)
        return True
    except Exception as e:
        return False


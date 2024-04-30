from firebase_admin import auth

teme_data = None


def login_checker(entry1: str, entry2: str) -> bool:
    global teme_data

    try:
        user = auth.get_user_by_email(entry1)
        print(user)
        return True
    except Exception as e:
        pass
    return False

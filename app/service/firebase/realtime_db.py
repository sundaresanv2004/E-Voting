import app.service.firebase.connect_firebase as connect_firebase
import app.service.user.login_auth as cc


def read_candidate() -> dict:
    db = connect_firebase.firebase.database()
    all_data = db.get(cc.auth_data['idToken']).val()

    # Print all data
    print(all_data)
    return all_data


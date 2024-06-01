import random
import flet as ft
from time import sleep

import app.functions.verification_dialog as ver


def verify_code_email(page: ft.Page) -> bool:
    ver_code = str(random.randint(1000, 99999))
    print(ver_code)

    ver.verification_dialogs(page, "abcdefghij12345@gmail.com", ver_code)

    while ver.verified_dialog_open:
        if ver.verified_dialog_open is False:
            break
        else:
            sleep(1)

    return ver.verified

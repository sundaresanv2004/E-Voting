import pandas as pd
import flet as ft

from ..files.check_installation import path
from ..files.local_files_scr import file_path
from ...functions.dialogs import loading_dialogs


def check_connection_files(page: ft.Page) -> None:
    ele_data = pd.read_csv(path + file_path['election_data'])
    if ele_data.empty:
        from ...functions.connection_setup import connection_setup
        connection_setup(page, True)
    else:
        import app.service.firebase.connect_firebase as conn

        if conn.connection_status is False:
            dig = loading_dialogs(page, "Connecting...")
            conn.start_connection(page)
            dig.open = False

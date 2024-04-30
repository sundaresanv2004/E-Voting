import pandas as pd
import flet as ft

from ..scr.check_installation import path
from ..scr.local_files_scr import file_path


def check_connection_files(page: ft.Page):
    ele_data = pd.read_csv(path + file_path['election_data'])
    if ele_data.empty:
        from ...functions.connection_file_upload import connection_file_error
        connection_file_error(page)
    else:
        from .firebase_connect import start_connection
        start_connection()

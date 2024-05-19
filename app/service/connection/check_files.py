import pandas as pd
import flet as ft

from ..files.check_installation import path
from ..files.local_files_scr import file_path


def check_connection_files(page: ft.Page) -> None:
    ele_data = pd.read_csv(path + file_path['election_data'])
    if ele_data.empty:
        from ...functions.connection_setup import connection_setup
        connection_setup(page)
    else:
        from .firebase_connect import start_connection
        start_connection()

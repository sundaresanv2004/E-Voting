import flet as ft
import pandas as pd

from .window_close import close_true
from ..service.files.settings_file import window_resize_change
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path


def window_at_start(page: ft.Page) -> None:
    settings_ser = pd.read_json(path + file_path['settings'], orient='table')

    # at_close
    def at_close_event(e):
        if e.data == "close":
            close_true(page)

    # ask question at close [True, False]
    page.window_prevent_close = settings_ser.loc['at_close'].values[0]
    page.on_window_event = at_close_event

    page.window_maximized = settings_ser.loc['maximized'].values[0]


def window_on_resize(page: ft.Page) -> None:

    try:
        setting_ser = pd.read_json(path + file_path['settings'], orient='table')
        if page.window_maximized != setting_ser.loc['maximized'].values[0]:
            window_resize_change(page.window_maximized)
        page.update()
    except ValueError:
        pass

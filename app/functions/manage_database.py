import flet as ft
import pandas as pd

from app.functions.connection_setup import connection_setup
from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path
from app.service.firebase.connect_firebase import delete_firebase_admin_app


def manage_db_dialogs(page: ft.Page):
    def on_close(e):
        manage_db_alertdialog.open = False
        page.update()

    def new_connection(e):
        on_close(e)
        connection_setup(page, False)

    dropdown = ft.Dropdown(
        label="Current Connection",
        width=400,
        filled=False,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        border_color=ft.colors.BLACK,
        color=ft.colors.BLACK,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),

    )

    ele_data = pd.read_csv(path + file_path['election_data'])
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')

    for i in ele_data['election_name'].values:
        dropdown.options.append(ft.dropdown.Option(i))

    dropdown.value = setting_ser.loc['election_name'].values[0]

    def on_save(e):
        if dropdown.value != setting_ser.loc['election_name'].values[0]:
            on_close(e)
            setting_ser.loc['election_name'] = dropdown.value
            setting_ser.to_json(path + file_path['settings'], orient='table', index=True)
            delete_firebase_admin_app()
            page.clean()
            from main import main
            main(page)
        else:
            on_close(e)

    manage_db_alertdialog = ft.AlertDialog(
        modal=False,
        title=ft.Text(
            value="Manage Firebase Connections",
            weight=ft.FontWeight.W_500,
        ),
        content=ft.Column(
            [
                dropdown,
                ft.TextButton(
                    text="New Connection",
                    icon=ft.icons.ADD_ROUNDED,
                    on_click=new_connection,
                ),
            ],
            height=110,
            spacing=10
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
            ft.TextButton(
                text="Save",
                on_click=on_save,
            ),
        ]
    )

    # Open dialog
    page.dialog = manage_db_alertdialog
    manage_db_alertdialog.open = True
    page.update()

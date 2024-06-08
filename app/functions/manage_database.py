import flet as ft
import pandas as pd

from .connection_setup import connection_setup
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..service.files.settings_file import delete_election_data
from .snack_bar import snackbar
from ..service.firebase.connect_firebase import delete_firebase_admin_app


def manage_db_dialogs(page: ft.Page, admin: bool):
    def on_close(e):
        manage_db_alertdialog.open = False
        page.update()

    def on_delete(e):
        on_close(e)
        delete_connection(page, dropdown.value)

    def new_connection(e):
        on_close(e)
        connection_setup(page, False)

    dropdown = ft.Dropdown(
        label="Current Connection",
        width=450,
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
            snackbar(page, "Connection Updated")
        else:
            on_close(e)

    row_options = ft.Row(
        [
            ft.TextButton(
                text="Add Connection",
                icon=ft.icons.ADD_ROUNDED,
                on_click=new_connection,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    if admin:
        row_options.controls.append(
            ft.TextButton(
                text="Remove Connection",
                icon=ft.icons.DELETE_ROUNDED,
                on_click=on_delete,
            ),
        )

    manage_db_alertdialog = ft.AlertDialog(
        modal=False,
        title=ft.Text(
            value="Manage Firebase Connections",
            weight=ft.FontWeight.W_500,
        ),
        content=ft.Column(
            [
                dropdown,
                row_options,
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


def delete_connection(page: ft.Page, election_name: str):
    def on_close(e):
        remove_db_alertdialog.open = False
        page.update()

    def on_delete(e):
        if box_entry.value == election_name:
            on_close(e)
            box_entry.error_text = None
            delete_election_data()
            delete_firebase_admin_app()
            page.clean()
            from main import main
            main(page)
            snackbar(page, "Connection Removed")
        else:
            box_entry.error_text = "Invalid election name!"
            box_entry.focus()
        page.update()

    box_entry = ft.TextField(
        width=480,
        filled=False,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
    )

    remove_db_alertdialog = ft.AlertDialog(
        modal=False,
        title=ft.Text(
            value="Remove Firebase Connections",
            weight=ft.FontWeight.W_500,
        ),
        content=ft.Column(
            [
                ft.Text(
                    value=f"To confirm, type '{election_name}' in the box below",
                    font_family='Verdana',
                    weight=ft.FontWeight.W_400,
                ),
                box_entry
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
                text="Remove",
                on_click=on_delete,
            ),
        ]
    )

    # Open dialog
    page.dialog = remove_db_alertdialog
    remove_db_alertdialog.open = True
    page.update()

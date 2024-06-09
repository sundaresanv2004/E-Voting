import flet as ft
import pandas as pd

from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path


def institution_name_dialogs(page: ft.Page):
    def on_ok(e):
        institution_name_dialogs1.open = False
        page.update()

    app_data_sys_df = pd.read_json(path + file_path['app_data'], orient='table')

    def check_entry_valid(e):
        if len(institution_name_entry.value) != 0:
            institution_name_entry.suffix_icon = None
            institution_name_entry.error_text = None
        else:
            institution_name_entry.error_text = "Enter the institution name"
            institution_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        institution_name_entry.update()

    def save_name(e):
        check_entry_valid(e)
        if len(institution_name_entry.value) != 0:
            if app_data_sys_df.at[0, 'institution_name'] != institution_name_entry.value:
                from ..service.firebase.firestore import update_appdata_name
                from .settings import update_settings_data
                update_appdata_name({"institution_name": institution_name_entry.value})
                on_ok(e)
                update_settings_data()
            else:
                on_ok(e)
        else:
            institution_name_entry.focus()
            institution_name_entry.update()

    institution_name_entry = ft.TextField(
        hint_text="Enter the institution name",
        width=360,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border_radius=10,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        value=app_data_sys_df.at[0, 'institution_name'],
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_entry_valid,
        on_submit=save_name,
    )

    # AlertDialog data
    institution_name_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Institution Name",
            font_family='Verdana',
        ),
        content=ft.Row(
            [
                institution_name_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Save",
                on_click=save_name,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = institution_name_dialogs1
    institution_name_dialogs1.open = True
    page.update()


def help_dialogs(page: ft.Page):
    from ..service.files.local_files_scr import all_done_message

    def on_close(e):
        help_dialogs1.open = False
        page.update()

    help_content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.LIVE_HELP_ROUNDED,
                                size=30,
                            ),
                            ft.Text(
                                value="Help",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family='Verdana',
                            ),
                        ],
                        width=450,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        key='top'
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CLOSE_ROUNDED,
                                tooltip="Close",
                                on_click=on_close,
                            )
                        ]
                    )
                ],
                width=500,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(height=10),
            ft.Column(
                [
                    ft.Column(
                        [
                            ft.Markdown(
                                code_theme="atom-one-dark",
                                selectable=False,
                                value=all_done_message,
                                code_style=ft.TextStyle(font_family="Verdana"),
                            )
                        ],
                        width=460,
                    ),
                ],
                width=480,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(height=5),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_CIRCLE_UP_ROUNDED,
                        tooltip='Back to top',
                        icon_size=30,
                        icon_color=ft.colors.BLACK,
                        on_click=lambda _: help_content.scroll_to(key="top", duration=1000)
                    ),
                    ft.Row(width=1)
                ],
                width=480,
                alignment=ft.MainAxisAlignment.END
            )
        ],
        width=500,
        height=570,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    # AlertDialog data
    help_dialogs1 = ft.AlertDialog(
        modal=False,
        content=help_content,
    )

    # Open dialog
    page.dialog = help_dialogs1
    help_dialogs1.open = True
    page.update()


def election_name_dialogs(page: ft.Page):
    def on_ok(e):
        election_name_dialogs1.open = False
        page.update()

    ele_ser = pd.read_json(path + file_path['app_data'], orient='table')

    def on_election_name_change(e):
        if len(election_name_entry.value) != 0:
            election_name_entry.error_text = None
            election_name_entry.suffix_icon = None
        else:
            election_name_entry.error_text = 'Enter the election name.'
            election_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        election_name_entry.update()

    def on_save_election_name(e):
        on_election_name_change(e)
        if len(election_name_entry.value) != 0:
            if election_name_entry.value != ele_ser.at[0, 'election_name']:
                from ..service.firebase.firestore import update_appdata_name
                from .settings import update_settings_data
                update_appdata_name({"election_name": election_name_entry.value})
                on_ok(e)
                update_settings_data()
            else:
                on_ok(e)
        else:
            election_name_entry.focus()
        election_name_entry.update()

    election_name_entry = ft.TextField(
        hint_text="Enter the Election Name",
        width=350,
        border_radius=10,
        filled=False,
        border=ft.InputBorder.OUTLINE,
        capitalization=ft.TextCapitalization.CHARACTERS,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_save_election_name,
        on_change=on_election_name_change,
        value=ele_ser.at[0, 'election_name'],
    )

    # AlertDialog data
    election_name_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            font_family='Verdana',
            value="Election Name",
        ),
        content=ft.Row(
            [
                election_name_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Save",
                on_click=on_save_election_name,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = election_name_dialogs1
    election_name_dialogs1.open = True
    page.update()



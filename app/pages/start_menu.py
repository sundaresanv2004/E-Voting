import flet as ft

from app.functions.manage_database import manage_db_dialogs
from app.pages.create_account import create_account_page
from app.pages.login import login_page
from app.service.files.check_installation import new_start
import app.service.firebase.connect_firebase as ser


def start_menu_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    settings_button = ft.FloatingActionButton(
        icon=ft.icons.CLOUD_SYNC_ROUNDED,
        tooltip="Manage Firebase Connection",
        on_click=lambda _: manage_db_dialogs(page)
    )

    def animations(size):  # 250
        content_image.height = size
        content_column.clean()
        page.update()

    def on_create_account(e):
        page.remove(settings_button)
        animations(170)
        create_account_page(page, content_image, content_column)

    def on_sign_in(e):
        page.remove(settings_button)
        animations(170)
        login_page(page, content_image, content_column)

    if new_start():
        list_menu_button = [
            ft.ElevatedButton(
                text="New Election",
                height=50,
                width=250,
                on_click=on_create_account,
                disabled=ser.new_election,
            ),
            ft.ElevatedButton(
                text="Connect Server",
                height=50,
                width=250,
                tooltip="Disabled",
                disabled=ser.connect_server,
            ),
        ]
    else:
        list_menu_button = [
            ft.ElevatedButton(
                text="Sign In",
                height=50,
                width=250,
                on_click=on_sign_in,
            ),
            ft.ElevatedButton(
                text="Vote",
                height=50,
                width=250,
            ),
        ]

    page.add(
        settings_button
    )

    content_column.controls = [
        ft.Column(
            list_menu_button,
            width=250,
            spacing=20,
        )
    ]

    page.update()

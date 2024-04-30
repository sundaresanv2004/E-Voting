import flet as ft

from .create_account import create_account_page
from .login import login_page
from ..service.scr.check_installation import new_start

cont_image = None
cont_column: ft.Column = None
page1: ft.Page = None


class MenuButtons(ft.UserControl):
    def __init__(self, page: ft.Page, text: str):
        super().__init__()
        self.page = page

    def vote_login(self, e):
        pass
        # self.animations(250)
        # vote_login_page(self.page, self.cont_image, self.cont_column)


def animations(size):  # 250
    cont_image.height = size
    cont_column.clean()
    page1.update()


def on_sign_in(e):
    animations(170)
    login_page(page1, cont_image, cont_column)


def on_create_account(e):
    animations(170)
    create_account_page(page1, cont_image, cont_column)


def start_menu_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    global cont_image, cont_column, page1
    cont_image, cont_column, page1 = content_image, content_column, page
    from ..service.connection.firebase_connect import new_election, connect_server

    if new_start is True:
        list_menu_button = [
            ft.ElevatedButton(
                text="New Election",
                height=50,
                width=250,
                on_click=on_create_account,
                disabled=new_election
            ),
            ft.ElevatedButton(
                text="Connect Server",
                height=50,
                width=250,
                tooltip="Disabled",
                disabled=connect_server,
            ),
        ]
        page.add(
            ft.FloatingActionButton(
                icon=ft.icons.SETTINGS_ROUNDED
            )
        )
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

    content_column.controls = [
        ft.Column(
            list_menu_button,
            width=250,
            spacing=20,
        )
    ]

    page.update()

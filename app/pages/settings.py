import flet as ft
import pandas as pd

from .settings_options import institution_name_dialogs, election_name_dialogs, help_dialogs, system_dialogs
from ..functions.manage_database import manage_db_dialogs
from ..functions.snack_bar import snackbar
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path

var_option_data_update = None


class SettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.systems = None
        self.page = page
        self.app_data = pd.read_json(path + file_path['app_data'], orient='table')
        self.election_name = None
        self.help = None
        self.institution_name = None
        self.create_election = None
        self.project = None
        self.next_icon = ft.Icon(
            name=ft.icons.NAVIGATE_NEXT_ROUNDED,
            size=25,
        )
        self.election_name_text = ft.Text(font_family='Verdana')
        self.institution_name_text = ft.Text(font_family='Verdana')

    def institution_name_option(self):
        self.institution_name_text.value = self.app_data.at[0, 'institution_name']
        self.institution_name = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Institution Name",
                        font_family='Verdana',
                    ),
                    subtitle=self.institution_name_text,
                    trailing=self.next_icon,
                    on_click=lambda _: institution_name_dialogs(self.page),
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.5, '#44CCCCCC')
        )

        return self.institution_name

    def election_name_option(self):
        self.election_name_text.value = self.app_data.at[0, 'election_name']
        self.election_name = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        font_family='Verdana',
                        value=f"Election Name",
                    ),
                    subtitle=self.election_name_text,
                    trailing=self.next_icon,
                    on_click=lambda _: election_name_dialogs(self.page),
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.5, '#44CCCCCC')
        )

        return self.election_name

    def manage_connection_option(self):
        self.create_election = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Manage Connection",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: manage_db_dialogs(self.page, True)
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.5, '#44CCCCCC'),
        )

        return self.create_election

    def help_option(self):
        self.help = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Help",
                        font_family='Verdana',
                    ),
                    on_click=lambda _: help_dialogs(self.page),
                    trailing=self.next_icon,
                ),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.5, '#44CCCCCC'),
        )

        return self.help

    def create_project(self):
        self.project = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"How to create Firebase Project",
                        font_family='Verdana',
                    ),
                    # on_click=lambda _: help_dialogs(self.page),
                    trailing=self.next_icon,
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
            ),
            color=ft.colors.with_opacity(0.5, '#44CCCCCC'),
            elevation=0,
        )

        return self.project

    def system_connected(self):
        self.systems = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Connected Devices",
                        font_family='Verdana',
                    ),
                    on_click=lambda _: system_dialogs(self.page),
                    trailing=self.next_icon,
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.5, '#44CCCCCC'),
        )

        return self.systems

    def change_in_data(self):
        self.app_data = pd.read_json(path + file_path['app_data'], orient='table')
        self.institution_name_text.value = self.app_data.at[0, 'institution_name']
        self.election_name_text.value = self.app_data.at[0, 'election_name']
        self.page.update()
        snackbar(self.page, "Settings Updated.")


def settings_page(page: ft.Page, main_column: ft.Column):
    global var_option_data_update
    option_menu = SettingsMenu(page)
    var_option_data_update = option_menu

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=3),
                option_menu.institution_name_option(),
                option_menu.election_name_option(),
                option_menu.manage_connection_option(),
                option_menu.system_connected(),
                option_menu.create_project(),
                option_menu.help_option(),
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )
    ]

    page.splash = None
    page.update()


def update_settings_data():
    var_option_data_update.change_in_data()

import flet as ft
import pandas as pd

from ..functions.date_time import current_time
import app.service.user.login_auth as cc
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path


def home_page(page: ft.Page, main_column: ft.Column):
    home_data = pd.read_json(path + file_path['app_data'], orient='table')

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=20),
                ft.Container(
                    margin=ft.margin.only(left=5, right=5),
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        value=f'{home_data.at[0, "institution_name"]}',
                        size=40,
                        font_family='Verdana',
                        color='#172554',
                        weight=ft.FontWeight.W_800,
                    )
                ),
                ft.Row(height=20),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                value=f"{current_time}, {cc.auth_data['displayName'].capitalize()}",
                                size=30,
                                font_family='Verdana',
                                italic=True,
                            ),
                            ft.Text(
                                value=f"Election Name: {home_data.at[0, 'election_name']}",
                                size=25,
                                font_family='Verdana',
                                italic=False,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=30,
                    margin=ft.margin.only(left=30, right=10),
                    height=200
                ),
                ft.Row(height=20),
                ft.Container(
                    margin=ft.margin.only(left=5, right=5),
                    padding=10,
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        [

                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    )
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]
    page.splash = None
    page.update()

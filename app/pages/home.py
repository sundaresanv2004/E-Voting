import flet as ft
import pandas as pd

from ..functions.date_time import current_time
import app.service.user.login_auth as cc
from ..service.firebase.firestore import read_home_data
from ..service.firebase.realtime_db import read_candidate


def home_page(page: ft.Page, main_column: ft.Column):
    home_data = read_home_data()
    candidate_data = read_candidate()

    student_container = ft.Container(
        width=300,
        height=150,
        border_radius=15,
        bgcolor='#44CCCCCC',
        alignment=ft.alignment.center,
        blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
        content=ft.ListTile(
            leading=ft.Icon(
                name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                size=40,
                color=ft.colors.BLACK
            ),
            title=ft.Text(
                value=f"{'0' if candidate_data is None else 'a'}",
                font_family='Verdana',
                weight=ft.FontWeight.W_400
            ),
            subtitle=ft.Text(
                value="No.of Candidates",
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_300,
                font_family='Verdana'
            ),
            width=300,
        )
    )

    staff_container = ft.Container(
        width=300,
        height=150,
        border_radius=15,
        bgcolor='#44CCCCCC',
        alignment=ft.alignment.center,
        blur=ft.Blur(20, 10, ft.BlurTileMode.MIRROR),
        content=ft.ListTile(
            leading=ft.Icon(
                name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                size=40,
                color=ft.colors.BLACK
            ),
            title=ft.Text(
                value=f"{'0' if home_data['election_settings']['final_nomination'] is False else '123123'}",
                font_family='Verdana',
                weight=ft.FontWeight.W_400
            ),
            subtitle=ft.Text(
                value="No.of Votes",
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_300,
                font_family='Verdana'
            ),
            width=300,
        )
    )

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=20),
                ft.Container(
                    margin=ft.margin.only(left=5, right=5),
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        value=home_data['appdata']['institution_name'],
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
                                value=f"Election Name: {home_data['appdata']['election_name']}",
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
                            student_container,
                            staff_container
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

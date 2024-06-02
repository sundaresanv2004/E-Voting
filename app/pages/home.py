import flet as ft
import pandas as pd

from ..functions.date_time import current_time


def home_page(page: ft.Page, main_column: ft.Column):

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
                value= "34",  # f"{len(candidate_data_df)}",
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

    # staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
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
                value="34", # f"{len(staff_df)}",
                font_family='Verdana',
                weight=ft.FontWeight.W_400
            ),
            subtitle=ft.Text(
                value="No.of Staff",
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_300,
                font_family='Verdana'
            ),
            width=300,
        )
    )

    # app_data_df = pd.read_json(path + file_path['app_data'], orient='table')
    # setting_df = pd.read_json(path + file_path['settings'], orient='table')

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=20),
                ft.Container(
                    margin=ft.margin.only(left=5, right=5),
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        value="Vels", # app_data_df[app_data_df.topic == 'institution_name'].values[0][1],
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
                                value=f"{current_time}, Sundar",  # {cc.teme_data[1].capitalize()}",
                                size=30,
                                font_family='Verdana',
                                italic=True,
                            ),
                            ft.Text(
                                value=f"Selected Name:  2024-25", # {setting_df.loc['Election'].values[0]}",
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

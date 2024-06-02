import flet as ft
import pandas as pd

from ..functions.dialogs import message_dialogs
from ..service.firebase.realtime_db import read_candidate

column_1 = ft.Column()
main_column1 = None
search_entry = ft.TextField(
    hint_text="Search",
    hint_style=ft.TextStyle(color='f2f9f9', font_family='Verdana'),
    width=450,
    border=ft.InputBorder.OUTLINE,
    height=55,
    disabled=True,
    border_radius=50,
    focused_border_color='#f2f9f9',
    border_color='#ddeff0',
    prefix_style=ft.TextStyle(color=ft.colors.WHITE),
    text_style=ft.TextStyle(font_family='Verdana'),
    prefix_icon=ft.icons.SEARCH_ROUNDED,
)


def candidate_home_page(page: ft.Page, main_column: ft.Column):
    global search_entry, column_1, main_column1

    main_column1 = main_column

    def search(e):
        pass
        # search_display_candidate(page)

    search_entry.on_change = search
    search_entry.value = None

    main_column.controls = [
        ft.Container(
            margin=ft.margin.only(left=5, right=5),
            content=search_entry,
            alignment=ft.alignment.center,
        ),
        ft.Container(
            padding=5,
            content=column_1,
            expand=True,
        ),
    ]
    page.update()
    page.splash = None
    display_candidate(page)


def display_candidate(page):
    global column_1
    # file
    candidate_data = read_candidate()

    row_can_data_list = []

    if candidate_data is None:
        row_can_data_list.append(
            ft.Row(
                [
                    ft.Text(
                        value="No record found",
                        size=25,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        column_1.alignment = ft.MainAxisAlignment.CENTER
    else:
        pass
        """for i in range(len(candidate_data.index)):
            row_can_data_list.append(ViewStaffRecord(page, main_column1, i))
        column_1.expand = True
        search_entry.disabled = False
        column_1.scroll = ft.ScrollMode.ADAPTIVE
"""
    column_1.controls = row_can_data_list
    page.update()



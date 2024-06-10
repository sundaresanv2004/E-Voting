import flet as ft
import pandas as pd
from time import sleep

from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path
from app.service.files.manage_files import create_category
from app.service.firebase.firestore import add_category_data


def category_dialogs(page: ft.Page):
    create_category()

    category_dialogs1 = ft.AlertDialog(
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_close(e):
        category_dialogs1.open = False
        page.update()

    def add_cat(e):
        category_dialogs1.open = False
        page.update()
        sleep(0.2)
        category_add_page(page, 'category')

    # Read category data
    category_data_df = pd.read_csv(path + file_path['category_data'])

    # Table
    category_data_table = ft.DataTable(
        column_spacing=20,
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Category ID")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Created On")),
        ],
    )

    category_data_row: list = []
    if len(category_data_df) != 0:
        for i in range(len(category_data_df)):
            category_data_row.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=f"{i + 1}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.at[i, 'category_id']}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.at[i, 'category_name']}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.at[i, 'created_at']}")),
                        # ft.DataCell(CategoryView(page, i, category_dialogs1, category_data_df))
                    ],
                )
            )

    category_data_table.rows = category_data_row
    data_list1: list = [
        ft.Row(
            [
                category_data_table,
            ],
        )
    ]

    if len(category_data_df) == 0:
        data_list1.append(
            ft.Row(
                [
                    ft.Text(
                        value="No Records",
                        size=20,
                    )
                ],
                width=700,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    # AlertDialog data
    category_dialogs1.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Category",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                                font_family='Verdana',
                            ),
                        ],
                        expand=True,
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
                width=760,
            ),
            ft.Column(
                controls=data_list1,
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=450,
        width=780,
    )

    ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')
    if not ele_ser_1.at[0, 'final_nomination']:
        category_dialogs1.actions = [
            ft.TextButton(
                text="Add new category",
                on_click=add_cat,
            )
        ]

    # Open dialog
    page.dialog = category_dialogs1
    category_dialogs1.open = True
    page.update()


def category_add_page(page: ft.Page, page_view):
    def on_close(e):
        add_category_alertdialog.open = False
        page.update()
        sleep(0.2)
        if page_view == 'candidate':
            from .candidate_add import candidate_add_page
            candidate_add_page(page)

    category_df = pd.read_csv(path + file_path['category_data'])
    if category_df.empty is True:
        category_list = []
    else:
        category_list = list(category_df['category_name'].unique())

    def add_new_category(e):
        if len(category_entry.value) != 0:
            if category_entry.value not in category_list:
                category_entry.error_text = None
                category_entry.update()
                add_category_data(category_entry.value)
                from ..functions.snack_bar import snackbar
                on_close(e)
                snackbar(page, "Successfully Added")
            else:
                category_entry.error_text = "It looks like this category has already been created."
                category_entry.focus()
                category_entry.update()
        else:
            category_entry.error_text = "Enter the Category"
            category_entry.focus()
            category_entry.update()

    def on_change_category(e):
        if category_entry.value in category_list:
            category_entry.error_text = "It looks like this category has already been created."
        else:
            category_entry.error_text = None
        category_entry.update()

    category_entry = ft.TextField(
        hint_text="Enter the Category",
        width=420,
        border=ft.InputBorder.OUTLINE,
        autofocus=True,
        border_radius=10,
        capitalization=ft.TextCapitalization.CHARACTERS,
        border_color=ft.colors.SECONDARY,
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=add_new_category,
        on_change=on_change_category,
    )

    content_column1 = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Add new Category",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                            )
                        ],
                        expand=True,
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
                ]
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            category_entry,
                        ],
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        height=150,
        width=450,
    )

    # AlertDialog data
    add_category_alertdialog = ft.AlertDialog(
        modal=True,
        content=content_column1,
        actions=[
            ft.TextButton(
                text="Add",
                on_click=add_new_category,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = add_category_alertdialog
    add_category_alertdialog.open = True
    page.update()

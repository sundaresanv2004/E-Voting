from time import sleep
import flet as ft
import pandas as pd

from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path
from app.service.firebase.realtime_db import get_image_url

index_val, ver_val = None, None


def candidate_profile_page(page: ft.Page, id_val):
    global index_val

    candidate_data_df = pd.read_json(path + file_path["candidate_data"], orient='table')

    def on_close(e):
        alertdialog.open = False
        page.update()

    index_val = id_val

    def next_fun(e):
        global index_val
        index_val += 1
        content_change()
        page.update()

    def back_fun(e):
        global index_val
        index_val -= 1
        content_change()
        page.update()

    next_button = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
        icon_size=30,
        tooltip='Next',
        on_click=next_fun,
    )

    back_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
        icon_size=30,
        tooltip="Previous",
        on_click=back_fun,
    )

    container = ft.Container(
        width=200,
        height=250,
        alignment=ft.alignment.center,
        border=ft.border.all(0.5, ft.colors.SECONDARY),
        border_radius=ft.border_radius.all(5),
    )

    def button_check():
        if index_val == 0:
            back_button.disabled = True
        else:
            back_button.disabled = False

        if index_val == candidate_data_df.index.max():
            next_button.disabled = True
        else:
            next_button.disabled = False

    def delete_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.1)
        # from .candidate_delete import delete_candidate_dialogs
        # delete_candidate_dialogs(page, index_val, True)

    def edit_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.2)
        # from .candidate_edit import candidate_edit_page
        # candidate_edit_page(page, index_val, True)

    title1 = ft.Text(
        weight=ft.FontWeight.W_500,
        size=20,
        font_family='Verdana',
    )

    name_text = ft.Text(
        size=20,
        font_family='Verdana',
    )

    category_text = ft.Text(
        size=20,
        font_family='Verdana',
    )

    added_on_text = ft.Text(
        size=20,
        font_family='Verdana',
    )

    added_by_text = ft.Text(
        size=20,
        font_family='Verdana',
    )

    def content_change():
        global ver_val
        button_check()
        title1.value = f"Candidate ID: {candidate_data_df.at[index_val, 'candidate_id']}"
        name_text.value = f"Name: {candidate_data_df.at[index_val, 'name']}"
        category_text.value = f"Category: {candidate_data_df.at[index_val, 'category']}"
        added_on_text.value = f"Created on: {candidate_data_df.at[index_val, 'created_at']}"
        added_by_text.value = f"Updated on: {candidate_data_df.at[index_val, 'updated_at']}"
        container.content = ft.Text()
        container.image_src = get_image_url(candidate_data_df.at[index_val, 'image'])
        container.image_fit = ft.ImageFit.COVER

    content_change()

    edit_button = ft.TextButton(
        text="Edit",
        icon=ft.icons.EDIT_ROUNDED,
        tooltip="Edit",
        on_click=edit_on_click,
    )

    delete_button = ft.TextButton(
        text="Delete",
        icon=ft.icons.DELETE_ROUNDED,
        tooltip='Delete',
        on_click=delete_on_click,
    )

    alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                title1,
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
                        back_button,
                        ft.Row(
                            [
                                container,
                                ft.Column(
                                    [
                                        name_text,
                                        category_text,
                                        added_on_text,
                                        added_by_text,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=25,
                            width=640,
                            scroll=ft.ScrollMode.ADAPTIVE,
                        ),
                        next_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    width=750,
                    height=320,
                ),

            ],
            height=370,
            width=750,
        ),
        actions=[
            edit_button,
            delete_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()

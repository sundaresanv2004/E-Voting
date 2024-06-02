import os
import glob
import shutil
import random
import string
from time import sleep
import flet as ft
import pandas as pd

from app.service.firebase.firestore import read_category_data
from .category import category_add_page

list_cand_data = ['', '', '']
save_button = ft.TextButton(
    text='Save',
    disabled=True,
)
alertdialog_candidate_add = None


def candidate_add_page(page: ft.Page):
    global alertdialog_candidate_add

    def add_cat(e):
        alertdialog_candidate_add.open = False
        page.update()
        category_add_page(page, 'candidate')

    def on_close(e):
        global list_cand_data
        alertdialog_candidate_add.open = False
        page.update()
        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) != 0:
                pass

        list_cand_data = ['', '', '', '', '']

    alertdialog_candidate_add = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    value="Add Candidate",
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
                    ]
                ),
                build(page)
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            height=360,
            width=650,
        ),
        actions=[
            ft.TextButton(
                text="Add new category",
                on_click=add_cat,
            ),
            save_button,
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    page.dialog = alertdialog_candidate_add
    alertdialog_candidate_add.open = True
    page.update()


def build(page: ft.Page):
    global list_cand_data

    def disable_button(e):
        global list_cand_data
        if len(name_entry.value) != 0:
            list_cand_data[0] = name_entry.value
            if category_dropdown.value is not None:
                if category_dropdown.value != "No Category Records":
                    list_cand_data[1] = category_dropdown.value
                    if list_cand_data[2] is not False:
                        save_button.disabled = False
                    else:
                        save_button.disabled = True
                else:
                    save_button.disabled = True
            else:
                save_button.disabled = True
        else:
            save_button.disabled = True
        save_button.update()

    def save(e):
        global list_cand_data, alertdialog_candidate_add
        alertdialog_candidate_add.open = False
        page.splash = ft.ProgressBar()
        page.update()
        # from ..service.files.write_files import add_candidate
        # from ..functions.snack_bar import snack_bar1
        sleep(0.2)
        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) == 0:
                image_data = False
            else:
                image_data = list_cand_data[1]
        else:
            image_data = False
        #add_candidate([name_entry.value, category_dropdown.value, True, qualification_dropdown.value, image_data,
        #    cc.teme_data[1]])
        page.splash = None
        page.update()
        from .candidate_home import display_candidate
        display_candidate(page)
        # snack_bar1(page, "Successfully Added")
        list_cand_data = ['', '', '', '', '']

    save_button.on_click = save

    # category_df = pd.read_csv(ee.current_election_path + rf'/{file_data["category_data"]}')
    # candidate_image_destination = ee.current_election_path + r'/images'

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Candidate name",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        autofocus=True,
        capitalization=ft.TextCapitalization.WORDS,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        on_change=disable_button,
    )

    category_dropdown = ft.Dropdown(
        hint_text="Choose Candidate Category",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        text_style=ft.TextStyle(font_family='Verdana'),
        color=ft.colors.BLACK,
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_change=disable_button,
    )

    container = ft.Container(
        content=ft.Text("Upload Image", font_family='Verdana'),
        width=200,
        height=250,
        alignment=ft.alignment.center,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=10,
        image_fit=ft.ImageFit.COVER,
    )

    category_df = read_category_data()
    print(category_df)

    temp_list: list = []
    if category_df is not None:
        for i in list(category_df.values()):
            temp_list.append(ft.dropdown.Option(i))
    else:
        temp_list.append(ft.dropdown.Option("No Category Records"))

    category_dropdown.options = temp_list

    def pick_files_result(e: ft.FilePickerResultEvent):
        global list_cand_data
        # from ..functions.dialogs import error_dialogs
        candidate_image_destination1 = r'/images'

        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) != 0:
                candidate_image_destination1 += rf'/{list_cand_data[1]}'
                try:
                    os.remove(candidate_image_destination1)
                except FileNotFoundError:
                    pass

        selected_image_name = "".join(map(lambda f: f.name, e.files)) if e.files else False
        selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False
        if selected_image_name is not False:
            pass
        else:
            container.image_src = None
            container.content = ft.Text("Upload canceled!", font_family='Verdana', )
            container.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    upload_button = ft.TextButton(
        text="Upload Image",
        icon=ft.icons.FILE_UPLOAD_ROUNDED,
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE),
    )

    main_column = ft.Row(
        [
            ft.Column(
                [

                    ft.Row(
                        [
                            ft.Column(
                                [
                                    container,
                                    upload_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    name_entry,
                                    category_dropdown,
                                ],
                                spacing=40,
                            )
                        ],
                        height=300,
                        spacing=50,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    return main_column

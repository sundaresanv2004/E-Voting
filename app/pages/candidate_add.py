from time import sleep
import flet as ft
import pandas as pd

from .category import category_add_page
from ..functions.dialogs import loading_dialogs
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path

list_cand_data = ['', '', None, '']
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
        sleep(0.2)
        category_add_page(page, 'candidate')

    def on_close(e):
        global list_cand_data
        alertdialog_candidate_add.open = False
        page.update()
        list_cand_data = ['', '', None, '']

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
                    if list_cand_data[2] is not None:
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

    category_df = pd.read_csv(path + file_path['category_data'])

    def save(e):
        global list_cand_data, alertdialog_candidate_add
        alertdialog_candidate_add.open = False
        page.splash = ft.ProgressBar()
        dig = loading_dialogs(page, "Saving...")
        page.update()
        from ..service.firebase.realtime_db import add_candidate
        from ..functions.snack_bar import snackbar
        index_val = category_df[category_df.category_name == category_dropdown.value].index.values[0]
        category = category_df.at[index_val, 'category_id']
        add_candidate([
            name_entry.value,
            category,
            list_cand_data[2],
            list_cand_data[3],
        ])
        page.splash = None
        dig.open = False
        page.update()
        from .candidate_home import display_candidate
        display_candidate(page)
        snackbar(page, "Successfully Added")
        list_cand_data = ['', '', None, '']

    save_button.on_click = save

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Candidate name",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        autofocus=True,
        capitalization=ft.TextCapitalization.WORDS,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        on_change=disable_button,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
    )

    category_dropdown = ft.Dropdown(
        hint_text="Choose Candidate Category",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        color=ft.colors.BLACK,
        options=[
            ft.dropdown.Option("Select Candidate Qualification"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_change=disable_button,
    )

    container = ft.Container(
        content=ft.Text("Upload Image", font_family='Verdana'),
        width=200,
        height=250,
        border=ft.border.all(1, ft.colors.BLACK),
        alignment=ft.alignment.center,
        border_radius=10,
        image_fit=ft.ImageFit.COVER,
    )

    temp_list1: list = []
    if not category_df.empty:
        for i in list(category_df['category_name'].unique()):
            temp_list1.append(ft.dropdown.Option(i))
    else:
        temp_list1.append(ft.dropdown.Option("No Category Records"))

    category_dropdown.options = temp_list1

    if len(list_cand_data[0]) != 0:
        name_entry.value = list_cand_data[0]

    if len(list_cand_data[1]) != 0:
        category_dropdown.value = list_cand_data[3]

    if list_cand_data[2] is not None:
        container.image_src = list_cand_data[3]
        container.content = None

    def pick_files_result(e: ft.FilePickerResultEvent):
        global list_cand_data
        from ..functions.dialogs import error_dialogs

        selected_image_name = "".join(map(lambda f: f.name, e.files)) if e.files else False
        selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False

        if selected_image_name is not False:
            list_cand_data[2] = selected_image_name
            list_cand_data[3] = selected_file_path
            container.image_src = selected_file_path
            container.content = None
            container.update()
            try:
                pass
            except OSError:
                container.content = ft.Text("Upload Image", font_family='Verdana', )
                container.update()
                list_cand_data[1] = ''
                error_dialogs(page, "002")
        else:
            container.image_src = None
            container.content = ft.Text("Upload canceled!", font_family='Verdana', )
            container.update()
        disable_button(e)

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
                                spacing=35,
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

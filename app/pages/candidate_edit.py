import flet as ft
import pandas as pd

from .candidate_profile import candidate_profile_page
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..service.firebase.realtime_db import get_image_url

list_cand_data_edit = ['', '', None, '']
save_button = ft.TextButton(
    text='Save Changes',
    disabled=True,
)
alertdialog_candidate_edit = None


def candidate_edit_page(page: ft.Page, index_val, page_view):
    global alertdialog_candidate_edit

    def on_close_edit(e):
        global list_cand_data_edit
        save_button.disabled = True
        alertdialog_candidate_edit.open = False
        page.update()
        list_cand_data_edit = ['', '', None, '']
        if page_view:
            candidate_profile_page(page, index_val)

    alertdialog_candidate_edit = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    value="Edit Candidate",
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
                                    on_click=on_close_edit,
                                )
                            ]
                        )
                    ]
                ),
                build(page, index_val, page_view)
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            height=360,
            width=650,
        ),
        actions=[
            save_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    page.dialog = alertdialog_candidate_edit
    alertdialog_candidate_edit.open = True
    page.update()


def build(page: ft.Page, index_val, page_view):
    global list_cand_data_edit
    candidate_df = pd.read_json(path + file_path["candidate_data"], orient='table')
    candidate_data = candidate_df.loc[index_val].values
    list_cand_data_edit[0] = candidate_df.at[index_val, 'name']
    list_cand_data_edit[1] = candidate_df.at[index_val, 'category']
    list_cand_data_edit[2] = candidate_df.at[index_val, 'image']

    def disable_button(e):
        global list_cand_data_edit
        list_value: list = [False, False, False]
        if name_entry.value != candidate_df.at[index_val, 'name']:
            if len(name_entry.value) != 0:
                name_entry.error_text = None
                name_entry.update()
                list_value[0] = True
                list_cand_data_edit[0] = name_entry.value
            else:
                name_entry.error_text = "Enter the Name"
                name_entry.update()
        else:
            list_value[0] = False

        if category_dropdown.value != candidate_df.at[index_val, 'category']:
            if len(category_dropdown.value) != 0:
                category_dropdown.error_text = None
                category_dropdown.update()
                list_value[1] = True
                list_cand_data_edit[1] = category_dropdown.value
            else:
                category_dropdown.error_text = "Select a Category"
                category_dropdown.update()
                list_value[1] = False
        else:
            list_value[1] = False

        if list_cand_data_edit[2] != candidate_df.at[index_val, 'image']:
            list_value[2] = True
        else:
            list_value[2] = False

        if True in list_value:
            if list_cand_data_edit[2] is not False:
                save_button.disabled = False
            else:
                save_button.disabled = True
        else:
            save_button.disabled = True
        save_button.update()

    def save(e):
        global list_cand_data_edit, alertdialog_candidate_edit
        alertdialog_candidate_edit.open = False
        page.splash = ft.ProgressBar()
        page.update()
        from ..service.firebase.realtime_db import edit_candidate
        from ..functions.snack_bar import snackbar
        if list_cand_data_edit[2] == candidate_df.at[index_val, 'image']:
            list_cand_data_edit[2] = False
        edit_candidate(
            index_val,
            [name_entry.value,
             category_dropdown.value,
             list_cand_data_edit[2],
             list_cand_data_edit[3]
             ])
        page.splash = None
        page.update()
        from .candidate_home import display_candidate
        display_candidate(page)
        if page_view:
            candidate_profile_page(page, index_val)
        snackbar(page, "Successfully Updated")
        list_cand_data_edit = ['', '', None, '']

    save_button.on_click = save

    category_df = pd.read_csv(path + file_path['category_data'])

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Candidate name",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
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
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
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
        alignment=ft.alignment.center,
        border=ft.border.all(1, ft.colors.BLACK),
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

    if len(list_cand_data_edit[0]) != 0:
        name_entry.value = list_cand_data_edit[0]

    if len(list_cand_data_edit[1]) != 0:
        category_dropdown.value = list_cand_data_edit[1]

    if list_cand_data_edit[2] is not None:
        container.image_src = get_image_url(list_cand_data_edit[2])
        container.content = None

    def pick_files_result(e: ft.FilePickerResultEvent):
        global list_cand_data_edit
        from ..functions.dialogs import error_dialogs

        selected_image_name = "".join(map(lambda f: f.name, e.files)) if e.files else False
        selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False

        if selected_image_name is not False:
            list_cand_data_edit[2] = selected_image_name
            list_cand_data_edit[3] = selected_file_path
            container.image_src = selected_file_path
            container.content = None
            container.update()
            try:
                pass
            except OSError:
                container.content = ft.Text("Upload Image", font_family='Verdana', )
                container.update()
                list_cand_data_edit[1] = ''
                error_dialogs(page, "002")
        else:
            container.image_src = get_image_url(list_cand_data_edit[2])
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

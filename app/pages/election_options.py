import os
import flet as ft
import pandas as pd

from ..functions.dialogs import error_dialogs
from ..service.files.check_installation import path
from ..service.files.local_files_scr import messages, file_path
from ..service.firebase.firestore import update_vote_option


def category_order(page: ft.Page):
    from ..functions.order_category import order_category_option

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_next1(e):
        message_alertdialog.open = False
        page.update()

        order_category_option(page)

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Choose Order", font_family='Verdana')
        message_alertdialog.content = ft.Text(value=messages['final_list'], font_family='Verdana')
        message_alertdialog.actions = [
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
        ]

        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Warning!",
            font_family='Verdana',
            weight=ft.FontWeight.W_500,
            color=ft.colors.RED_500,
        ),
        content=ft.Text(
            value=messages['make_sure'],
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Continue",
                on_click=on_next,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()


def download_nomination(page: ft.Page):
    def save_file_nomination(e: ft.FilePickerResultEvent):
        download_nomination_alertdialog1.open = False
        page.update()
        path1 = e.path if e.path else False
        path_download = str(path1)
        if path_download != "False":
            candidate_df = pd.read_json(path + file_path["candidate_data"], orient='table')
            category_df = pd.read_csv(path + file_path['category_data'])
            category_df.dropna(subset=['order'], inplace=True, axis=0, ignore_index=True)
            category_dict = {}
            for i in range(len(category_df)):
                category_dict[category_df.at[i, 'category_id']] = category_df.at[i, 'category_name']

            for i in range(len(candidate_df)):
                if candidate_df.at[i, 'category'] in list(category_dict.keys()):
                    candidate_df.at[i, 'category'] = category_dict[candidate_df.at[i, 'category']]
                else:
                    candidate_df.drop(i, inplace=True, axis=0)

            new_df = candidate_df[['candidate_id', 'name', 'category', 'created_at', 'updated_at']]
            try:
                new_df.to_csv(path_download, index=False)
            except PermissionError:
                error_dialogs(page, '003')
            page.remove(save_file_dialog)
            os.system(path_download)

    save_file_dialog = ft.FilePicker(on_result=save_file_nomination)

    def on_ok(e):
        download_nomination_alertdialog1.open = False
        page.update()
        page.remove(save_file_dialog)

    # AlertDialog data
    download_nomination_alertdialog1 = ft.AlertDialog(
        modal=False,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Download Nomination List", size=20, font_family='Verdana'),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE_ROUNDED,
                                    icon_size=30,
                                    tooltip="Close",
                                    on_click=on_ok,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.FILE_DOWNLOAD_ROUNDED,
                                    tooltip='Download',
                                    on_click=lambda _: save_file_dialog.save_file(file_name="Nomination_List.csv",
                                                                                  file_type=ft.FilePickerFileType.ANY),
                                    disabled=page.web,
                                )
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    expand=True,
                )
            ],
            width=350,
            height=120,
        )
    )

    # Open dialog
    page.dialog = download_nomination_alertdialog1
    download_nomination_alertdialog1.open = True
    page.update()
    page.add(save_file_dialog)


def vote_options(value):
    from .election_settings import update_election_set
    update_vote_option(value)
    update_election_set()


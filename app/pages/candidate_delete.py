from time import sleep
import flet as ft
import pandas as pd

from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path
from app.service.firebase.realtime_db import delete_candidate


def delete_candidate_dialogs(page: ft.Page, index_df, view):
    def del_ok(e):
        page.snack_bar = ft.ProgressBar()
        page.update()
        from ..functions.snack_bar import snackbar
        delete_candidate_dialogs1.open = False
        page.update()
        from .candidate_home import display_candidate
        delete_candidate(page, index_df)
        page.snack_bar = False
        snackbar(page, "Successfully Deleted.")
        page.update()
        display_candidate(page)
        candidate_data_df = pd.read_json(path + file_path["candidate_data"], orient='table')
        list1 = candidate_data_df.index.values
        if view is True:
            from .candidate_profile import candidate_profile_page
            if index_df in list1:
                candidate_profile_page(page, index_df)
            elif index_df - 1 in list1:
                candidate_profile_page(page, index_df - 1)

    def on_close(e):
        delete_candidate_dialogs1.open = False
        page.update()
        if view is True:
            sleep(0.1)
            from .candidate_profile import candidate_profile_page
            candidate_profile_page(page, index_df)

    # AlertDialog
    delete_candidate_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            font_family='Verdana',
            value="Delete this record?",
        ),
        actions=[
            ft.TextButton(
                on_click=del_ok,
                text="Ok",
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
        ],
        content=ft.Text(
            value="This record will be deleted forever.",
            font_family='Verdana',
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = delete_candidate_dialogs1
    delete_candidate_dialogs1.open = True
    page.update()


"""
def approve_dialogs(page: ft.Page, content_column: ft.Column, title_text, id_val, ver_val, page_type):
    from .candidate_profile import candidate_profile_page

    def on_no(e):
        alertdialog.open = False
        page.update()
        if page_type:
            sleep(0.1)
            candidate_profile_page(page, content_column, title_text, id_val)

    def on_yes(e):
        from ..authentication.files.write_files import change_verification
        alertdialog.open = False
        page.update()
        change_verification(page, id_val)
        if page_type:
            sleep(0.1)
            candidate_profile_page(page, content_column, title_text, id_val)
        else:
            from Main.pages.candidate_home import candidate_home_page
            page.update()
            content_column.clean()
            content_column.update()
            candidate_home_page(page, content_column, title_text)

    if ver_val == False:
        ver_text_1 = ft.Text(
            value="Would you like to approve this candidate for the position?"
        )
    else:
        ver_text_1 = ft.Text(
            value="Would you like to reject this candidate from the position?"
        )

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Make Sure",
        ),
        content=ver_text_1,
        actions=[
            ft.TextButton(
                text="Yes",
                on_click=on_yes,
            ),
            ft.TextButton(
                text="No",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
"""

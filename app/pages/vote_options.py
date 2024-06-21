import shutil

import flet as ft
import pandas as pd

from app.service.files.check_installation import path


def vote_exit(page: ft.Page, election_path, turbo: bool) -> None:
    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()

    def on_yes(e):
        on_no(e)

        exit_confirm_dialog.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"Uploading...",
                            size=25,
                            italic=True,
                            font_family='Verdana',
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ProgressRing(),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            height=180,
            width=130,
        )

        exit_confirm_dialog.actions = []
        exit_confirm_dialog.title = None
        page.update()
        from app.service.files.manage_files import vote_end
        vote_end(page, election_path)
        page.update()
        page.window_full_screen = False
        page.update()
        page.window_maximized = True
        page.update()
        page.clean()
        page.update()
        from main import main
        main(page)

    exit_confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Exit"),
        content=ft.Text("Are you sure do you want to exit?", font_family='Verdana'),
        actions=[
            ft.TextButton(
                "No",
                on_click=on_no,
                disabled=turbo,
            ),
            ft.TextButton(
                "Yes",
                on_click=on_yes,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.update()


def vote_done(page: ft.Page, appbar, main_column, election_path):
    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()
        election_log = pd.read_json(election_path + r'/election_datalog.json', orient='table')
        file_destination = path + rf'/backup{election_log.at[0, "file_name"]}'
        shutil.copy(election_path + election_log.at[0, 'file_name'], file_destination)
        from .vote_home import vote_content_page
        vote_content_page(page, appbar, main_column, election_path)

    exit_confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Successfully Done"),
        content=ft.Text("Thank you for voting! Your data has been securely saved.", font_family='Verdana'),
        actions=[
            ft.TextButton(
                "Ok",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.update()

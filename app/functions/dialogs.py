from time import sleep
import flet as ft
import shutil

from ..service.files.local_files_scr import warnings


def message_dialogs(page: ft.Page, message_key: str):
    def on_ok(e):
        message_alertdialog.open = False
        page.update()
        if message_key == "Restart Required":
            page.window_destroy()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"{message_key}",
            font_family='Verdana',
        ),
        content=ft.Text(
            value=f"{warnings[message_key]}",
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Ok",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()


def loading_dialogs(page: ft.Page, text: str) -> ft.AlertDialog:
    alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"{text}",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                            font_family='Verdana',
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
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()

    return alertdialog

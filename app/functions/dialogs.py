from time import sleep

import flet as ft

from app.service.files.local_files_scr import warnings, error_data


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


def network_error(page: ft.Page, error: Exception):
    def on_retry(e):
        from main import main
        page.clean()
        main(page)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Network Error!",
            font_family='Verdana',
            weight=ft.FontWeight.W_500,
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            name=ft.icons.SIGNAL_WIFI_STATUSBAR_CONNECTED_NO_INTERNET_4_ROUNDED,
                            size=25,
                        ),
                        ft.Text(
                            value="Unable to connect to the internet. Please check your internet connection.",
                            font_family='Verdana',
                        ),
                    ],
                ),
                ft.Column(
                    [
                        ft.ExpansionTile(
                            title=ft.Text(
                                value="Show detail"
                            ),
                            affinity=ft.TileAffinity.TRAILING,
                            maintain_state=True,
                            shape=ft.RoundedRectangleBorder(
                                radius=30,
                            ),
                            controls=[
                                ft.ListTile(
                                    title=ft.Text(
                                        f"{error}"
                                    )
                                )
                            ],
                        )
                    ],
                    height=180,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            ],
            height=200,
            width=600,
        ),
        actions=[
            ft.TextButton(
                text="Retry",
                icon=ft.icons.REFRESH_ROUNDED,
                on_click=on_retry,
            ),
        ]
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()

    # return alertdialog


def error_dialogs(page: ft.Page, error_key: str):
    def on_ok(e):
        alertdialog.open = False
        page.update()

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Error {error_key}!",
            font_family='Verdana',
        ),
        content=ft.Text(
            value=f"{error_data[error_key]}",
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

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def error_message_dialogs(page: ft.Page, error_key: str):

    def on_ok(e):
        alertdialog.open = False
        page.update()
        # election_data_missing(page)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Error!",
            font_family='Verdana',
        ),
        content=ft.Text(
            value=f"{error_key}",
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

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()

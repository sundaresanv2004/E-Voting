import flet as ft


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

import flet as ft

from app.service.read_write.settings_file import on_close_change


def close_true(page: ft.Page):
    def on_no(e):
        from ..service.connection.check_files import check_connection_files
        exit_confirm_dialog.open = False
        page.update()
        check_connection_files(page)

    def on_yes(e):
        if check_box.value is True:
            on_close_change(False)
        page.window_destroy()

    check_box = ft.Checkbox(
        label="Don't ask again",
        adaptive=True,
        label_style=ft.TextStyle(font_family='Verdana'),
    )

    exit_confirm_dialog = ft.AlertDialog(
        modal=False,
        title=ft.Row(
            [
                ft.Icon(
                    name=ft.icons.QUESTION_MARK_ROUNDED,
                ),
                ft.Text(
                    value="Confirm Exit",
                    font_family='Verdana',
                ),
            ]
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(width=5),
                        ft.Text(
                            value="Are you sure do you want to exit?",
                            font_family='Verdana',
                        ),
                    ]
                ),
                check_box
            ],
            height=50,
            width=320,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.START,

        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_no
            ),
            ft.OutlinedButton(
                text="Exit",
                on_click=on_yes
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.update()

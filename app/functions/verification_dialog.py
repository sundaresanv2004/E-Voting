import flet as ft
from time import sleep

verified: bool = False
verified_dialog_open: bool = True


def verification_dialogs(page: ft.Page, email_id, ver_code):
    global verified, verified_dialog_open
    verified = False
    verified_dialog_open = True

    def on_cancel(e):
        global verified_dialog_open
        verified_dialog_open = False
        code_alertdialog.open = False
        page.update()

    def on_ok(e):
        global verified
        if len(entry.value) != 0:
            if entry.value == ver_code:
                code_alertdialog.actions.remove(submit_button)
                code_alertdialog.actions.append(load_ring)
                cancel_button.disabled = True
                entry.disabled = True
                page.update()
                sleep(0.5)
                verified = True
                on_cancel(e)
            else:
                entry.error_text = "Invalid code! Try again."
                entry.focus()
        else:
            entry.error_text = "Enter the code"
            entry.focus()
        page.update()

    entry = ft.TextField(
        hint_text="Enter the code",
        width=330,
        filled=False,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        autofocus=True,
        border_color=ft.colors.BLACK,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_ok,
    )

    cancel_button = ft.TextButton(
        text="Cancel",
        on_click=on_cancel,
    )

    submit_button = ft.TextButton(
        text="Submit",
        on_click=on_ok,
    )

    load_ring = ft.ProgressRing(
        height=20,
        width=20,
        stroke_width=3,
    )

    code_alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Enter the code",
                            font_family='Verdana',
                            weight=ft.FontWeight.W_800,
                            size=25,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                    image_src='/images/verification_img.png',
                                    image_fit=ft.ImageFit.COVER,
                                    height=200,
                                    width=200
                                ),
                                ft.Text(
                                    value=f"Code sent to:",
                                    font_family='Verdana',
                                    weight=ft.FontWeight.W_500,
                                    size=19,
                                ),
                                ft.Text(
                                    value=f"{email_id}",
                                    font_family='Verdana',
                                ),
                                ft.Column(height=15),
                                entry,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            height=420,
            width=380,
        ),
        actions=[
            cancel_button,
            submit_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = code_alertdialog
    code_alertdialog.open = True
    page.update()

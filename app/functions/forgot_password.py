import flet as ft
import re

from app.service.firebase.connect_firebase import admin_data


def forgot_password_dialog(page: ft.Page):
    def on_ok(e):
        forgot_password_alertdialog.open = False
        page.update()

    # Valid Mail checker
    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def on_submit_click(e):
        if len(mail_entry.value) != 0:
            if re.fullmatch(mail_check, mail_entry.value):
                admin_data()
            else:
                mail_entry.error_text = "Enter the valid email address"
                mail_entry.focus()
        else:
            mail_entry.error_text = "Enter your email address"
            mail_entry.focus()
        page.update()

    mail_entry = ft.TextField(
        hint_text="Enter your email address",
        width=400,
        filled=False,
        autofocus=True,
        prefix_icon=ft.icons.MAIL_ROUNDED,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_submit_click,
    )

    # AlertDialog data
    forgot_password_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Forgot password?",
            font_family='Verdana',
        ),
        content=ft.Row(
            [
                mail_entry
            ],
            width=400
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Send Code",
                on_click=on_submit_click,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = forgot_password_alertdialog
    forgot_password_alertdialog.open = True
    page.update()

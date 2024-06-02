import flet as ft
import re
from time import sleep

from app.service.firebase.auth import admin_data_email, update_password
from app.service.user.code_verification import verify_code_email

emails = None


def forgot_password_dialog(page: ft.Page):
    global emails
    emails = None

    def on_ok(e):
        forgot_password_alertdialog.open = False
        page.update()

    # Valid Mail checker
    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def on_submit_click(e):
        global emails
        if len(mail_entry.value) != 0:
            if re.fullmatch(mail_check, mail_entry.value):
                mail_entry.error_text = None
                forgot_password_alertdialog.actions.remove(send_code_button)
                forgot_password_alertdialog.actions.append(load_ring)
                close_button.disabled = True
                page.update()
                sleep(0.5)
                if emails is None:
                    emails = admin_data_email(page)

                if mail_entry.value in emails.keys():
                    user_id = emails[mail_entry.value]
                    mail_entry.error_text = None
                    mail_entry.update()
                    if verify_code_email(page, mail_entry.value, "Your Password Reset Verification Code") is True:
                        update_password_dialog(page, user_id)
                else:
                    mail_entry.error_text = "Email address not found!"
                    mail_entry.focus()
                forgot_password_alertdialog.actions.remove(load_ring)
                forgot_password_alertdialog.actions.append(send_code_button)
                close_button.disabled = False
                page.update()
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

    close_button = ft.TextButton(
        text="Cancel",
        on_click=on_ok,
    )

    send_code_button = ft.TextButton(
        text="Send Code",
        on_click=on_submit_click,
    )

    load_ring = ft.ProgressRing(
        height=20,
        width=20,
        stroke_width=3,
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
            close_button,
            send_code_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = forgot_password_alertdialog
    forgot_password_alertdialog.open = True
    page.update()


def update_password_dialog(page: ft.Page, user_id):
    def on_ok(e):
        forgot_password_alertdialog.open = False
        page.update()

    def on_submit_click(e):
        if len(password_entry.value) != 0:
            if len(password_entry.value) >= 8:
                password_entry.error_text = None
                if len(conform_password.value) != 0:
                    if password_entry.value == conform_password.value:
                        conform_password.error_text = None
                        forgot_password_alertdialog.actions.remove(send_code_button)
                        forgot_password_alertdialog.actions.append(load_ring)
                        close_button.disabled = True
                        page.update()
                        update_password(page, user_id, password_entry.value)
                        on_ok(e)
                    else:
                        conform_password.error_text = "Password didn't match!"
                        conform_password.focus()
                else:
                    conform_password.error_text = "Enter your password again!"
                    conform_password.focus()
            else:
                password_entry.error_text = "Password should be least 8 characters long!"
                password_entry.focus()
        else:
            password_entry.error_text = "Enter your password!"
            password_entry.focus()
        page.update()

    password_entry = ft.TextField(
        hint_text="Enter your new password",
        width=350,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        autofocus=True,
        border_color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_submit_click,
    )

    conform_password = ft.TextField(
        hint_text="Conform your new password",
        width=350,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border_radius=10,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_submit_click,
    )

    close_button = ft.TextButton(
        text="Cancel",
        on_click=on_ok,
    )

    send_code_button = ft.TextButton(
        text="Update",
        on_click=on_submit_click,
    )

    load_ring = ft.ProgressRing(
        height=20,
        width=20,
        stroke_width=3,
    )

    # AlertDialog data
    forgot_password_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Update Password",
            font_family='Verdana',
        ),
        content=ft.Column(
            [
                password_entry,
                conform_password,
            ],
            spacing=20,
            height=180,
            width=370,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[
            close_button,
            send_code_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = forgot_password_alertdialog
    forgot_password_alertdialog.open = True
    page.update()

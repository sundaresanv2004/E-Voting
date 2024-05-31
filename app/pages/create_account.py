import re
from datetime import datetime
from time import sleep

import flet as ft

from ..functions.dialogs import message_dialogs
from ..service.user.code_verification import verify_code_email

institution_name = None
election_name = False


def create_account_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    global institution_name, election_name

    def back(e):
        global institution_name
        institution_name = None
        from .start_menu import start_menu_page
        content_image.height = 370
        content_image.update()
        sleep(0.2)
        content_column.clean()
        page.update()
        start_menu_page(page, content_image, content_column)

    def check_entry_valid(e):
        if len(type_name_entry.value) != 0:
            type_name_entry.suffix_icon = None
            type_name_entry.error_text = None
        else:
            type_name_entry.error_text = "Enter the institution name!"
            type_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        type_name_entry.update()

    def check_election_name_valid(e):
        if len(election_name_entry.value) != 0:
            election_name_entry.suffix_icon = None
            election_name_entry.error_text = None
        else:
            election_name_entry.error_text = "Enter the election name!"
            election_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        election_name_entry.update()

    def next_button_click(e):
        global institution_name, election_name
        check_entry_valid(e)
        check_election_name_valid(e)

        if len(type_name_entry.value) != 0:
            if len(election_name_entry.value) != 0:
                button_container.content = ft.ProgressRing()
                page.update()
                type_name_entry.disabled = True
                election_name_entry.disabled = True
                button_container.disabled = True
                button_container.opacity = 0.5
                page.update()
                sleep(0.4)
                institution_name = type_name_entry.value
                election_name = election_name_entry.value
                content_image.height = 0
                content_image.update()
                content_column.clean()
                page.update()
                sign_up_page(page, content_image, content_column)
            else:
                election_name_entry.focus()
                election_name_entry.update()
        else:
            type_name_entry.focus()
            page.update()

    election_name_entry = ft.TextField(
        hint_text="Enter the election name",
        width=330,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_election_name_valid,
        on_submit=next_button_click,
    )

    type_name_entry = ft.TextField(
        hint_text="Enter the institution name",
        width=330,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_entry_valid,
        on_submit=next_button_click,
    )

    if institution_name is not None:
        type_name_entry.value = institution_name
        election_name_entry.value = election_name

    button_container = ft.ElevatedButton(
        text="Next",
        height=50,
        width=340,
        on_click=next_button_click,
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="New Election",
                            size=25,
                            font_family='Verdana',
                            color='#0c4a6e',
                            weight=ft.FontWeight.W_800,
                        ),
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        type_name_entry,
                        election_name_entry,
                        button_container,
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
            ],
            width=450,
            height=320,
            spacing=20,
        ),
        ft.Container(
            ft.Row(
                [
                    ft.TextButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        on_click=back,
                    )
                ],
                width=450,
            ),
            bgcolor="#44CCCCCC",
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
        )
    ]

    page.update()


def sign_up_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    def back(e):
        content_image.height = 170
        content_image.update()
        sleep(0.4)
        content_column.clean()
        page.update()
        create_account_page(page, content_image, content_column)

    def check_username_entry(e):
        if len(username_entry.value) != 0:
            username_entry.suffix_icon = None
            username_entry.error_text = None
        else:
            username_entry.error_text = "Enter the username"
            username_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        username_entry.update()

    # Valid Mail checker
    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def check_mail_id_entry(e):
        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                mail_id_entry.suffix_icon = ft.icons.CHECK_CIRCLE
                mail_id_entry.error_text = None
            else:
                mail_id_entry.error_text = "Enter the valid email address"
                mail_id_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
        else:
            mail_id_entry.error_text = "Enter your email address"
            mail_id_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        mail_id_entry.update()

    def check_password_entry(e):
        if len(password_entry.value) != 0:
            if len(password_entry.value) >= 8:
                password_entry.error_text = None
            else:
                password_entry.error_text = "Password should be least 8 characters long!"
        else:
            password_entry.error_text = "Enter the password"
        password_entry.update()

    def on_submit_click(e):
        check_username_entry(e)
        check_mail_id_entry(e)
        check_password_entry(e)

        if len(username_entry.value) != 0:
            if len(mail_id_entry.value) != 0:
                if re.fullmatch(mail_check, mail_id_entry.value):
                    if len(password_entry.value) != 0:
                        if len(password_entry.value) >= 8:
                            if verify_code_email(page):
                                button_container.content = ft.ProgressRing()
                                page.update()
                                back_button.disabled = True
                                button_y_admin_details.disabled = True
                                username_entry.disabled = True
                                password_entry.disabled = True
                                mail_id_entry.disabled = True
                                button_container.disabled = True
                                button_container.opacity = 0.5
                                page.update()
                                sleep(0.5)

                                from ..service.firebase.connect_firebase import create_user, app_data, system_data
                                create_user(page, {
                                    "username": username_entry.value,
                                    "password": password_entry.value,
                                    "email": mail_id_entry.value,
                                })

                                app_data(
                                    {
                                        "institution_name": institution_name,
                                        "election_name": election_name,
                                        "created_datetime": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                    }
                                )
                                system_data(True)

                                sleep(1)
                                content_column.clean()
                                page.update()
                                from .all_done import all_done_page
                                all_done_page(page, content_column)
                                sleep(0.5)

                                from ..functions.snack_bar import snackbar
                                snackbar(page, "Successfully completed the app setup!🎉")
                            else:
                                mail_id_entry.error_text = "Enter the valid email address"
                                mail_id_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
                        else:
                            password_entry.focus()
                            password_entry.update()
                    else:
                        password_entry.focus()
                        password_entry.update()
                else:
                    mail_id_entry.focus()
                    mail_id_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            username_entry.focus()
            username_entry.update()

    # button
    back_button = ft.TextButton(
        text="Back",
        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
        on_click=back,
    )

    # Why admin details button
    button_y_admin_details = ft.TextButton(
        text="Read Me!",
        on_click=lambda e: message_dialogs(page, 'Read Me!'),
    )

    # Input Fields
    username_entry = ft.TextField(
        hint_text="Enter your username",
        width=330,
        filled=False,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_username_entry,
        on_submit=on_submit_click,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter your email address",
        width=330,
        filled=False,
        prefix_icon=ft.icons.MAIL_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_mail_id_entry,
        on_submit=on_submit_click,
    )

    password_entry = ft.TextField(
        hint_text="Enter your password",
        width=330,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_password_entry,
        on_submit=on_submit_click,
    )

    button_container = ft.ElevatedButton(
        text="Sign Up",
        height=50,
        width=340,
        on_click=on_submit_click,
    )

    content_column.controls = [
        ft.Row(height=20),
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Sign Up",
                            size=30,
                            font_family='Verdana',
                            color='#0c4a6e',
                            weight=ft.FontWeight.W_800,
                        ),
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        username_entry,
                        mail_id_entry,
                        password_entry,
                        button_container
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=40,
                ),
            ],
            width=450,
            height=460,
            spacing=20,
            scroll=ft.ScrollMode.ADAPTIVE
        ),
        ft.Container(
            content=ft.Row(
                [
                    back_button,
                    button_y_admin_details
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450,
            ),
            bgcolor='#44CCCCCC',
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
        )
    ]

    page.update()


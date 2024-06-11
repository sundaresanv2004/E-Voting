import flet as ft
import re
from time import sleep


from ..functions.forgot_password import forgot_password_dialog
from ..functions.snack_bar import snackbar
from ..service.firebase.firestore import system_data
from ..service.user.code_verification import verify_code_email


def connect_server_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    def back(e):
        from .start_menu import start_menu_page
        content_image.height = 370
        content_image.update()
        sleep(0.3)
        content_column.clean()
        page.update()
        start_menu_page(page, content_image, content_column)

    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def check_mail_id_entry(e):
        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                mail_id_entry.suffix_icon = None
                mail_id_entry.error_text = None
            else:
                mail_id_entry.error_text = "Enter the valid email address"
                mail_id_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
        else:
            mail_id_entry.error_text = "Enter your email address"
            mail_id_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        mail_id_entry.update()

    def check_password_input(e):
        login_waring_text.value = None
        login_waring_text.update()
        if len(password_entry.value) != 0:
            password_entry.error_text = ""
        else:
            password_entry.error_text = "Enter the password!"
        password_entry.update()

    def login_check_fun(e):
        check_mail_id_entry(e)
        check_password_input(e)

        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                if len(password_entry.value) != 0:
                    button_container.content = ft.ProgressRing()
                    content_column.disabled = True
                    button_container.opacity = 0.5
                    page.update()
                    from ..service.user.login_auth import check_login
                    val = check_login(page, mail_id_entry.value, password_entry.value)
                    sleep(1)
                    if val is True:
                        if verify_code_email(page, mail_id_entry.value, "Your One-Time Verification Code"):
                            system_data(page, True)
                            content_column.clean()
                            page.update()
                            from .all_done import all_done_page
                            all_done_page(page, content_column)
                            snackbar(page, "Successfully connected to the server")
                        else:
                            button_container.content = ft.Text("Connect Server")
                            button_container.opacity = 1
                            content_column.disabled = False
                            page.update()
                            login_waring_text.value = "  Invalid Email or Password!  "
                            password_entry.error_text = ""
                            mail_id_entry.focus()
                            page.update()
                            val = False
                    else:
                        button_container.content = ft.Text("Connect Server")
                        content_column.disabled = False
                        button_container.opacity = 1
                        page.update()
                        login_waring_text.value = "  Invalid Email or Password!  "
                        password_entry.error_text = ""
                        mail_id_entry.focus()
                        page.update()
                        val = False
                else:
                    password_entry.focus()
                    password_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            mail_id_entry.focus()
            mail_id_entry.update()

    # text
    login_waring_text = ft.Text(
        size=20,
        color=ft.colors.ERROR,
    )

    button_container = ft.ElevatedButton(
        text="Connect Server",
        height=50,
        width=340,
        on_click=login_check_fun,
    )

    # Input Fields
    mail_id_entry = ft.TextField(
        hint_text="Enter your email address",
        width=330,
        filled=False,
        prefix_icon=ft.icons.MAIL_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        on_change=check_mail_id_entry,
        on_submit=login_check_fun,
        autofocus=True,
        error_style=ft.TextStyle(font_family='Verdana'),
        text_style=ft.TextStyle(font_family='Verdana'),
    )

    password_entry = ft.TextField(
        hint_text="Enter your Password",
        width=330,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True,
        on_change=check_password_input,
        on_submit=login_check_fun,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Connect Server",
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
                        mail_id_entry,
                        password_entry,
                        button_container,
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=28,
                ),
                ft.Row(
                    [
                        login_waring_text
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            width=450,
            spacing=15,
            height=320,
            scroll=ft.ScrollMode.ADAPTIVE,
        ),
        ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        on_click=back,
                    ),
                    ft.TextButton(
                        text="Forgot Password?",
                        on_click=lambda e: forgot_password_dialog(page),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450,
            ),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
            bgcolor='#44CCCCCC',
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
        )
    ]

    page.update()

import flet as ft

from ..service.connection.firebase_connect import new_election, connect_server
from ..service.files.check_installation import new_start


def start_page(page: ft.Page):
    content_image = ft.Container(
        image_src='/images/content_image-1.png',
        image_fit=ft.ImageFit.FIT_HEIGHT,
        height=370,
        animate=ft.Animation(600, ft.AnimationCurve.DECELERATE)
    )

    content_column = ft.Column(
        width=450,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    bg_container = ft.Container(
        image_src="/images/Background-1.png",
        image_fit=ft.ImageFit.COVER,
        margin=-10,
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Container(
            width=450,
            height=550,
            border_radius=15,
            bgcolor='#44CCCCCC',
            blur=ft.Blur(30, 15, ft.BlurTileMode.CLAMP),
            content=ft.Column(
                [
                    content_image,
                    content_column,
                ],
                width=450,
                height=550,
            )
        )
    )

    settings_icon = ft.FloatingActionButton(
        icon=ft.icons.SETTINGS_ROUNDED,
        visible=False
    )

    if new_start is True:
        list_menu_button = [
            ft.ElevatedButton(
                text="New Election",
                height=50,
                width=250,
                on_click=lambda _: page.go("/store"),
                disabled=new_election
            ),
            ft.ElevatedButton(
                text="Connect Server",
                height=50,
                width=250,
                tooltip="Disabled",
                disabled=connect_server,
            ),
        ]
        settings_icon.visible = True
    else:
        list_menu_button = [
            ft.ElevatedButton(
                text="Sign In",
                height=50,
                width=250,
                # on_click=on_sign_in,
            ),
            ft.ElevatedButton(
                text="Vote",
                height=50,
                width=250,
            ),
        ]

    content_column.controls = [
        ft.Column(
            list_menu_button,
            width=250,
            spacing=20,
        )
    ]

    return [
        bg_container,
        settings_icon
    ]

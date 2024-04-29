import flet as ft

from app.functions.dialogs import loading_dialogs
from app.functions.theme import set_theme
from app.functions.window_actions import window_on_resize, window_at_start
from app.pages.start_menu import start_menu_page
from app.service.connection.check_files import check_connection_files
from app.service.scr.check_installation import installation_requirement


def main(page: ft.Page):
    # minimum width and height of the window.
    page.window_min_width = 800
    page.window_min_height = 600

    # Title
    page.title = "E-Voting"

    page.window_center()
    window_at_start(page)
    page.on_window_event = lambda e: window_on_resize(page)

    # theme
    set_theme(page)

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

    load = loading_dialogs(page, "Connecting...")
    page.add(bg_container)
    check_connection_files(page)
    start_menu_page(page, content_image, content_column)
    load.open = False
    page.update()


if __name__ == '__main__':
    installation_requirement()
    ft.app(
        target=main,
        assets_dir='assets',

    )

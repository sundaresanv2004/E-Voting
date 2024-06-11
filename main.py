import flet as ft

from app.functions.theme import set_theme
from app.functions.window_actions import window_at_start, window_on_resize
from app.pages.menubar import menubar_page
from app.pages.start_menu import start_menu_page
from app.service.files.check_installation import installation_requirement
from app.service.files.manage_files import create_election_settings
from app.service.firebase.check_files import check_connection_files
from app.service.user.login_auth import check_login


def main(page: ft.Page):
    # Title
    page.title = "E-Voting"

    # Minimum Height and Width of Window
    page.window_min_width = 900
    page.window_min_height = 700

    page.window_center()
    window_at_start(page)
    page.on_window_event = lambda e: window_on_resize(page)

    # Theme
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
            blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
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

    page.add(bg_container)
    check_connection_files(page)
    # create_election_settings()
    # check_login('admin@gmail.com', 'admin1234')
    # menubar_page(page)
    start_menu_page(page, content_image, content_column)


if __name__ == '__main__':
    installation_requirement()
    ft.app(
        target=main,
        assets_dir='assets',
    )

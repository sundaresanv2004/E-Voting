import flet as ft

from app.functions.theme import set_theme
from app.functions.window_actions import window_at_start, window_on_resize
from app.pages.start_meu import start_page
from app.service.files.check_installation import installation_requirement
from app.service.firebase.check_files import check_connection_files


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

    start_page(page)
    check_connection_files(page)


if __name__ == '__main__':
    installation_requirement()
    ft.app(
        target=main,
        assets_dir='assets',
    )


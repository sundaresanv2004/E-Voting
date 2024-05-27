import flet as ft

from app.service.files.check_installation import installation_requirement
from app.functions.window_actions import window_at_start, window_on_resize
from app.service.connection.check_files import check_connection_files
from app.functions.theme import set_theme
from app.pages._layout import layout


def main(page: ft.Page) -> None:
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
    page.update()

    # Layout
    layout(page)

    check_connection_files(page)
    page.go('/')


if __name__ == '__main__':
    installation_requirement()
    ft.app(
        target=main,
        assets_dir='assets'
    )

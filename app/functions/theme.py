import flet as ft


def set_theme(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.theme.Theme(color_scheme_seed='indigo')
    page.update()

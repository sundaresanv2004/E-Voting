import flet as ft


def snackbar(page: ft.Page, text: str) -> None:

    def close(e):
        page.snack_bar = snack_bar
        page.snack_bar.open = False
        page.update()

    # SnackBar data
    snack_bar = ft.SnackBar(
        content=ft.Text(f"{text}", font_family='Verdana',),
        action="Close",
        on_action=close,
        action_color=ft.colors.BLUE,
    )

    # open snackBar
    page.snack_bar = snack_bar
    page.snack_bar.open = True
    page.update()

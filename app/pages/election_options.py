import flet as ft
import pandas as pd

from ..functions.dialogs import message_dialogs, loading_dialogs
from ..service.files.local_files_scr import messages


def category_order(page: ft.Page):
    from ..functions.order_category import order_category_option

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_next1(e):
        message_alertdialog.open = False
        page.update()

        order_category_option(page)

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Choose Order", font_family='Verdana')
        message_alertdialog.content = ft.Text(value=messages['final_list'], font_family='Verdana')
        message_alertdialog.actions = [
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
        ]

        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Warning!",
            font_family='Verdana',
            weight=ft.FontWeight.W_500,
            color=ft.colors.RED_500,
        ),
        content=ft.Text(
            value=messages['make_sure'],
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Continue",
                on_click=on_next,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()

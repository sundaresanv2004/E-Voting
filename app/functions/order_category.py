from time import sleep
import flet as ft
import pandas as pd

from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..functions.dialogs import loading_dialogs
from ..service.firebase.firestore import update_election_data

list_category = []


class CategoryList(ft.UserControl):

    def __init__(self, val):
        super().__init__()
        self.text = ft.Text(size=20, value=None, font_family='Verdana')
        self.val = val

    def on_click_cat(self, e):
        global list_category
        if e in list_category:
            list_category.remove(e)
            self.text.value = None
        else:
            list_category.append(e)
            self.text.value = list_category.index(e) + 1
        self.text.update()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Checkbox(
                        label=self.val,
                        data=self.val,
                        on_change=lambda e: self.on_click_cat(e.control.data)),
                    ft.Row(expand=True),
                    self.text,
                    ft.Row(width=2),
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            width=450,
            height=50,
            border_radius=5,
            padding=10,
        )


def order_category_option(page: ft.Page):
    candidate_data_df = pd.read_csv(path + file_path['category_data'])
    df1 = candidate_data_df['category_name']

    def on_reset(e):
        global list_category
        message_alertdialog.open = False
        page.update()
        sleep(0.2)
        list_category = []
        order_category_option(page)

    temp_category_data = []
    if candidate_data_df.empty is False:
        for i in df1:
            temp_category_data.append(CategoryList(i))
    else:
        temp_category_data.append(
            ft.Row(
                [
                    ft.Text(
                        value="No Records",
                        size=25,
                        font_family='Verdana',
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=350,
                height=200,
            )
        )

    def on_ok(e):
        global list_category
        message_alertdialog.open = False
        page.update()
        list_category = []

    def on_save(e):
        message_alertdialog.open = False
        page.update()
        if len(list_category) > 0:
            dig = loading_dialogs(page, "Updating...")
            update_election_data(list_category)
            from ..pages.election_settings import update_election_set
            dig.open = False
            page.update()
            update_election_set()

    save_button = ft.TextButton(
        text="Save",
        on_click=on_save,
    )

    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Chose Category Order", font_family='Verdana', ),
        content=ft.Container(
            content=ft.Column(
                controls=temp_category_data,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            height=450,
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Reset",
                on_click=on_reset,
            ),
            save_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()

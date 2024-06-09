import flet as ft
import pandas as pd

from ..functions.dialogs import message_dialogs
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..service.firebase.realtime_db import get_image_url

column_1 = ft.Column()
main_column1 = None
search_entry = ft.TextField(
    hint_text="Search",
    hint_style=ft.TextStyle(color='f2f9f9', font_family='Verdana'),
    width=450,
    filled=False,
    border=ft.InputBorder.OUTLINE,
    height=50,
    disabled=True,
    border_radius=55,
    # focused_border_color='#f2f9f9',
    # border_color='#ddeff0',
    prefix_style=ft.TextStyle(color=ft.colors.WHITE),
    text_style=ft.TextStyle(font_family='Verdana'),
    prefix_icon=ft.icons.SEARCH_ROUNDED,
)


def candidate_home_page(page: ft.Page, main_column: ft.Column):
    global search_entry, column_1, main_column1

    main_column1 = main_column

    def search(e):
        search_display_candidate(page)

    search_entry.on_change = search
    search_entry.value = None

    main_column.controls = [
        ft.Container(
            margin=ft.margin.only(left=5, right=5),
            content=search_entry,
            alignment=ft.alignment.center,
        ),
        ft.Container(
            padding=5,
            content=column_1,
            expand=True,
        ),
    ]
    page.update()
    page.splash = None
    display_candidate(page)


def search_display_candidate(page: ft.Page):
    # file
    candidate_data_df = pd.read_json(path + file_path["candidate_data"], orient='table')
    name_enc = candidate_data_df['name'].to_list()
    cat_enc = list(candidate_data_df['category'].unique())

    row_can_data_list: list = []
    data_in: list = []
    if len(search_entry.value) != 0:
        for i in name_enc:
            if search_entry.value.lower() in i.lower():
                if name_enc.index(i) not in data_in:
                    row_can_data_list.append(ViewStaffRecord(page, main_column1, name_enc.index(i)))
                    data_in.append(name_enc.index(i))

        for j in cat_enc:
            if search_entry.value.lower() in j.lower():
                for k in list(candidate_data_df[candidate_data_df.category == j].index.values):
                    if k not in data_in:
                        row_can_data_list.append(ViewStaffRecord(page, main_column1, k))
                        data_in.append(k)

        column_1.controls = row_can_data_list
        page.update()
    else:
        display_candidate(page)


def display_candidate(page):
    global column_1
    # file
    candidate_data_df = pd.read_json(path + file_path["candidate_data"], orient='table')

    row_can_data_list = []

    if candidate_data_df.empty is True:
        row_can_data_list.append(
            ft.Row(
                [
                    ft.Text(
                        value="No record found",
                        size=25,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        search_entry.disabled = True
        column_1.alignment = ft.MainAxisAlignment.CENTER
        page.update()
    else:
        for i in range(len(candidate_data_df.index)):
            row_can_data_list.append(ViewStaffRecord(page, main_column1, i))
        column_1.expand = True
        search_entry.disabled = False
        column_1.scroll = ft.ScrollMode.ADAPTIVE

    column_1.controls = row_can_data_list
    page.update()


class ViewStaffRecord(ft.UserControl):

    def __init__(self, page, column, index_val):
        super().__init__()
        self.page = page
        self.index_val = index_val
        self.column = column
        self.candidate_data_df = pd.read_json(path + file_path["candidate_data"], orient='table')

    def edit(self, e):
        from .candidate_edit import candidate_edit_page
        candidate_edit_page(self.page, self.index_val, False)

    def profile(self, e):
        from .candidate_profile import candidate_profile_page
        candidate_profile_page(self.page, self.index_val)

    def delete(self, e):
        from .candidate_delete import delete_candidate_dialogs
        delete_candidate_dialogs(self.page, self.index_val, False)

    def build(self):
        self_icon = ft.CircleAvatar(
            content=ft.Icon(
                name=ft.icons.ACCOUNT_CIRCLE,
            ),
        )

        single_box_row = ft.Card(
            ft.Container(
                ft.ListTile(
                    leading=self_icon,
                    title=ft.Text(
                        value=f"{self.candidate_data_df.at[self.index_val, 'name']}",
                        font_family='Verdana',
                    ),
                    subtitle=ft.Text(
                        value=f"{self.candidate_data_df.at[self.index_val, 'category']}",
                        font_family='Verdana',
                    ),
                    trailing=ft.PopupMenuButton(
                        icon=ft.icons.MORE_VERT_ROUNDED,
                        items=[
                            ft.PopupMenuItem(
                                text="Edit",
                                icon=ft.icons.EDIT_ROUNDED,
                                on_click=self.edit
                            ),
                            ft.PopupMenuItem(
                                text="Delete",
                                icon=ft.icons.DELETE_ROUNDED,
                                on_click=self.delete
                            ),
                        ],
                    ),
                    on_click=self.profile,
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC')
        )

        return single_box_row

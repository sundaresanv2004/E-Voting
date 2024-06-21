from time import sleep
import flet as ft
import pandas as pd

from .vote_options import vote_exit, vote_done
from ..functions.dialogs import error_message_dialogs
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path

category_text = ft.Text(
    size=35,
    font_family='Verdana',
    color='#172554',
    weight=ft.FontWeight.W_800,
    # bgcolor=ft.colors.YELLOW,
)
page_text = ft.Text(
    size=25,
    font_family='Verdana',
    color='#172554',
    weight=ft.FontWeight.W_700,
)
curr_data = 0
temp_list = []
image_not_found = ft.Column(
    [
        ft.Icon(
            name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
            size=40,
        ),
        ft.Text(
            value="Image not found",
            font_family='Verdana',
        ),
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    alignment=ft.MainAxisAlignment.CENTER,
    height=250,
    width=200,
)


def vote_start_page(page: ft.Page, election_path):
    main_column = ft.Column(expand=True)

    appbar = ft.Container(
        border_radius=9,
        bgcolor=ft.colors.with_opacity(0.5, '#FFFFFF'),
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        margin=ft.margin.only(left=5, top=5, right=5),

    )
    container = ft.Container(
        image_fit=ft.ImageFit.COVER,
        image_src="/images/background-4.png",
        margin=-10,
        expand=True,
        content=ft.Column(
            [
                appbar,
                main_column,
            ],
        )
    )

    page.add(container)
    page.update()
    vote_content_page(page, appbar, main_column, election_path)


def vote_content_page(page: ft.Page, appbar: ft.Container, main_column: ft.Column, election_path: str):
    def on_vote_click(e):
        appbar.content = None
        main_column.clean()
        appbar.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Row(width=5),
                        category_text
                    ],
                    expand=True,
                ),
                ft.VerticalDivider(color=ft.colors.PRIMARY, thickness=2),
                ft.Row(
                    [
                        page_text
                    ]
                ),
                ft.Row(width=5)
            ],
            height=60,
        )
        page.update()
        user_vote_start(page, appbar, main_column, election_path)

    app_data_df = pd.read_json(path + file_path['app_data'], orient='table')
    election_log = pd.read_json(election_path + r'/election_datalog.json', orient='table')
    df1 = election_log[election_log.active_status == True]
    index_val = df1.index.values[0]
    vote_data_path = election_path + rf"/{election_log.at[index_val, 'file_name']}"

    try:
        election_data3 = pd.read_csv(vote_data_path)
    except pd.errors.ParserError as e:
        error_message_dialogs(page, str(e), election_path)
    except pd.errors.EmptyDataError as e:
        error_message_dialogs(page, str(e), election_path)
    except Exception as e:
        error_message_dialogs(page, str(e), election_path)

    appbar.content = ft.Row(
        [
            ft.Row(
                [
                    ft.Text(
                        value=app_data_df.at[0, 'institution_name'],
                        size=40,
                        font_family='Verdana',
                        color='#172554',
                        weight=ft.FontWeight.W_800,
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.VerticalDivider(color=ft.colors.PRIMARY, thickness=2),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.LOGOUT_ROUNDED,
                        tooltip="Logout",
                        icon_size=30,
                        icon_color='#172554',
                        on_click=lambda _: vote_exit(page, election_path, False),
                    )
                ]
            ),
            ft.Row(width=5)
        ],
        height=60,
    )

    try:
        len_vote = len(election_data3)
    except Exception as e:
        len_vote = 0

    main_column.controls = [
        ft.Column(
            [
                ft.Container(
                    width=550,
                    height=300,
                    border_radius=15,
                    bgcolor='#44CCCCCC',
                    blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
                    animate=ft.Animation(700, ft.AnimationCurve.DECELERATE),
                    content=ft.Column(
                        [
                            ft.Text(
                                value=app_data_df.at[0, 'election_name'],
                                size=30,
                                font_family='Verdana',
                                color='#172554',
                                weight=ft.FontWeight.W_800,
                            ),
                            ft.Text(
                                value=f"Vote No: {len_vote}",
                                size=30,
                                font_family='Verdana',
                                color='#172554',
                                weight=ft.FontWeight.W_800,
                            ),
                            ft.Row(height=10),
                            ft.FloatingActionButton(

                                text="Start Voting",
                                width=250,
                                height=50,
                                on_click=on_vote_click,

                            ),
                        ],
                        spacing=20,
                        width=300,
                        height=260,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                ft.Row(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
    ]

    page.update()


def user_vote_start(page: ft.Page, appbar: ft.Container, main_column: ft.Column, election_path):
    global category_text, page_text, curr_data

    final_category_data1 = pd.read_csv(election_path + r'/category_data.csv')
    candidate_df = pd.read_json(election_path + r'/candidate_data.json', orient='table')

    category_dict = {}
    for i in range(len(final_category_data1)):
        category_dict[final_category_data1.at[i, 'category_id']] = final_category_data1.at[i, 'category_name']

    category_list = list(final_category_data1['category_id'])

    category_text.value = f" Category: {category_dict[category_list[curr_data]]}  "
    page_text.value = f"Page: {curr_data + 1}of{len(category_list)}"
    page_text.update()
    df1 = candidate_df[candidate_df.category == category_list[curr_data]].values
    content_list = []
    for i in range(len(df1)):
        content_list.append(VoteUser(page, df1[i][0], appbar, main_column, election_path))

    main_column.controls = [
        ft.Column(
            [

                ft.Column(height=10),
                ft.Container(
                    content=ft.Row(
                        controls=content_list,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        spacing=30,
                    ),
                    margin=ft.margin.only(left=5, right=5),
                    alignment=ft.alignment.top_center,
                ),
                ft.Column(height=10),
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    page.update()


class VoteUser(ft.UserControl):
    def __init__(self, page: ft.Page, can_id, appbar: ft.Container, main_column: ft.Column, election_path):
        super().__init__()
        self.page = page
        self.can_id = can_id
        self.appbar = appbar
        self.main_column = main_column
        self.candidate_df = pd.read_json(election_path + r'/candidate_data.json', orient='table')
        self.candidate_image_destination = election_path
        final_category_data2 = pd.read_csv(election_path + r'/category_data.csv')
        self.category_list1 = list(final_category_data2['category_name'])
        self.election_path = election_path

    def on_user_click(self, e):
        global temp_list, curr_data
        temp_list.append(e)
        if len(temp_list) != len(self.category_list1):
            self.main_column.clean()
            curr_data += 1
            sleep(0.1)
            self.main_column.clean()
            user_vote_start(self.page, self.appbar, self.main_column, self.election_path)
        else:
            try:
                election_log = pd.read_json(self.election_path + r'/election_datalog.json', orient='table')
                vote_data_path = self.election_path + election_log.at[0, 'file_name']
                election_data3 = pd.read_csv(vote_data_path)
                election_data3.loc['a'] = temp_list
                election_data3.to_csv(vote_data_path, index=False)
            except pd.errors.ParserError as e:
                error_message_dialogs(self.page, str(e), self.election_path)
            except pd.errors.EmptyDataError as e:
                error_message_dialogs(self.page, str(e), self.election_path)
            except Exception as e:
                error_message_dialogs(self.page, str(e), self.election_path)
            curr_data = 0
            temp_list = []
            self.main_column.clean()
            sleep(0.1)
            vote_done(self.page, self.appbar, self.main_column, self.election_path)

    def build(self):
        can_data = self.candidate_df[self.candidate_df.candidate_id == self.can_id].index.values[0]

        img_container = ft.Container(
            width=240,
            height=290,
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            image_fit=ft.ImageFit.COVER,
        )

        img_container.image_src = self.candidate_image_destination + rf"/{ self.candidate_df.at[can_data, 'image']}"

        def on_hover_animate(e):
            e.control.scale = 1.1 if e.data == "true" else 1
            e.control.update()

        main_con = ft.Container(
            width=240,
            height=360,
            scale=1,
            bgcolor=ft.colors.with_opacity(0.3, ft.colors.WHITE),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=10,
            content=ft.Column(
                [
                    img_container,
                    ft.Row(
                        [
                            ft.Text(
                                value=self.candidate_df.at[can_data, 'name'],
                                size=20,
                                weight=ft.FontWeight.W_700,
                            )
                        ],
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                width=240,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_hover=on_hover_animate,
            data=self.can_id,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            on_click=lambda e: self.on_user_click(e.control.data),
        )

        return main_con

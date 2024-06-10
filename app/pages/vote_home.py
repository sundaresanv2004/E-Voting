from time import sleep
import flet as ft
import pandas as pd

import Main.service.scr.election_scr as ee
from Main.functions.error_message import error_message_dialogs
from Main.functions.troubleshooting import election_data_missing
from Main.pages.vote_options import vote_exit, vote_done
from Main.service.scr.check_installation import path
from Main.service.scr.loc_file_scr import file_data, file_path

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


def vote_start_page(page: ft.Page):
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
    vote_content_page(page, appbar, main_column)


election_data_loc = rf'/{file_data["vote_data"]}/{file_data["election_data"]}'


def vote_content_page(page: ft.Page, appbar: ft.Container, main_column: ft.Column):
    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

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
        user_vote_start(page, appbar, main_column)

    app_data_df = pd.read_json(path + file_path['app_data'], orient='table')
    election_data2 = None
    try:
        election_data2 = pd.read_json(ee.current_election_path + election_data_loc, orient='table')
    except pd.errors.ParserError as e:
        error_message_dialogs(page, str(e))
    except pd.errors.EmptyDataError as e:
        error_message_dialogs(page, str(e))
    except Exception as e:
        error_message_dialogs(page, str(e))
    ele_ser12 = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')

    appbar.content = ft.Row(
        [
            ft.Row(
                [
                    ft.Text(
                        value=app_data_df[app_data_df.topic == 'institution_name'].values[0][1],
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
                        on_click=lambda _: vote_exit(page),
                    )
                ]
            ),
            ft.Row(width=5)
        ],
        height=60,
    )

    if len(election_data2) == 1:
        ele_ser12.loc['completed'] = True
        ele_ser12.to_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table', index=True)

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
                                value=ele_ser12.loc['election-name'].values[0],
                                size=30,
                                font_family='Verdana',
                                color='#172554',
                                weight=ft.FontWeight.W_800,
                            ),
                            ft.Text(
                                value=f"Vote No: {len(election_data2) + 1}",
                                size=30,
                                font_family='Verdana',
                                color='#172554',
                                weight=ft.FontWeight.W_800,
                            ),
                            ft.Row(height=10),
                            ft.Container(
                                width=250,
                                height=50,
                                border_radius=10,
                                bgcolor="#0ea5e9",
                                alignment=ft.alignment.center,
                                on_hover=on_hover_color,
                                content=ft.Text(
                                    value="Vote",
                                    size=20,
                                    color=ft.colors.WHITE,
                                    font_family='Verdana',
                                    weight=ft.FontWeight.W_500,
                                ),
                                on_click=on_vote_click,
                                animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE)
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


def user_vote_start(page: ft.Page, appbar: ft.Container, main_column: ft.Column):
    global category_text, page_text, curr_data
    final_category_data1 = pd.read_csv(
        ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_category"]}')
    candidate_df = pd.read_json(
        ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_nomination"]}',
        orient='table')
    category_list = list(final_category_data1['category'])

    category_text.value = f" Category: {category_list[curr_data]}  "
    page_text.value = f"Page: {curr_data + 1}of{len(category_list)}"
    page_text.update()
    df1 = candidate_df[candidate_df.category == category_list[curr_data]].values
    content_list = []
    for i in range(len(df1)):
        content_list.append(VoteUser(page, df1[i][0], appbar, main_column))

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
    def __init__(self, page: ft.Page, can_id, appbar: ft.Container, main_column: ft.Column):
        super().__init__()
        self.page = page
        self.can_id = can_id
        self.appbar = appbar
        self.main_column = main_column
        self.candidate_df = pd.read_json(
            ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_nomination"]}',
            orient='table')
        self.candidate_image_destination = ee.current_election_path + r'/images'
        final_category_data2 = pd.read_csv(
            ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_category"]}')
        self.category_list1 = list(final_category_data2['category'])

    def on_user_click(self, e):
        global temp_list, curr_data
        temp_list.append(e)
        if len(temp_list) != len(self.category_list1):
            self.main_column.clean()
            curr_data += 1
            sleep(0.1)
            self.main_column.clean()
            user_vote_start(self.page, self.appbar, self.main_column)
        else:
            try:
                election_data3 = pd.read_json(ee.current_election_path + election_data_loc, orient='table')
                election_data3.loc['a'] = temp_list
                election_data3.to_json(ee.current_election_path + election_data_loc, orient='table', index=False)
            except pd.errors.ParserError as e:
                error_message_dialogs(self.page, str(e))
            except pd.errors.EmptyDataError as e:
                error_message_dialogs(self.page, str(e))
            except Exception as e:
                error_message_dialogs(self.page, str(e))
            curr_data = 0
            temp_list = []
            self.main_column.clean()
            sleep(0.1)
            vote_done(self.page, self.appbar, self.main_column)

    def build(self):
        can_data = self.candidate_df[self.candidate_df.id == self.can_id].values[0]

        img_container = ft.Container(
            width=240,
            height=290,
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            image_fit=ft.ImageFit.COVER,
        )
        if can_data[5] is False:
            img_container.content = image_not_found
        else:
            img_container.image_src = self.candidate_image_destination + rf'/{can_data[5]}'

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
                                value=can_data[1],
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

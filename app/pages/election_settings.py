import flet as ft
import pandas as pd

from .category import category_dialogs
from .election_options import category_order, vote_options, download_nomination, view_results, download_result
from .summary_view import summary_view_page
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..service.firebase.realtime_db import read_vote_data

ele_option_data_update = None


class ElectionSettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.vote_button = None
        self.page = page
        self.final_nomination_list = None
        self.download_result = None
        self.download_nomination = None
        self.view_result = None
        self.summary_view_result = None
        self.forgot_passcode = None
        self.vote_switch = ft.Switch(on_change=lambda _: vote_options(self.vote_switch.value))
        self.ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')
        self.tot_no_vote = ft.Text(value="Total no.of votes: 0", font_family='Verdana')
        self.next_icon = ft.Icon(
            name=ft.icons.NAVIGATE_NEXT_ROUNDED,
            size=25,
        )

    def vote_option(self):
        self.vote_button = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    font_family='Verdana',
                    value=f"Vote Option",
                ),
                trailing=self.vote_switch,
            ),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            padding=ft.padding.symmetric(vertical=3.5),
            border_radius=10,
        )

        return ft.Card(
            self.vote_button,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def final_nomination_list_option(self):
        self.final_nomination_list = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Generate Nomination List",
                    font_family='Verdana',
                ),
                trailing=self.next_icon,
                on_click=lambda _: category_order(self.page),
            ),
            padding=ft.padding.symmetric(vertical=3.5),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=10,
            disabled=True,
        )

        return ft.Card(
            content=self.final_nomination_list,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def view_result_option(self):
        self.view_result = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    font_family='Verdana',
                    value=f"View result",
                ),
                subtitle=self.tot_no_vote,
                trailing=self.next_icon,
                on_click=lambda _: view_results(self.page, read_vote_data(self.page)),
            ),
            border_radius=10,
            padding=ft.padding.symmetric(vertical=3.5),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
        )

        return ft.Card(
            self.view_result,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def summary_view_result_option(self):
        self.summary_view_result = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Summary view result",
                    font_family='Verdana',
                ),
                trailing=self.next_icon,
                on_click=lambda _: summary_view_page(self.page, read_vote_data(self.page)),
            ),
            border_radius=10,
            padding=ft.padding.symmetric(vertical=3.5),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
        )

        return ft.Card(
            self.summary_view_result,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def download_result_option(self):
        self.download_result = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    font_family='Verdana',
                    value=f"Download result",
                ),
                trailing=self.next_icon,
                on_click=lambda _: download_result(self.page, read_vote_data(self.page)),
            ),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=10,
            padding=ft.padding.symmetric(vertical=3.5),
        )

        return ft.Card(
            content=self.download_result,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def download_nomination_option(self):
        self.download_nomination = ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Download Nomination List",
                    font_family='Verdana',
                ),
                on_click=lambda _: download_nomination(self.page),
                trailing=self.next_icon,
            ),
            padding=ft.padding.symmetric(vertical=3.5),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            border_radius=10,
        )

        return ft.Card(
            self.download_nomination,
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

    def update_in_data(self):
        candidate_df = pd.read_json(path + file_path["candidate_data"], orient='table')
        self.ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')

        if candidate_df.empty is False:
            if not self.ele_ser_1.at[0, 'result']:
                self.final_nomination_list.disabled = False

        if self.ele_ser_1.at[0, 'final_nomination']:
            self.vote_button.disabled = False
        else:
            self.vote_button.disabled = True

        if self.ele_ser_1.at[0, 'vote_option']:
            self.vote_switch.value = True
        else:
            self.vote_switch.value = False

        if self.ele_ser_1.at[0, 'final_nomination']:
            self.download_nomination.disabled = False
        else:
            self.download_nomination.disabled = True

        if self.ele_ser_1.at[0, 'result']:
            election_df = read_vote_data(self.page)
            self.tot_no_vote.value = f"Total no.of votes: {sum(list(election_df.loc[0].values))}"
            self.view_result.disabled = False
            self.summary_view_result.disabled = False
            self.download_result.disabled = False
        else:
            self.view_result.disabled = True
            self.summary_view_result.disabled = True
            self.download_result.disabled = True

        self.page.update()


def election_settings_page(page: ft.Page, main_column: ft.Column):
    global ele_option_data_update
    option_menu_ele = ElectionSettingsMenu(page)
    ele_option_data_update = option_menu_ele

    category_option = ft.Card(
        ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Manage Category",
                    font_family='Verdana',
                ),
                trailing=ft.Icon(
                    name=ft.icons.NAVIGATE_NEXT_ROUNDED,
                    size=25,
                ),
                on_click=lambda _: category_dialogs(page),
            ),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            padding=ft.padding.symmetric(vertical=3.5),
            border_radius=10,
        ),
        elevation=0,
        color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
    )

    main_column.controls = [
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(height=3),
                    category_option,
                    # option_menu_ele.lock_election_option(),
                    option_menu_ele.final_nomination_list_option(),
                    option_menu_ele.download_nomination_option(),
                    option_menu_ele.vote_option(),
                    # option_menu_ele.generate_result_option(),
                    option_menu_ele.view_result_option(),
                    option_menu_ele.summary_view_result_option(),
                    option_menu_ele.download_result_option(),
                    # option_menu_ele.forgot_passcode_option(),
                    # option_menu_ele.help_option(),
                ],
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            margin=ft.margin.only(left=5, right=5),
            expand=True,
        )
    ]

    page.splash = None
    page.update()
    option_menu_ele.update_in_data()


def update_election_set():
    ele_option_data_update.update_in_data()

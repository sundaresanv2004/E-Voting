import flet as ft
import pandas as pd

import app.service.user.login_auth as cc
from .candidate_add import candidate_add_page
from ..service.files.check_installation import path
from ..service.files.local_files_scr import file_path
from ..service.files.manage_files import create_category, create_candidate, remove_files, create_election_settings

old_data = None


def menubar_page(page: ft.Page) -> None:
    create_election_settings()

    def add_candidate_page_fun(e):
        candidate_add_page(page)

    main_column = ft.Column(expand=True)

    add_candidate_button = ft.FloatingActionButton(
        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
        tooltip="Add new Candidate",
        on_click=add_candidate_page_fun,
    )

    def on_option_click(e):
        ele_ser_1 = pd.read_json(path + file_path['election_settings'], orient='table')
        page.splash = ft.ProgressBar()
        global old_data

        if e != 5:
            main_column.clean()
            page.update()
            if old_data == 0:
                container.image_src = "/images/background-3.png"
                home.icon = None
            elif old_data == 1:
                if not ele_ser_1.at[0, 'final_nomination']:
                    try:
                        page.remove(add_candidate_button)
                    except ValueError:
                        pass
                candidate.icon = None
            elif old_data == 2:
                election.icon = None
            elif old_data == 3:
                settings.icon = None
        old_data = e
        page.update()

        if e == 0:
            container.image_src = "/images/background-2.png"
            home.icon = ft.icons.HOME_ROUNDED
            create_candidate()
            create_category(page)
            from .home import home_page
            home_page(page, main_column)
        elif e == 1:
            candidate.icon = ft.icons.SUPERVISED_USER_CIRCLE
            from .candidate_home import candidate_home_page
            candidate_home_page(page, main_column)
            if not ele_ser_1.at[0, 'final_nomination']:
                page.add(add_candidate_button)
        elif e == 2:
            election.icon = ft.icons.HOW_TO_VOTE
            from .election_settings import election_settings_page
            election_settings_page(page, main_column)
        elif e == 3:
            settings.icon = ft.icons.SETTINGS
            from .settings import settings_page
            settings_page(page, main_column)
        elif e == 4:
            # dia = loading_dialogs(page, "Logging out...")
            old_data = None
            page.update()
            from main import main
            remove_files()
            page.clean()
            page.splash = None
            # dia.open = False
            page.update()
            main(page)

        page.update()

    home = ft.TextButton(
        text='Home',
        data=0,
        on_click=lambda e: on_option_click(e.control.data)
    )

    candidate = ft.TextButton(
        text="Candidate",
        data=1,
        on_click=lambda e: on_option_click(e.control.data)
    )

    election = ft.TextButton(
        text="Election",
        data=2,
        on_click=lambda e: on_option_click(e.control.data)
    )

    settings = ft.TextButton(
        text="Settings",
        data=3,
        on_click=lambda e: on_option_click(e.control.data)
    )

    log_out = ft.TextButton(
        icon=ft.icons.LOGOUT_OUTLINED,
        text="Logout",
        data=4,
        on_click=lambda e: on_option_click(e.control.data)
    )

    appbar = ft.Container(
        border_radius=9,
        bgcolor=ft.colors.with_opacity(0.5, '#FFFFFF'),
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Text(
                                            value="sfddsf",# cc.auth_data['displayName'][0].upper(),
                                            size=22,
                                        ),
                                    ),
                                    ft.Text(
                                        value=cc.auth_data['displayName'].capitalize(),
                                        weight=ft.FontWeight.BOLD,
                                        size=15,
                                    )
                                ]
                            ),
                            margin=5,
                            padding=ft.padding.only(10, 0, 0, 0)
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                ft.Row(
                    [
                        home,
                        candidate,
                        election,
                        settings,
                    ]
                ),
                ft.VerticalDivider(color=ft.colors.PRIMARY, thickness=2),
                ft.Container(
                    log_out,
                    padding=ft.padding.only(0, 0, 10, 0)
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            height=50
        ),
        margin=ft.margin.only(left=5, top=5, right=5),

    )

    container = ft.Container(
        image_fit=ft.ImageFit.COVER,
        image_src="/images/background-2.png",
        margin=-10,
        expand=True,
        content=ft.Column(
            [
                appbar,
                main_column
            ],
        )
    )

    page.add(container)
    page.update()
    on_option_click(0)


def update():
    global old_data
    old_data = None

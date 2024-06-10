import flet as ft
import pandas as pd

from .category import category_dialogs
from .election_options import category_order, forgot_code, generate_result, result_view_dialogs
from .settings_options import help_dialogs

ele_option_data_update = None


def election_settings_page(page: ft.Page, main_column: ft.Column):
    global ele_option_data_update
    # option_menu_ele = ElectionSettingsMenu(page)
    # ele_option_data_update = option_menu_ele

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
                    # option_menu_ele.final_nomination_list_option(),
                    # option_menu_ele.download_nomination_option(),
                    # option_menu_ele.vote_option(),
                    # option_menu_ele.generate_result_option(),
                    # option_menu_ele.view_result_option(),
                    # option_menu_ele.summary_view_result_option(),
                    # option_menu_ele.download_result_option(),
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
    # option_menu_ele.update_in_data()


def update_election_set():
    ele_option_data_update.update_in_data()

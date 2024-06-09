import os
from time import sleep
import flet as ft
import pandas as pd

from ..functions.dialogs import message_dialogs, loading_dialogs


def passcode_election(page: ft.Page, switch_data: ft.Switch):
    from ..service.scr.loc_file_scr import messages
    from ..service.files.vote_settings_write import first_lock

    # Functions
    def on_ok(e):
        switch_data.value = False
        message_alertdialog.open = False
        page.update()

    def save_on(e):
        if len(entry1.value) == 5:
            entry1.error_text = None
            message_alertdialog.open = False
            page.update()
            first_lock(entry1.value)
        else:
            entry1.error_text = "Enter the Code"
            entry1.focus()
            entry1.update()

    entry1 = ft.TextField(
        hint_text="Enter the Code",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        max_length=5,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        on_submit=save_on,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
    )

    def on_next1(e):
        message_alertdialog.title = ft.Text(value="2-Step Verification", font_family='Verdana')
        message_alertdialog.content = ft.Column(
            [
                entry1
            ],
            height=70,
            width=350,
        )

        message_alertdialog.actions = [
            ft.TextButton(
                text="Save",
                on_click=save_on,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]
        page.update()

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Make Sure?", font_family='Verdana')
        message_alertdialog.content = ft.Column(
            [
                ft.Text(
                    value=messages["code_text2"],
                    size=15,
                    font_family='Verdana'),
            ],
            height=100,
        )

        message_alertdialog.actions = [
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]
        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"2-Step Verification",
            font_family='Verdana',
        ),
        content=ft.Column(
            [
                ft.Text(
                    value=messages["code_text1"],
                    size=15,
                    font_family='Verdana',
                ),
            ],
            height=100,
        ),
        actions=[
            ft.TextButton(
                text="Next",
                on_click=on_next,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()


def lock_unlock_data(page: ft.Page, switch_data: ft.Switch):
    from ..service.files.vote_settings_write import lock_and_unlock

    # Functions
    def on_ok(e):
        if switch_data.value:
            switch_data.value = False
        else:
            switch_data.value = True
        message_alertdialog.open = False
        page.update()

    def save_on(e):
        if len(entry1.value) != 0:
            if verification_page(entry1.value):
                entry1.error_text = None
                message_alertdialog.open = False
                page.update()
                lock_and_unlock()
            else:
                entry1.error_text = "Invalid Code"
                entry1.focus()
                entry1.update()
        else:
            entry1.error_text = "Enter the Code"
            entry1.focus()
            entry1.update()

    entry1 = ft.TextField(
        hint_text="Enter the Code",
        border=ft.InputBorder.OUTLINE,
        width=350,
        border_radius=9,
        password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
        on_submit=save_on,
    )

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"2-Step Verification",
            font_family='Verdana',
        ),
        content=ft.Column(
            [
                entry1
            ],
            height=70,
            width=350,
        ),
        actions=[
            ft.TextButton(
                text="Submit",
                on_click=save_on,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()


def category_order(page: ft.Page):
    from ..functions.order_category import order_category_option

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_next1(e):
        message_alertdialog.open = False
        page.update()
        election_data_loc = rf'/{file_data["vote_data"]}/{file_data["election_data"]}'
        if os.path.exists(ee.current_election_path + election_data_loc):
            os.remove(ee.current_election_path + election_data_loc)
        sleep(0.1)
        order_category_option(page)

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Read", font_family='Verdana')
        message_alertdialog.content = ft.Text(value=messages['final_list'], font_family='Verdana')
        message_alertdialog.actions = [
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]

        page.update()

    ele_ser = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')
    if ele_ser.loc['final_nomination'].values[0]:
        message_alertdialog.title = ft.Text(value="Make Sure?", font_family='Verdana')
        message_alertdialog.content = ft.Text(value=messages['re_final_list'], font_family='Verdana')
        message_alertdialog.actions = [
            ft.TextButton(
                text="Yes",
                on_click=on_next,
            ),
            ft.TextButton(
                text="No",
                on_click=on_ok,
            ),
        ]
    else:
        on_next('e')

    if ele_ser.loc["completed"].values[0]:
        message_dialogs(page, "Option is locked")
    else:
        page.dialog = message_alertdialog
        message_alertdialog.open = True
        page.update()


def forgot_code(page: ft.Page):
    from ..service.enc.code_generator import code_checker, code_generate
    import Main.service.user.login_enc as cc

    def on_close(e):
        forgot_code_dialog1.open = False
        page.update()

    def on_ok(e):
        if len(code_entry.value) != 0:
            if code_checker(code_entry.value):
                code_entry.error_text = None
                code_entry.update()
                forgot_code_dialog1.title = ft.Text("Forgot code?", font_family='Verdana')
                ele_ser10 = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}",
                                         orient='table')
                forgot_code_dialog1.content = ft.Row(
                    [
                        ft.Text(
                            value=f"Code: {decrypter(ele_ser10.loc['code'].values[0])}",
                            font_family='Verdana',
                        )
                    ]
                )
                forgot_code_dialog1.actions = [
                    ft.TextButton(
                        text="Close",
                        on_click=on_close,
                    ),
                ]
                page.update()
            else:
                code_entry.error_text = "Invalid Code!"
                code_entry.focus()
        else:
            code_entry.error_text = "Enter the code."
            code_entry.focus()
        code_entry.update()

    code_entry = ft.TextField(
        hint_text="Enter the one time code.",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
        prefix_icon=ft.icons.PASSWORD_ROUNDED,
        on_submit=on_ok,
    )

    if cc.teme_data[0] == 1:
        code_generate(page)
        forgot_code_dialog1 = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="2-Step verification",
                font_family='Verdana',
            ),
            content=ft.Row(
                [
                    code_entry
                ],
                width=400,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            actions=[
                ft.TextButton(
                    text="Check",
                    on_click=on_ok,
                ),
                ft.TextButton(
                    text="Cancel",
                    on_click=on_close,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = forgot_code_dialog1
        forgot_code_dialog1.open = True
        page.update()
    else:
        message_dialogs(page, "Forgot Code?")


def generate_result(page: ft.Page):
    from ..service.files.result import generate_result_fun

    def on_close(e):
        generate_result_alertdialog.open = False
        page.update()

    def on_ok(e):
        generate_result_alertdialog.open = False
        page.update()
        generate_result_fun()
        loading_dialogs(page, "Generating...", 1)

    # AlertDialog data
    generate_result_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Make sure?",
            font_family='Verdana',
        ),
        content=ft.Text(
            value=f"{messages['re_result']}",
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Yes",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="No",
                on_click=on_close,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    ele_ser_2 = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')
    if ele_ser_2.loc['result'].values[0]:
        page.dialog = generate_result_alertdialog
        generate_result_alertdialog.open = True
        page.update()
    else:
        ele_ser_2.loc['result'] = True
        ele_ser_2.to_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table', index=True)
        generate_result_fun()
        loading_dialogs(page, "Generating...", 1)


def result_view_dialogs(page: ft.Page):
    result_view_dialogs1 = ft.AlertDialog(
        modal=False,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_close(e):
        result_view_dialogs1.open = False
        page.update()

    result_df = pd.read_json(ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["result"]}',
                             orient='table')
    # Table
    result_view_table = ft.DataTable(
        column_spacing=20,
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Candidate Name")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Qualification")),
            ft.DataColumn(ft.Text("No.of Votes"))
        ],
    )

    result_view_row = []
    for i in range(len(result_df)):
        result_view_row.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(value=f"{i + 1}")),
                    ft.DataCell(ft.Text(value=f"{result_df.loc[i].values[1]}")),
                    ft.DataCell(ft.Text(value=f"{result_df.loc[i].values[2]}")),
                    ft.DataCell(ft.Text(value=f"{result_df.loc[i].values[3]}")),
                    ft.DataCell(ft.Text(value=f"{result_df.loc[i].values[5]}")),
                ],
            )
        )

    result_view_table.rows = result_view_row
    data_list1: list = [
        ft.Row(
            [
                result_view_table,
            ],
        )
    ]

    # AlertDialog data
    result_view_dialogs1.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Result",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                                font_family='Verdana',
                            ),
                        ],
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CLOSE_ROUNDED,
                                tooltip="Close",
                                on_click=on_close,
                            )
                        ]
                    )
                ],
                width=800,
            ),
            ft.Column(
                controls=data_list1,
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=550,
        width=800,
    )

    # Open dialog
    page.dialog = result_view_dialogs1
    result_view_dialogs1.open = True
    page.update()

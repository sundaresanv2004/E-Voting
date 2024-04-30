import flet as ft

from ..functions.dialogs import message_dialogs
from ..service.scr.local_files_scr import all_done_message


def all_done_page(page: ft.Page, content_column: ft.Column):
    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

    def on_change_button(e):
        if checkbox_terms.value is True:
            button_container.disabled = False
            button_container.tooltip = None
            button_container.bgcolor = "#0ea5e9"
            button_container.opacity = 1
            button_container.on_hover = on_hover_color
        else:
            button_container.disabled = True
            button_container.tooltip = 'Disabled'
            button_container.bgcolor = "#bae6fd"
            button_container.opacity = 0.5
            button_container.on_hover = None
        button_container.update()

    button_container = ft.Container(
        width=300,
        height=50,
        border_radius=10,
        bgcolor="#bae6fd",
        opacity=0.5,
        disabled=True,
        tooltip='Disabled',
        content=ft.Text(
            value="Restart",
            size=20,
            font_family='Verdana',
            weight=ft.FontWeight.W_400,
            color=ft.colors.WHITE,
        ),
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE),
        on_click=lambda e: message_dialogs(page, 'Restart Required'),
    )

    # Input Filed
    checkbox_terms = ft.Checkbox(
        label="I have read and understand the above information.",
        value=False,
        adaptive=True,
        on_change=on_change_button,
    )

    # alignment and data
    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            name=ft.icons.DONE_ALL_ROUNDED,
                            size=40,
                        ),
                        ft.Text(
                            value="All Done",
                            size=35,
                            weight=ft.FontWeight.W_600,
                            font_family='Verdana',
                        ),
                    ],
                    width=450,
                    height=70,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    key='top'
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Markdown(
                                    selectable=False,
                                    value=all_done_message,
                                    code_theme="atom-one-dark",
                                    code_style=ft.TextStyle(font_family="Verdana"),
                                )
                            ],
                            width=400,
                        ),
                        ft.Column(
                            [
                                checkbox_terms,
                                ft.Row(
                                    [
                                        button_container
                                    ],
                                    width=450,
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ],
                            width=400,
                            spacing=30,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(height=20),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_CIRCLE_UP_ROUNDED,
                            tooltip='Back to Top',
                            icon_size=30,
                            icon_color=ft.colors.BLACK87,
                            on_click=lambda _: content_column.scroll_to(key="top", duration=1000)
                        ),
                        ft.Row(width=1)
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    content_column.expand = True
    page.update()

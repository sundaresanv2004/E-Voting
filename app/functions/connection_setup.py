import flet as ft
import re

from ..service.files.local_files_scr import firebase_project


def connection_setup(page: ft.Page):
    def on_ok(e):
        if len(entry_box.value) > 0:
            entry_box.error_text = None
            match = re.search(r'const firebaseConfig = \{([^}]+)\};', entry_box.value, re.DOTALL)

            if match:
                pass
            else:
                entry_box.error_text = "invalid config code."
                entry_box.focus()
        else:
            entry_box.error_text = "Paste or Enter the config code."
            entry_box.focus()
        page.update()

    def troubleshoot(e):
        connection_error.open = False
        page.update()
        troubleshoot_file_error(page)

    entry_box = ft.TextField(
        hint_text='{apiKey: "your-api-key",\ndatabaseURL: "https://your-app.firebaseio.com",\n...}',
        multiline=True,
        border_radius=ft.border_radius.all(8),
        max_lines=4,
    )

    upload_file = ft.Row(
        [
            ft.TextButton(
                icon=ft.icons.UPLOAD_FILE_ROUNDED,
                text="Upload file",
            )
        ]
    )

    # AlertDialog data
    connection_error = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Connect Firebase",
            font_family='Verdana',
        ),
        content=ft.Column(
            [
                ft.Text(
                    value="To proceed, please paste the app config dictionary generated by your Firebase project. If you don't have a Firebase project yet, please contact support for assistance or refer to our GitHub repository for help.",
                    font_family='Verdana',
                    width=650
                ),
                entry_box,
                upload_file,
            ],
            spacing=20,
            height=260,
        ),
        actions=[
            ft.TextButton(
                text="Help",
                on_click=troubleshoot,
            ),
            ft.TextButton(
                text="Connect",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = connection_error
    connection_error.open = True
    page.update()


def troubleshoot_file_error(page: ft.Page):
    def on_ok(e):
        troubleshoot.open = False
        page.update()
        connection_setup(page)

    content_column = ft.Column(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            name=ft.icons.TROUBLESHOOT_ROUNDED,
                                            size=30
                                        ),
                                        ft.Text(
                                            value="How to Create Firebase Project",
                                            font_family='Verdana',
                                            size=27,
                                            weight=ft.FontWeight.W_700
                                        )
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.CLOSE_ROUNDED,
                                            on_click=on_ok,
                                            tooltip="Close",
                                            icon_color=ft.colors.BLACK,
                                            icon_size=25,
                                        )
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            key='top'
                        ),
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Video(
                                        playlist=[
                                            ft.VideoMedia(
                                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                                            )
                                        ],
                                        fill_color=ft.colors.TRANSPARENT,
                                        autoplay=False,
                                        muted=True,
                                        filter_quality=ft.FilterQuality.HIGH,
                                        aspect_ratio=16 / 9,
                                        playlist_mode=ft.PlaylistMode.NONE
                                    ),
                                    border_radius=10,
                                    margin=ft.margin.all(10),
                                )
                            ]
                        ),
                        ft.Markdown(
                            selectable=False,
                            value=firebase_project,
                            code_theme="atom-one-dark",
                            code_style=ft.TextStyle(font_family="Verdana"),
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
                            ],
                            width=650,
                            alignment=ft.MainAxisAlignment.END
                        )
                    ]
                ),
                padding=ft.padding.only(right=15)
            ),
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        width=650,
        height=650,
    )

    # AlertDialog data
    troubleshoot = ft.AlertDialog(
        modal=True,
        content=content_column,
    )

    page.dialog = troubleshoot
    troubleshoot.open = True
    page.update()

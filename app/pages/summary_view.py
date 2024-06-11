import flet as ft
import pandas as pd

from app.service.files.check_installation import path
from app.service.files.local_files_scr import file_path

index_v = None


def summary_view_page(page: ft.Page, vote_df: pd.DataFrame):
    global index_v
    setting_ser = pd.read_json(path + file_path['settings'], orient='table')
    path_election = path + rf"/data/e/{setting_ser.at['election_name', 'values']}"

    candidate_image_destination = path_election + r'/'
    final_category_data2 = pd.read_csv(path_election + r'/category_data.csv')
    category_list2 = list(final_category_data2['category_name'])
    candidate_df = pd.read_json(path + file_path["candidate_data"], orient='table')
    cat_enc_dict = {}
    for i in range(len(final_category_data2)):
        cat_enc_dict[final_category_data2.at[i, 'category_id']] = final_category_data2.at[i, 'category_name']

    result = pd.DataFrame(columns=['id', 'candidate_name', 'category', 'image', 'no_of_votes'])

    for i in range(len(candidate_df)):
        if candidate_df.at[i, 'candidate_id'] in vote_df.columns.to_list():
            result.loc[i] = [
                candidate_df.at[i, 'candidate_id'],
                candidate_df.at[i, 'name'],
                cat_enc_dict[candidate_df.at[i, 'category']],
                candidate_df.at[i, 'image'],
                sum(vote_df[candidate_df.at[i, 'candidate_id']].to_list())
            ]

    temp_sum_df = pd.DataFrame(columns=['id', 'candidate_name', 'category', 'image', "no_of_votes"])
    index_a = 0
    for i in category_list2:
        df_1 = result[result.category == i]
        max_val = df_1['no_of_votes'].max()
        c_ = df_1[df_1.no_of_votes == max_val].values
        for k in c_:
            temp_sum_df.loc[index_a] = k
            index_a += 1

    def on_close(e):
        summary_view_profile.open = False
        page.update()

    index_v = 0

    def next_fun(e):
        global index_v
        index_v += 1
        content_change()
        page.update()

    def back_fun(e):
        global index_v
        index_v -= 1
        content_change()
        page.update()

    next_button = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
        icon_size=30,
        tooltip='Next',
        on_click=next_fun,
    )

    back_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
        icon_size=30,
        tooltip="Previous",
        on_click=back_fun,
    )

    container = ft.Container(
        width=200,
        height=250,
        alignment=ft.alignment.center,
        border=ft.border.all(0.5, ft.colors.SECONDARY),
        border_radius=ft.border_radius.all(5),
    )

    def button_check():
        if index_v == 0:
            back_button.disabled = True
        else:
            back_button.disabled = False

        if index_v == temp_sum_df.index.max():
            next_button.disabled = True
        else:
            next_button.disabled = False

    title1 = ft.Text(
        weight=ft.FontWeight.W_500,
        font_family='Verdana',
        size=20,
    )

    name_text = ft.Text(
        font_family='Verdana',
        size=20,
    )

    category_text = ft.Text(
        font_family='Verdana',
        size=20,
    )

    no_of_vote = ft.Text(
        font_family='Verdana',
        size=20,
    )

    def content_change():
        global index_v
        user_data = temp_sum_df.loc[index_v].values
        button_check()
        title1.value = f"Candidate ID: {user_data[0]}"
        name_text.value = f"Name: {user_data[1]}"
        category_text.value = f"Category: {user_data[2]}"
        no_of_vote.value = f"No.of votes: {user_data[4]}"

        if user_data[3] != False:
            container.content = ft.Text()
            container.image_src = candidate_image_destination + f'{user_data[3]}'
            container.image_fit = ft.ImageFit.COVER
        else:
            container.image_src = None
            container.content = ft.Column(
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

    content_change()

    summary_view_profile = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                title1,
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
                    ]
                ),
                ft.Row(
                    [
                        back_button,
                        ft.Row(
                            [
                                container,
                                ft.Column(
                                    [
                                        name_text,
                                        category_text,
                                        no_of_vote,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=25,
                            width=640,
                            scroll=ft.ScrollMode.ADAPTIVE,
                        ),
                        next_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    width=750,
                    height=320,
                ),

            ],
            height=370,
            width=750,
        )
    )

    page.dialog = summary_view_profile
    summary_view_profile.open = True
    page.update()
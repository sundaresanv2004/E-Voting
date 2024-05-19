import flet as ft

from .start_page import start_page


def layout(page) -> None:
    def route_change(e: ft.RouteChangeEvent) -> None:
        print(page.views)
        page.views.clear()

        page.views.append(
            ft.View(
                "/",
                controls=start_page(page)
            )
        )

        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )

        page.update()

    page.on_route_change = route_change
    # page.on_view_pop = view_pop
    page.go(page.route)

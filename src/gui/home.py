import flet as ft
from srv import ui_controller as ui


def show(page: ft.Page):
    global content_column
    content_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    bgcolor="#222831",
                    border_radius=20,
                    padding=10,
                    margin=10,
                    width=200,
                    height=620,
                    content=ft.Column(
                        [
                            ft.Text(
                                "MENU",
                                color="#EEEEEE",
                                size=24,
                                weight=ft.FontWeight.W_800,
                                align=ft.Alignment.CENTER,
                            ),
                            ft.ElevatedButton(
                                "ADD USER",
                                bgcolor="#393E46",
                                color="#00ADB5",
                                icon=ft.Icons.ADD,
                                align=ft.Alignment.CENTER,
                                on_click=lambda _: ui.show_create(page),
                            ),
                            ft.ElevatedButton(
                                "LIST USERS",
                                bgcolor="#393E46",
                                color="#00ADB5",
                                icon=ft.Icons.LIST,
                                align=ft.Alignment.CENTER,
                                on_click=lambda _: ui.show_list(page),
                            ),
                        ],
                        ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    bgcolor="#222831",
                    border_radius=20,
                    padding=10,
                    margin=10,
                    expand=True,
                    height=620,
                    content=content_column,
                ),
            ]
        )
    )

from asyncio import create_task
import flet as ft
from srv import controller
from srv import ui_controller as ui


def show(page: ft.Page):
    users = controller.get_users()
    if users:
        ft.Text("USERS", size=22, weight=ft.FontWeight.BOLD)
        cards_row = ft.Row(wrap=True, expand=True, spacing=5, scroll=ft.ScrollMode.AUTO)
        for uid in users:
            id = uid[0]
            user = controller.get_user(id)

            cards_row.controls.append(
                ft.Card(
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(
                                    f"ID: {user.id}",
                                    weight=ft.FontWeight.BOLD,
                                    color="#EEEEEE",
                                ),
                                ft.Text(
                                    f"TITLE: {user.title}", color="#EEEEEE", size=12
                                ),
                                ft.Text(
                                    f"USERNAME/EMAIL: {user.user}",
                                    color="#EEEEEE",
                                    size=12,
                                ),
                                ft.Text(f"SITE: {user.site}", color="#EEEEEE", size=12),
                                ft.Row(
                                    [
                                        ft.Text(
                                            f"PASSWORD: {user.password}",
                                            color="#EEEEEE",
                                            size=12,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.COPY,
                                            icon_color="#00ADB5",
                                            icon_size=12,
                                            on_click=lambda _, pswd=user.password: (
                                                create_task(ui.copy_clip(pswd, page))
                                            ),
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_size=14,
                                            icon_color="#00ADB5",
                                            on_click=lambda _, uid=user.id: (
                                                ui.show_update(page, uid)
                                            ),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_size=14,
                                            icon_color="red",
                                            on_click=lambda _, uid=user.id: (
                                                page.show_dialog(
                                                    ft.AlertDialog(
                                                        title=ft.Text("DELETE USER"),
                                                        content=ft.Text(
                                                            "DO YOU WANT TO REMOVE THE SELECTED USER?"
                                                        ),
                                                        actions=[
                                                            ft.TextButton(
                                                                "YES",
                                                                on_click=lambda _: (
                                                                    page.pop_dialog(),
                                                                    page.show_dialog(
                                                                        ft.AlertDialog(
                                                                            title="DELETE USER",
                                                                            content=ft.Text(
                                                                                controller.delete_user(
                                                                                    uid
                                                                                )
                                                                            ),
                                                                            actions=[
                                                                                ft.TextButton(
                                                                                    "OK",
                                                                                    on_click=lambda _: (
                                                                                        page.pop_dialog(),
                                                                                        page.update(),
                                                                                        ui.show_list(
                                                                                            page
                                                                                        ),
                                                                                    ),
                                                                                )
                                                                            ],
                                                                        )
                                                                    ),
                                                                ),
                                                            ),
                                                            ft.TextButton(
                                                                "NO",
                                                                on_click=lambda _: (
                                                                    page.pop_dialog(),
                                                                    page.update(),
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                page.update(),
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            spacing=2,
                        ),
                        bgcolor="#393E46",
                        padding=10,
                        width=250,
                        border_radius=10,
                    ),
                    margin=5,
                )
            )
        return cards_row
    else:
        no_users = ft.Text("NO USERS FOUND")
        return no_users

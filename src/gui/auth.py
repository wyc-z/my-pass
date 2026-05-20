import flet as ft
from srv import controller
from srv import ui_controller as ui


def show(page: ft.Page):

    username_input = ft.TextField(label="USERNAME", color="#EEEEEE", bgcolor="#393E46")
    password_input = ft.TextField(
        label="PASSWORD",
        color="#EEEEEE",
        bgcolor="#393E46",
        password=True,
        can_reveal_password=True,
    )
    login_verify = ft.ElevatedButton(
        "LOGIN",
        bgcolor="#393E46",
        color="#00ADB5",
        on_click=lambda _: controller.verify_admin(
            username_input.value, password_input.value, page
        ),
    )

    page.add(
        ft.Container(
            bgcolor="#222831",
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Text(
                        "LOGIN",
                        color="#EEEEEE",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    username_input,
                    password_input,
                    login_verify,
                ]
            ),
        )
    )


def show_create(page: ft.Page):
    username_input = ft.TextField(label="USERNAME", color="#EEEEEE", bgcolor="#393E46")
    password_input = ft.TextField(
        label="PASSWORD",
        color="#EEEEEE",
        bgcolor="#393E46",
        password=True,
        can_reveal_password=True,
    )
    password_input_v = ft.TextField(
        label="CONFIRM PASSWORD", color="#EEEEEE", bgcolor="#393E46"
    )
    login_verify = ft.ElevatedButton(
        "SAVE ADMIN",
        bgcolor="#393E46",
        color="#00ADB5",
        on_click=lambda _: page.show_dialog(
            ft.AlertDialog(
                title="SAVE ADMIN",
                content=ft.Text(
                    controller.save_admin(
                        username_input.value,
                        password_input.value,
                        password_input_v.value,
                    )
                ),
                actions=[
                    ft.TextButton(
                        "OK", on_click=lambda _: (page.pop_dialog(), ui.show_main(page))
                    )
                ],
            )
        ),
    )

    page.add(
        ft.Container(
            bgcolor="#222831",
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Text(
                        "REGISTER ADMIN",
                        color="#EEEEEE",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    username_input,
                    password_input,
                    password_input_v,
                    login_verify,
                ]
            ),
        )
    )

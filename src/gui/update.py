import flet as ft
from srv import controller
from srv import ui_controller as ui


def show(page: ft.Page, uid: int):

    user = controller.get_user(uid)

    title_input = ft.TextField(
        label="TITLE",
        width=400,
        border_radius=15,
        color="#EEEEEE",
        bgcolor="#393E46",
        value=user.title,
    )
    username_input = ft.TextField(
        label="USERNAME/EMAIL",
        width=400,
        border_radius=15,
        color="#EEEEEE",
        bgcolor="#393E46",
        value=user.user,
    )
    password_input = ft.TextField(
        label="PASSWORD",
        width=400,
        password=True,
        can_reveal_password=True,
        border_radius=15,
        color="#EEEEEE",
        bgcolor="#393E46",
        value=user.password,
    )
    site_input = ft.TextField(
        label="SITE",
        width=400,
        border_radius=15,
        color="#EEEEEE",
        bgcolor="#393E46",
        value=user.site,
    )
    password_length = 12
    symbols_value = True

    def symbols_change(e):
        nonlocal symbols_value
        symbols_value = e.control.value
        run_generate()

    def slider_change(e):
        nonlocal password_length
        password_length = int(e.control.value)
        run_generate()

    def run_generate():
        password_input.value = controller.gen_pswd(password_length, symbols_value)
        page.update()

    slider = ft.Slider(
        active_color="#00ADB5",
        min=8,
        max=32,
        divisions=24,
        value=password_length,
        width=300,
        on_change=slider_change,
    )
    symbols = ft.Checkbox(value=True, on_change=symbols_change)

    content_column = [
        ft.Text("UPDATE USER", size=22, weight=ft.FontWeight.BOLD, color="#EEEEEE"),
        title_input,
        username_input,
        password_input,
        ft.Row(
            [
                ft.Text("Password Length: ", color="#EEEEEE"),
                slider,
                ft.Text("Symbols: ", color="#EEEEEE"),
                symbols,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        site_input,
        ft.ElevatedButton(
            "UPDATE",
            color="#00ADB5",
            bgcolor="#393E46",
            on_click=lambda _: (
                page.show_dialog(
                    ft.AlertDialog(
                        title=ft.Text("USER UPDATED"),
                        content=ft.Text(
                            controller.update_user(
                                title_input.value,
                                username_input.value,
                                site_input.value,
                                password_input.value,
                                uid,
                            ),
                            page.update(),
                        ),
                        actions=[
                            ft.TextButton(
                                "OK",
                                on_click=lambda _: (
                                    page.pop_dialog(),
                                    page.update(),
                                ),
                            )
                        ],
                    ),
                ),
                page.update(),
                ui.show_list(page),
            ),
        ),
    ]
    return content_column

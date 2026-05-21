import flet as ft
from gui import auth
from srv import controller


def main(page: ft.Page):
    page.title = "My Pass"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#393E46"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    if controller.exist_db_admin():
        auth.show(page)
    else:
        auth.show_create(page)


if __name__ == "__main__":
    ft.run(main)

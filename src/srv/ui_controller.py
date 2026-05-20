import main
from gui import create, home, list, update
import flet as ft


def show_home(page: ft.Page):
    page.clean()
    home.show(page)


def show_create(page: ft.Page):
    home.content_column.controls.clear()
    home.content_column.controls.extend(create.show(page))
    page.update()


def show_list(page: ft.Page):
    home.content_column.controls.clear()
    home.content_column.controls.append(list.show(page))
    page.update()


def show_update(page: ft.Page, uid):
    home.content_column.controls.clear()
    home.content_column.controls.extend(update.show(page, uid))
    page.update()


def show_main(page: ft.Page):
    page.clean()
    main.main(page)


def invalid_admin(page: ft.Page):
    page.show_dialog(
        ft.AlertDialog(
            title="INVALID CREDENTIALS",
            content=ft.Text("VERIFY THAT USERNAME AND PASSWORD ARE CORRECT"),
            actions=[ft.TextButton("OK", on_click=lambda _: page.pop_dialog())],
        )
    )


async def copy_clip(data: str, page: ft.Page):
    await ft.Clipboard().set(data or "")
    page.show_dialog(ft.SnackBar("Text copied!"))
    page.update()

from pathlib import Path

from auth import crypt
from db import requests
from domain import modules
from srv import ui_controller as ui

directory = str(Path(__file__).resolve().parent.parent / "vault")


def gen_pswd(length: int, sym: bool) -> str:
    return crypt.generate_password(length, sym)


def save_user(title: str, username: str, site: str, password: str):
    if not title or not password:
        return "ERROR: TITLE AND PASSWORD ARE REQUIRED!"
    tt, usr, st, pswd, nonce = crypt.encrypt(title, username, site, password)
    requests.Accounts(tt, usr, st, pswd, nonce).save()
    return "USER SAVED SUCCESFULLY!"


def update_user(title: str, username: str, site: str, password: str, uid: int):
    if not title or not password:
        return "ERROR: TITLE AND PASSWORD ARE REQUIRED!"
    tt, usr, st, pswd, nonce = crypt.encrypt(title, username, site, password)
    requests.Accounts(tt, usr, st, pswd, nonce).update(uid)
    return "USER UPDATED SUCCESFULLY!"


def delete_user(uid: int):
    requests.Accounts.delete(uid)
    return "USER DELETED SUCCESFULLY!"


def get_user(uid: int):
    title, username, site, password, nonce = requests.Accounts.get(uid)
    tt, usr, st, pswd = crypt.decrypt(title, username, site, password, nonce)
    user = modules.Account(uid, tt, usr, st, pswd)
    return user


def get_users():
    users = requests.Accounts.get_all()
    return users


def exist_db_admin():
    if Path(requests.database).exists() and requests.Admin.get():
        return True
    return False


def validate_key():
    key = crypt.get_key()
    if len(key) != 32:
        raise RuntimeError("CORRUPT SECRET KEY")


def db_integrity():
    if Path(requests.database).exists():
        requests.check()


def save_admin(user: str, password: str, passwordv: str):
    if not all((user, password, passwordv)):
        return "FILL IN ALL THE FIELDS!"
    elif password != passwordv:
        return "PASSWORDS DON'T MATCH"
    Path(directory).mkdir(exist_ok=True)
    requests.init()
    usr, pswd, nonce = crypt.encrypt_admin(user, password)
    requests.Admin(usr, pswd, nonce).save()
    return "ADMIN SAVED SUCCESFULLY!"


def verify_admin(user: str, password: str, page):
    u, p, n = requests.Admin.get()
    usr, pswd = crypt.decrypt_admin(u, p, n)
    if user == usr and password == pswd:
        ui.show_home(page)
    else:
        ui.invalid_admin(page)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from pathlib import Path
import secrets
import string

key_path = str(Path(__file__).resolve().parent.parent / "vault" / "secret.key")


def generate_password(length: int, symbols: bool):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    pswd = "".join(secrets.choice(chars) for _ in range(length))
    return pswd


def get_key():
    try:
        with open(key_path, "rb") as k:
            key = k.read()
    except (FileNotFoundError, OSError):
        key = None
    if not key:
        key = AESGCM.generate_key(256)
        with open(key_path, "wb") as k:
            k.write(key)
    return key


def encrypt_admin(user: str, password: str):
    key = get_key()
    aes = AESGCM(key)
    nonce = os.urandom(12)
    usr = aes.encrypt(nonce, user.encode(), None)
    pswd = aes.encrypt(nonce, password.encode(), None)
    return usr, pswd, nonce


def decrypt_admin(user: bytes, password: bytes, nonce: bytes):
    key = get_key()
    aes = AESGCM(key)
    usr = aes.decrypt(nonce, user, None).decode()
    pswd = aes.decrypt(nonce, password, None).decode()
    return usr, pswd


def encrypt(title: str, user: str, site: str, password: str):
    key = get_key()
    aes = AESGCM(key)
    nonce = os.urandom(12)
    tt = aes.encrypt(nonce, title.encode(), None)
    usr = aes.encrypt(nonce, user.encode(), None)
    st = aes.encrypt(nonce, site.encode(), None)
    pswd = aes.encrypt(nonce, password.encode(), None)
    return tt, usr, st, pswd, nonce


def decrypt(title: bytes, user: bytes, site: bytes, password: bytes, nonce: bytes):
    key = get_key()
    aes = AESGCM(key)
    tt = aes.decrypt(nonce, title, None).decode()
    usr = aes.decrypt(nonce, user, None).decode()
    st = aes.decrypt(nonce, site, None).decode()
    pswd = aes.decrypt(nonce, password, None).decode()
    return tt, usr, st, pswd

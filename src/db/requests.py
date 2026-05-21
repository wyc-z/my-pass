import sqlite3
from pathlib import Path

database = str(Path(__file__).resolve().parent.parent / "vault" / "data.db")


def init():
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY,
            username BYTES,
            password BYTES,
            nonce BYTES);

            CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            title BYTES,
            user BYTES,
            site BYTES,
            password BYTES,
            nonce BYTES
            );""")


def check():
    with sqlite3.connect(database) as conn:
        result = conn.execute("PRAGMA integrity_check").fetchone()
        if result[0] != "ok":
            raise RuntimeError(f"Database corrupted: {result[0]}")


class Admin:
    def __init__(self, username: bytes, password: bytes, nonce: bytes):
        if username and password and nonce:
            self._username = username
            self._password = password
            self._nonce = nonce

    def save(self):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO admin (
                username,
                password,
                nonce)
                VALUES(?,?,?)""",
                (self._username, self._password, self._nonce),
            )

    def update(self):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE INTO admin (
                username,
                password,
                nonce)
                VALUES(?,?,?)
                WHERE id=1
                """,
                (self._username, self._password, self._nonce),
            )

    @classmethod
    def delete(cls):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=OFF;")
            for (table,) in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            ):
                cur.execute(f"DROP TABLE IF EXISTS '{table}';")

    @classmethod
    def get(cls):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT username, password, nonce FROM admin WHERE id=1
                """
            )
            return cur.fetchone()


class Accounts:
    def __init__(
        self, title: bytes, username: bytes, site: bytes, password: bytes, nonce: bytes
    ):
        self._title = title
        self._username = username
        self._site = site
        self._password = password
        self._nonce = nonce

    def save(self):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO accounts (
                title,
                user,
                site,
                password,
                nonce)
                VALUES(?,?,?,?,?)""",
                (self._title, self._username, self._site, self._password, self._nonce),
            )

    def update(self, uid):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE accounts SET
                title=?,
                user=?,
                site=?,
                password=?,
                nonce=?
                WHERE id=?
                """,
                (
                    self._title,
                    self._username,
                    self._site,
                    self._password,
                    self._nonce,
                    uid,
                ),
            )

    @classmethod
    def delete(cls, uid: int):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM accounts WHERE id=?", (uid,))

    @classmethod
    def get(cls, uid):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT title, user, site, password, nonce FROM accounts WHERE id=?",
                (uid,),
            )
            return cur.fetchone()

    @classmethod
    def get_all(cls):
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM accounts ORDER BY id")
            return cur.fetchall()

import sqlite3
import pytest

from pathlib import Path


class TestInit:
    def test_create_tables(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        conn = sqlite3.connect(db_path)
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        conn.close()
        assert "admin" in tables
        assert "accounts" in tables

    def test_idempotent(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        db.requests.init()
        conn = sqlite3.connect(db_path)
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        conn.close()
        assert "admin" in tables
        assert "accounts" in tables


class TestCheck:
    def test_return_ok(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        db.requests.check()

    def test_raises_on_corrupt(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        Path(db_path).write_bytes(b"not a valid sqlite database")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        with pytest.raises((RuntimeError, sqlite3.DatabaseError)):
            db.requests.check()


class TestAdmin:
    def test_save_and_get(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        admin = db.requests.Admin(b"user_enc", b"pass_enc", b"nonce1234")
        admin.save()
        result = db.requests.Admin.get()
        assert result is not None
        assert result[0] == b"user_enc"
        assert result[1] == b"pass_enc"
        assert result[2] == b"nonce1234"

    def test_get_returns_none(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        result = db.requests.Admin.get()
        assert result is None

    def test_delete_admin(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        db.requests.Admin(b"u", b"p", b"n").save()
        assert db.requests.Admin.get() is not None
        db.requests.Admin.delete()
        with pytest.raises(sqlite3.OperationalError):
            db.requests.Admin.get()


class TestAccounts:
    @pytest.fixture
    def setup_db(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "accounts_test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        return db.requests

    def test_save_and_get(self, setup_db):
        requests = setup_db
        acc = requests.Accounts(b"tt", b"uu", b"ss", b"pp", b"nn")
        acc.save()
        result = requests.Accounts.get(1)
        assert result == (b"tt", b"uu", b"ss", b"pp", b"nn")

    def test_get_nonexistent(self, setup_db):
        requests = setup_db
        result = requests.Accounts.get(999)
        assert result is None

    def test_update(self, setup_db):
        requests = setup_db
        acc = requests.Accounts(b"tt", b"uu", b"ss", b"pp", b"nn")
        acc.save()
        updated = requests.Accounts(
            b"new_tt", b"new_uu", b"new_ss", b"new_pp", b"new_nn"
        )
        updated.update(1)
        result = requests.Accounts.get(1)
        assert result == (b"new_tt", b"new_uu", b"new_ss", b"new_pp", b"new_nn")

    def test_delete(self, setup_db):
        requests = setup_db
        acc = requests.Accounts(b"tt", b"uu", b"ss", b"pp", b"nn")
        acc.save()
        requests.Accounts.delete(1)
        result = requests.Accounts.get(1)
        assert result is None

    def test_delete_idempotent(self, setup_db):
        requests = setup_db
        requests.Accounts.delete(999)

    def test_get_all(self, setup_db):
        requests = setup_db
        for i in range(3):
            data = (f"t{i}".encode(), b"u", b"s", b"p", b"n")
            requests.Accounts(*data).save()
        result = requests.Accounts.get_all()
        assert result == [(1,), (2,), (3,)]

    def test_get_all_empty(self, setup_db):
        requests = setup_db
        result = requests.Accounts.get_all()
        assert result == []

    def test_multiple_ids(self, setup_db):
        requests = setup_db
        for i in range(5):
            requests.Accounts(
                f"t{i}".encode(), f"u{i}".encode(), b"s", b"p", b"n"
            ).save()
        result = requests.Accounts.get_all()
        ids = [row[0] for row in result]
        assert ids == [1, 2, 3, 4, 5]

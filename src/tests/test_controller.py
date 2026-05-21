import sys
from unittest.mock import MagicMock, patch, PropertyMock
import pytest
from pathlib import Path

mock_ui_module = MagicMock()
sys.modules["srv.ui_controller"] = mock_ui_module
from srv import controller
from domain.modules import Account


class TestGenPswd:
    def test_gen_password(self):
        with patch.object(
            controller.crypt, "generate_password", return_value="abc123"
        ) as mock_gen:
            result = controller.gen_pswd(12, True)
            mock_gen.assert_called_once_with(12, True)
            assert result == "abc123"


class TestSaveUser:
    def test_save_user(self):
        encrypted = (b"t", b"u", b"s", b"p", b"nonce")
        with (
            patch.object(
                controller.crypt, "encrypt", return_value=encrypted
            ) as mock_enc,
            patch.object(controller.requests.Accounts, "save") as mock_save,
        ):
            result = controller.save_user("Title", "User", "Site", "Pass")
            assert result == "USER SAVED SUCCESFULLY!"
            mock_enc.assert_called_once_with("Title", "User", "Site", "Pass")
            mock_save.assert_called_once()

    def test_requires_title(self):
        result = controller.save_user("", "User", "Site", "Pass")
        assert result == "ERROR: TITLE AND PASSWORD ARE REQUIRED!"

    def test_require_password(self):
        result = controller.save_user("Title", "User", "Site", "")
        assert result == "ERROR: TITLE AND PASSWORD ARE REQUIRED!"

    def test_require_title_and_password(self):
        result = controller.save_user("", "User", "Site", "")
        assert result == "ERROR: TITLE AND PASSWORD ARE REQUIRED!"


class TestUpdateUser:
    def test_update_user(self):
        encrypted = (b"t", b"u", b"s", b"p", b"nonce")
        with (
            patch.object(
                controller.crypt, "encrypt", return_value=encrypted
            ) as mock_enc,
            patch.object(controller.requests.Accounts, "update") as mock_update,
        ):
            result = controller.update_user("Title", "User", "Site", "Pass", 1)
            assert result == "USER UPDATED SUCCESFULLY!"
            mock_enc.assert_called_once_with("Title", "User", "Site", "Pass")
            mock_update.assert_called_once_with(1)

    def test_require_title(self):
        result = controller.update_user("", "User", "Site", "Pass", 1)
        assert result == "ERROR: TITLE AND PASSWORD ARE REQUIRED!"

    def test_require_password(self):
        result = controller.update_user("Title", "User", "Site", "", 1)
        assert result == "ERROR: TITLE AND PASSWORD ARE REQUIRED!"


class TestDeleteUser:
    def test_delete_user(self):
        with patch.object(controller.requests.Accounts, "delete") as mock_delete:
            result = controller.delete_user(5)
            assert result == "USER DELETED SUCCESFULLY!"
            mock_delete.assert_called_once_with(5)


class TestGetUser:
    def test_return_account(self):
        encrypted = (b"t_enc", b"u_enc", b"s_enc", b"p_enc", b"nonce")
        decrypted = ("MyTitle", "MyUser", "MySite", "MyPass")
        with (
            patch.object(
                controller.requests.Accounts, "get", return_value=encrypted
            ) as mock_get,
            patch.object(
                controller.crypt, "decrypt", return_value=decrypted
            ) as mock_decrypt,
        ):
            result = controller.get_user(3)
            assert isinstance(result, Account)
            assert result.id == 3
            assert result.title == "MyTitle"
            assert result.user == "MyUser"
            assert result.site == "MySite"
            assert result.password == "MyPass"
            mock_get.assert_called_once_with(3)
            mock_decrypt.assert_called_once_with(*encrypted)


class TestGetUsers:
    def test_return_all_users(self):
        users = [(1,), (2,), (3,)]
        with patch.object(
            controller.requests.Accounts, "get_all", return_value=users
        ) as mock_get_all:
            result = controller.get_users()
            assert result == users
            mock_get_all.assert_called_once()

    def test_empty_list(self):
        with patch.object(controller.requests.Accounts, "get_all", return_value=[]):
            result = controller.get_users()
            assert result == []


class TestExistDbAdmin:
    def test_exists_db_admin(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        db.requests.Admin(b"u", b"p", b"n").save()
        assert controller.exist_db_admin() is True

    def test_not_exists_without_db(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "nonexistent.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        assert controller.exist_db_admin() is False

    def test_not_exists_without_admin(self, monkeypatch, tmp_path):
        db_path = str(tmp_path / "test.db")
        import db.requests

        monkeypatch.setattr(db.requests, "database", db_path)
        db.requests.init()
        assert controller.exist_db_admin() is False


class TestSaveAdmin:
    def test_saves_admin_successfully(self):
        encrypted = (b"u_enc", b"p_enc", b"nonce")
        with (
            patch.object(
                controller.crypt, "encrypt_admin", return_value=encrypted
            ) as mock_enc,
            patch.object(controller.requests, "init") as mock_init,
            patch.object(controller.requests.Admin, "save") as mock_save,
        ):
            result = controller.save_admin("admin", "pass", "pass")
            assert result == "ADMIN SAVED SUCCESFULLY!"
            mock_enc.assert_called_once_with("admin", "pass")
            mock_init.assert_called_once()
            mock_save.assert_called_once()

    def test_validates_empty_fields(self):
        result = controller.save_admin("", "pass", "pass")
        assert result == "FILL IN ALL THE FIELDS!"
        result = controller.save_admin("admin", "", "pass")
        assert result == "FILL IN ALL THE FIELDS!"
        result = controller.save_admin("admin", "pass", "")
        assert result == "FILL IN ALL THE FIELDS!"

    def test_validates_password_match(self):
        result = controller.save_admin("admin", "pass1", "pass2")
        assert result == "PASSWORDS DON'T MATCH"


class TestVerifyAdmin:
    def test_show_home_on_success(self):
        with patch.object(controller, "ui") as mock_ui:
            with patch.object(
                controller.requests.Admin, "get", return_value=(b"u", b"p", b"n")
            ):
                with patch.object(
                    controller.crypt, "decrypt_admin", return_value=("admin", "pass")
                ):
                    page = MagicMock()
                    controller.verify_admin("admin", "pass", page)
                    mock_ui.show_home.assert_called_once_with(page)

    def test_invalid_on_wrong_password(self):
        with patch.object(controller, "ui") as mock_ui:
            with patch.object(
                controller.requests.Admin, "get", return_value=(b"u", b"p", b"n")
            ):
                with patch.object(
                    controller.crypt, "decrypt_admin", return_value=("admin", "pass")
                ):
                    page = MagicMock()
                    controller.verify_admin("admin", "wrong", page)
                    mock_ui.invalid_admin.assert_called_once_with(page)

    def test_invalid_on_wrong_username(self):
        with patch.object(controller, "ui") as mock_ui:
            with patch.object(
                controller.requests.Admin, "get", return_value=(b"u", b"p", b"n")
            ):
                with patch.object(
                    controller.crypt, "decrypt_admin", return_value=("admin", "pass")
                ):
                    page = MagicMock()
                    controller.verify_admin("wrong", "pass", page)
                    mock_ui.invalid_admin.assert_called_once_with(page)

    def test_page_is_passed_to_ui(self):
        with patch.object(controller, "ui") as mock_ui:
            with patch.object(
                controller.requests.Admin, "get", return_value=(b"u", b"p", b"n")
            ):
                with patch.object(
                    controller.crypt, "decrypt_admin", return_value=("admin", "pass")
                ):
                    page = object()
                    controller.verify_admin("admin", "pass", page)
                    mock_ui.show_home.assert_called_once_with(page)

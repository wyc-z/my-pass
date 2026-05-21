from domain.modules import Account, Admin


class TestAccount:
    def test_create_account(self):
        acc = Account(1, "Gmail", "user@example.com", "gmail.com", "p@ssw0rd")
        assert acc.id == 1
        assert acc.title == "Gmail"
        assert acc.user == "user@example.com"
        assert acc.site == "gmail.com"
        assert acc.password == "p@ssw0rd"

    def test_account_is_mutable(self):
        acc = Account(1, "a", "b", "c", "d")
        acc.title = "New Title"
        assert acc.title == "New Title"


class TestAdmin:
    def test_create_admin(self):
        admin = Admin("root", "s3cret")
        assert admin.user == "root"
        assert admin.password == "s3cret"

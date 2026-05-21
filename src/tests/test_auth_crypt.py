import string
import auth.crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class TestGeneratePassword:
    def test_default_length(self):
        pswd = auth.crypt.generate_password(16, False)
        assert len(pswd) == 16

    def test_length_zero(self):
        pswd = auth.crypt.generate_password(0, False)
        assert pswd == ""

    def test_with_symbols(self):
        pswd = auth.crypt.generate_password(32, True)
        assert len(pswd) == 32
        assert any(c in string.punctuation for c in pswd)

    def test_without_symbols(self):
        pswd = auth.crypt.generate_password(16, False)
        assert len(pswd) == 16
        assert all(c in string.ascii_letters + string.digits for c in pswd)

    def test_randomness(self):
        p1 = auth.crypt.generate_password(32, True)
        p2 = auth.crypt.generate_password(32, True)
        assert p1 != p2


class TestGetKey:
    def test_returns_32_bytes(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        key = auth.crypt.get_key()
        assert len(key) == 32

    def test_generates_key_file_if_missing(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        assert not key_file.exists()
        auth.crypt.get_key()
        assert key_file.exists()
        assert key_file.stat().st_size == 32

    def test_loads_existing_key(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        key_file.write_bytes(b"k" * 32)
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        key = auth.crypt.get_key()
        assert key == b"k" * 32

    def test_is_deterministic_same_key(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        key1 = auth.crypt.get_key()
        key2 = auth.crypt.get_key()
        assert key1 == key2


class TestEncryptDecryptAdmin:
    def test_roundtrip(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        usr, pswd, nonce = auth.crypt.encrypt_admin("admin", "secret")
        dec_usr, dec_pswd = auth.crypt.decrypt_admin(usr, pswd, nonce)
        assert dec_usr == "admin"
        assert dec_pswd == "secret"

    def test_encryption_changes_each_call(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        u1, p1, n1 = auth.crypt.encrypt_admin("admin", "secret")
        u2, p2, n2 = auth.crypt.encrypt_admin("admin", "secret")
        assert n1 != n2
        assert u1 != u2

    def test_tampered_ciphertext_fails(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        usr, pswd, nonce = auth.crypt.encrypt_admin("admin", "secret")
        tampered = bytearray(usr)
        tampered[0] ^= 0xFF
        from cryptography.exceptions import InvalidTag
        import pytest
        with pytest.raises(InvalidTag):
            auth.crypt.decrypt_admin(bytes(tampered), pswd, nonce)


class TestEncryptDecrypt:
    def test_roundtrip(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        tt, usr, st, pswd, nonce = auth.crypt.encrypt(
            "Google", "user@google.com", "google.com", "myp@ss"
        )
        dec_tt, dec_usr, dec_st, dec_pswd = auth.crypt.decrypt(tt, usr, st, pswd, nonce)
        assert dec_tt == "Google"
        assert dec_usr == "user@google.com"
        assert dec_st == "google.com"
        assert dec_pswd == "myp@ss"

    def test_different_nonce_produces_different_ciphertext(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        t1, _, _, _, n1 = auth.crypt.encrypt("X", "x", "x", "x")
        t2, _, _, _, n2 = auth.crypt.encrypt("X", "x", "x", "x")
        assert n1 != n2
        assert t1 != t2

    def test_encrypt_with_empty_strings(self, monkeypatch, tmp_path):
        key_file = tmp_path / "secret.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file))
        tt, usr, st, pswd, nonce = auth.crypt.encrypt("", "", "", "")
        dec_tt, dec_usr, dec_st, dec_pswd = auth.crypt.decrypt(tt, usr, st, pswd, nonce)
        assert dec_tt == ""
        assert dec_usr == ""
        assert dec_st == ""
        assert dec_pswd == ""

    def test_two_keys_are_incompatible(self, monkeypatch, tmp_path):
        key_file_1 = tmp_path / "secret1.key"
        key_file_2 = tmp_path / "secret2.key"
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file_1))
        tt, usr, st, pswd, nonce = auth.crypt.encrypt("A", "B", "C", "D")
        monkeypatch.setattr(auth.crypt, "key_path", str(key_file_2))
        from cryptography.exceptions import InvalidTag
        import pytest
        with pytest.raises(InvalidTag):
            auth.crypt.decrypt(tt, usr, st, pswd, nonce)

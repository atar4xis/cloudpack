from pathlib import Path

import pytest

from cloudpack.vault import lock, unlock


@pytest.fixture
def _(monkeypatch):
    monkeypatch.setattr(
        "cloudpack.vault.validate_master_password", lambda _: b"password"
    )
    monkeypatch.setattr(
        "cloudpack.vault.derive_vault_key", lambda *_: b"key12345678901234"
    )
    monkeypatch.setattr("cloudpack.vault.encrypt", lambda data, _: b"ENC" + data)
    monkeypatch.setattr("cloudpack.vault.decrypt", lambda data, _: data[3:])


def test_lock_unlock(tmp_path, _):
    vault_path = Path(tmp_path / "vault")

    files_dir = vault_path / "files"
    chunks_dir = vault_path / "chunks"
    files_dir.mkdir(parents=True)
    chunks_dir.mkdir(parents=True)
    (vault_path / "vault.meta").write_bytes(b"{}")

    (files_dir / "a.txt").write_text("test content")
    (files_dir / "b/b.txt").parent.mkdir(parents=True)
    (files_dir / "b/b.txt").write_text("more test stuff")

    lock(vault_path)

    # files should be removed and chunks should exist
    assert not files_dir.exists()
    assert any(chunks_dir.iterdir())

    unlock(vault_path)

    # original content should be restored
    assert (files_dir / "a.txt").read_text() == "test content"
    assert (files_dir / "b/b.txt").read_text() == "more test stuff"

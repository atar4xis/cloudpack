from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from cloudpack.cli import cli


def test_vault_init(tmp_path):
    master_password = "My$3cureV4ultPa$$w0rd!"
    with patch("cloudpack.vault.getpass", return_value=master_password):
        runner = CliRunner()
        vault_path = tmp_path / "vault"
        result = runner.invoke(cli, ["init", str(vault_path)])

        assert result.exit_code == 0
        assert "vault initialized" in result.output
        assert vault_path.exists() and vault_path.is_dir()
        assert (vault_path / ".passwd").exists()

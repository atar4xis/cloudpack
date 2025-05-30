import random
import string
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from cloudpack.cli import cli


def test_vault_init():
    master_password = "My$3cureV4ultPa$$w0rd!"
    with patch("cloudpack.vault.getpass", return_value=master_password):
        runner = CliRunner()
        vault_path = f"vault{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"
        result = runner.invoke(cli, ["init", vault_path])

        assert result.exit_code == 0
        assert "vault initialized" in result.output
        assert Path(vault_path).exists() and Path(vault_path).is_dir()
        assert (Path(vault_path) / ".passwd").exists()

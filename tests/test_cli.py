from typer.testing import CliRunner

from libre_chat.__main__ import cli

runner = CliRunner()


def test_help():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_version():
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0


def test_build():
    result = runner.invoke(cli, ["build"])
    assert result.exit_code == 1


# def test_start():
#     result = runner.invoke(cli, ["start"])
#     assert result.exit_code == 0

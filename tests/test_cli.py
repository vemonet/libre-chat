from typer.testing import CliRunner

from libre_llm.__main__ import cli

runner = CliRunner()


def test_help():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


# def test_api():
#     result = runner.invoke(cli, [])
#     assert result.exit_code == 0

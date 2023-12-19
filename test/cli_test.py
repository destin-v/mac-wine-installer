from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_run():
    result = runner.invoke(app)

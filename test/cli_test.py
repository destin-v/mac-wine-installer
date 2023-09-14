from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


# def test_setup():
#     result1 = runner.invoke(app, ["setup-head", "--partition manycore"])
#     result2 = runner.invoke(app, ["setup-cpu", "--partition manycore"])
#     result3 = runner.invoke(app, ["setup-gpu", "--partition gaia"])

#     # assert "success" in result.output


def test_run():
    result = runner.invoke(app)

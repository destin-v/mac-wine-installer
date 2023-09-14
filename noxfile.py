"""
Nox creates a new virtual environment for each individual test.  Thus, it is important for to install all the packages needed for testing.  When using Nox, it will by default grab the current python version available in your environment and run testing with it.

Useful commands:

# Lists out all the available sessions
> nox --list

# Runs the session for pytest
> nox -s pytest

"""
import nox


@nox.session
def pytest(session):
    """Run PyTests."""

    session.run("poetry", "install")
    session.install("pytest")
    session.run("pytest", "-v")


@nox.session
def flake8(session):
    """Lint checking."""

    session.install("flake8")
    session.run("flake8")


@nox.session
def black(session):
    """Format with Black."""
    session.install("black")
    session.run("black")


@nox.session
def coverage(session):
    """Runs coverage pytests"""

    session.run("poetry", "install")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "html", "-d", "save/coverage")
    session.run("coverage", "report", "-m")


@nox.session
def profile(session):
    """Profiles your selected code using scalene."""

    session.run("poetry", "install")

    session.run(
        "scalene",
        "--outfile",
        "save/profile.html",
        "--html",
        "main.py",
        env={
            "LINES": "25",
            "COLUMNS": "200",
        },
    )


@nox.session
def documentation(session):
    """Generate automatic documentation."""

    session.run("poetry", "install")
    session.run("pdoc3", "--html", "src")

import datetime
import os.path
import subprocess

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from typing_extensions import Annotated


# Tagging tools
curr_time = datetime.datetime.now().strftime("%m-%d-%y_%H:%M:%S")
userid = os.getenv("USER")

# Typer application CLI
console = Console()
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="markdown",
    epilog="Author: William Li :sunglasses:",
)


@app.command(
    help=":mountain: **Setup** Wine for Mac OS.",
)
def setup(
    uninstall: Annotated[
        bool,
        typer.Option(help="uninstall wine"),
    ] = False,
    homebrew: Annotated[
        bool,
        typer.Option(help="install homebrew if not installed"),
    ] = True,
    xquartz: Annotated[
        bool,
        typer.Option(help="install xquartz if not installed"),
    ] = True,
    wine: Annotated[
        bool,
        typer.Option(help="install wine if not installed"),
    ] = True,
    config: Annotated[
        bool,
        typer.Option(help="open wine config"),
    ] = True,
):
    """Automatically setup WINE for MacOS.  THe user can pass in variables to overwrite the default parameters.

    Args:
        uninstall (Annotated[ bool, typer.Option, optional): Uninstall WINE. Defaults to "uninstall wine"), ]=False.
        homebrew (Annotated[ bool, typer.Option, optional): Will install homebrew if not detected in the user environment. Defaults to "install homebrew if not installed"), ]=True.
        xquartz (Annotated[ bool, typer.Option, optional): Will install XQuartz if not detected in environment. Defaults to "install xquartz if not installed"), ]=True.
        wine (Annotated[ bool, typer.Option, optional): Will install WINE if not detected in the environment. Defaults to "install wine if not installed"), ]=True.
        config (Annotated[ bool, typer.Option, optional): Will open WINE config. Defaults to "open wine config"), ]=True.
    """
    # Uninstaller
    if uninstall:
        uninstall_wine()
        return

    # Installer
    if homebrew:
        install_homebrew()
        update_homebrew()
    if xquartz:
        install_xquartz()
    if wine:
        install_wine()

    # Configure wine here
    if config:
        config_wine()

    # Printout
    print(Panel("[green]To install a windows application run: \n[bold black]$ wine64 <*.exe>"))


def check_func(command: str) -> bool:
    """Check if `command` is found in the user's environment path.

    Args:
        command (str): A command to execute in the user's environment.

    Returns:
        bool: Returns `True` if the command is found, else return `False.
    """
    check = subprocess.run(["which", command], capture_output=True, text=True)
    output = check.stdout

    check1 = "not found" in output
    check2 = output == ""

    if check1 or check2:
        return False
    else:
        return True


def uninstall_wine() -> None:
    """Uninstall WINE."""

    run_in_terminal(["brew", "uninstall", "--cask", "wine-devel"])
    run_in_terminal(["rm", "-rf", "$HOME/.wine"])
    print(":party_popper: [green]Uninstalled wine.")


def install_homebrew() -> None:
    """Installs Homebrew if it is not detected in the user's environment.

    Raises:
        ValueError: Raises an error if homebrew fails to install.
    """
    if check_func("brew"):
        print(":party_popper: [green]Homebrew detected!")
        return
    else:
        print(":boom: [orange]Homebrew not installed, beginning install...")
        run_in_terminal(
            [
                "/bin/bash",
                "src/scripts/install_homebrew.sh",
            ]
        )

        raise ValueError(
            "Ensure that Homebrew is properly setup with your shell and re-run installer."
        )


def update_homebrew() -> None:
    """Update existing Homebrew package."""

    print(":party_popper: [green]Updating Homebrew to latest...")
    run_in_terminal(["brew", "update"])


def install_xquartz() -> None:
    """Installs XQuartz if it is not detected in the user's environment."""

    if check_func("xquartz"):
        print(":party_popper: [green]xQuartz detected!")
        return
    else:
        print(":boom: [orange]xQuartz not installed, beginning install...")
        run_in_terminal(["brew", "install", "--cask", "xquartz"])


def install_wine() -> None:
    """Installs WINE if it is not detected in the user's environment."""

    if check_func("wine"):
        print(":party_popper: [green]Wine detected!")
        return
    else:
        print(":boom: [orange]Wine not installed, beginning install...")
        run_in_terminal(["brew", "tap", "homebrew/cask-versions"])
        run_in_terminal(["brew", "install", "--cask", "--no-quarantine", "wine-devel"])


def config_wine() -> None:
    """Open the WINE configuration tool."""

    run_in_terminal(["wine64", "winecfg"])


def run_in_terminal(command: list) -> None:
    """Runs a command in the terminal capturing the output.

    Args:
        command (list): A list of commands to run in the terminal.

    Raises:
        Exception: Command fails to execute.
    """
    results = subprocess.run(command)

    if results.returncode != 0:
        raise Exception(f"Invalid result: { results.returncode }, Error: {results}")

    if results.stdout is not None:
        print(results.stdout)


if __name__ == "__main__":
    app()

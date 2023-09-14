import typer
from typing_extensions import Annotated

import os
import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
import subprocess
import os.path


# Tagging tools
curr_time = datetime.datetime.now().strftime("%m-%d-%y_%H:%M:%S")
userid = os.getenv("USER")

# Typer application CLI
console = Console()
app = typer.Typer(rich_markup_mode="markdown")


@app.command(
    help=":mountain: **Setup** Wine for Mac OS.",
    epilog="Author: William Li :sunglasses:",
)
def setup(
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
    print(
        Panel(
            "[green]To install a windows application run: \n[bold black]$ wine64 <windows_executable_setup.exe>"
        )
    )


def check_func(command) -> bool:
    check = subprocess.run(["which", command], capture_output=True, text=True)
    output = check.stdout

    if "not found" in output:
        return False
    else:
        return True


def install_homebrew() -> None:
    if check_func("brew"):
        print(":party_popper: [green]Homebrew detected!")
        return
    else:
        print(":boom: [orange]Homebrew not installed, beginning install...")
        run_in_terminal(
            [
                "/bin/bash",
                "-c",
                '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            ]
        )


def update_homebrew() -> None:
    print(":party_popper: [green]Updating Homebrew to latest...")
    run_in_terminal(["brew", "update"])


def install_xquartz() -> None:
    if check_func("xquartz"):
        print(":party_popper: [green]xQuartz detected!")
        return
    else:
        print(":boom: [orange]xQuartz not installed, beginning install...")
        run_in_terminal(["brew", "install", "––cask", "xquartz"])


def install_wine() -> None:
    if check_func("wine"):
        print(":party_popper: [green]Wine detected!")
        return
    else:
        print(":boom: [orange]Wine not installed, beginning install...")
        run_in_terminal(["brew", "tap", "homebrew/cask-versions"])
        run_in_terminal(["brew", "install", "--cask", "--no-quarantine", "wine-devel"])


def config_wine() -> None:
    run_in_terminal(["wine64", "winecfg"])


def run_in_terminal(command: list) -> None:
    results = subprocess.run(command)

    if results.returncode != 0:
        raise Exception(f"Invalid result: { results.returncode }, Error: {results}")

    if results.stdout is not None:
        print(results.stdout)


if __name__ == "__main__":
    app()

from pathlib import Path

import click

try:
    from rich.console import Console

    rich_available = True
except ImportError:
    rich_available = False

from .init import init, init_steps


@click.command()
@click.argument("project_root", type=click.Path(exists=False))
def cli(project_root: str):
    project_root_path = Path(project_root)
    if rich_available:
        console = Console()
        with console.status(
            f"Initialising Kedro project in {project_root_path.absolute()}"
        ):
            for step_message in init_steps(project_root_path):
                console.log(step_message)
            console.log(
                "[green]:large_orange_diamond: Kedro project successfully initialised!"
            )
    else:
        click.echo(f"Initialising Kedro project in {project_root_path.absolute()}...")
        init(project_root_path)
        click.echo("\U0001f536 Kedro project successfully initialised!")

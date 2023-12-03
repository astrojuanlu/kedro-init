from pathlib import Path

import click

from .init import init


@click.command()
@click.argument("project_root", type=click.Path(exists=False))
def cli(project_root):
    init(Path(project_root))

# Register Console
import click
from pyucc import console, colors, symbols
from typing import List
import sys

import subcommands

color_grey = colors.chex("#303030", "foreground")

@click.group()
@click.pass_context
def cli(ctx):
    pass

# Add Commands
cli.add_command(subcommands.nginx)

if __name__ == "__main__":
    cli()
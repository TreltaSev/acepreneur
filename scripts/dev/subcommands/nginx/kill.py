import click
from pyucc import console, colors
import os

@click.command()
def kill():
    """
    Kills any nginx.exe processes
    """

    os.system("taskkill /f /im nginx.exe")

    console.done(f"{colors.vibrant_red}Killed {colors.vibrant_green}nginx")

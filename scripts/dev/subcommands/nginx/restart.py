import click
from pyucc import console, colors
import os

color_grey = colors.chex("#AAAAAA", "foreground")

@click.command()
def restart():
    """
    Restarts nginx
    """

    os.system("taskkill /f /im nginx.exe")

    os.chdir("C:/nginx")

    os.system("start nginx")

    console.done(f"{color_grey}Restarted {colors.vibrant_green}nginx")

import os
import subprocess
import click
from pyucc import console
from siblink import Config, __git__
from pathlib import Path
import datetime

# Subcommands
from .dump import dump
from .kill import kill
from .restart import restart


@click.group()
def nginx():
    """
    Runs development-time nginx logic, such as the automation of the nginx.conf file on dev
    """
    pass

nginx.add_command(dump)
nginx.add_command(kill)
nginx.add_command(restart)
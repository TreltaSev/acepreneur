# Register Console
import scripts.console
import click
from pyucc import console, colors, symbols
from bump.Handler import Handler
from typing import List
import sys

color_grey = colors.chex("#303030", "foreground")

def get_options() -> List[str]:
    buff: List[str] = []
    buff.append(f"\b{colors.vibrant_blue}Available Sections:{symbols.reset}\n")
    
    for sec in Handler.gather():
        _ind = ' ' * 3
        buff.append(f"\b{_ind}{color_grey}[{sec}]{symbols.reset}\n")
    buff.append(f"\b\n{colors.vibrant_blue}Try using: {color_grey}siblink run -- scripts/bump {colors.vibrant_violet}{list(Handler.gather())[0]}")
    buff.append(symbols.reset) 
    return buff 

@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('section', default="")
@click.argument('level', default="patch")
@click.option('-l', '--list', 'should_list', default=False, type=bool, is_flag=True, show_default=True, help="List Registered Sections")
def cli(ctx, section, level, should_list):

    if (should_list):
        console.info('', *get_options())
        return

    buff: List[str] = []
    # Handle no input
    if not section:
        buff.append("No \"section\" found in command\n")
        buff.extend(get_options())
        console.fail(*buff)
        return


    _call = Handler.get(section)

    if not _call:
        buff.append(f"Couldn't find logic for \"{type}\", check your spelling or register it\n")
        buff.extend(get_options())
        console.fail(*buff)
        return
    
    _call(level=level)


if __name__ == "__main__":
    cli()
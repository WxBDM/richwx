import click
import configparser
from rich.console import Console
import os

from .alerts import get_alerts
from .intro import intro
from .useragent import check_user_agent, set_user_agent, purge_user_agent, _get_useragent_info

# This is the common entry point, and is called when you type richwx into the console.
@click.group()
@click.pass_context
def cli(ctx):
    """A fun little CLI tool that utilizes the National Weather Service API to display
    weather data in the terminal."""
    
    # This will r/w the .ini file, which stores the useragent information needed for the
    # NWS API.
    configs = configparser.ConfigParser()
    path_to_ini_file = os.path.join(os.path.abspath("."), 'useragent.ini')
    
    ctx.obj = {'console' : Console(),
                'config' : configs,
                'user_agent' : _get_useragent_info(configs, path_to_ini_file),
                'path_to_ini_file' : path_to_ini_file
                }

# Add the commands here.
cli.add_command(intro)
cli.add_command(get_alerts)
cli.add_command(set_user_agent)
cli.add_command(purge_user_agent)
cli.add_command(check_user_agent)

if __name__ == '__main__':
    cli()
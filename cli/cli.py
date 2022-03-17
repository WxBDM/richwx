import click
from rich.console import Console
import os
import sys
sys.path.insert(0, os.path.abspath(".")) # guarentees that the path of this is added. Please work.

from cli.utils.handlers import UserAgentHandler

from cli.commands.alerts import alerts
from cli.commands.intro import intro
from cli.commands.useragent import user_agent_group

# This is the common entry point, and is called when you type richwx into the console.
@click.group()
@click.pass_context
def cli(ctx):
    """A fun little CLI tool that utilizes the National Weather Service API to display
    weather data in the terminal."""
        
    ctx.obj = {'console' : Console(),
                'user_agent' : UserAgentHandler(),
              }

# Add the commands here.
cli.add_command(intro)
cli.add_command(alerts)
cli.add_command(user_agent_group)

if __name__ == '__main__':
    cli()
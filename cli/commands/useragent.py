import click

@click.group(name = "auth")
def user_agent_group():
    """Sets metadata for NWS API maintainers.
    
    This is highly encouraged by the maintainers as a form of contacting you in the event of a security event were to occur.. 
    Outside of the header information that is sent to the API, this data is saved locally in a file.
    To purge this information, use `richwx auth purge`.
    
    See more details here: https://www.weather.gov/documentation/services-web-api"""
    pass


@user_agent_group.command('set')
@click.argument('contact', required = True, nargs = -1, type = str)
@click.pass_obj
def set_user_agent(obj, contact):
    """Sets contact information to be sent to the NWS API.
    """
    
    if isinstance(contact, tuple):
        contact = " ".join(contact)
    
    # extract the information from context.
    user_agent = obj['user_agent']
    console = obj['console']
    user_agent.set_contact(contact)
            
    console.print(f"\nUser agent contact info now set to: [blue]{contact}[/blue]")
    console.print(f"\nReminder: Only the NWS API maintainers will see this information!\n")

@user_agent_group.command(name = 'purge')
@click.pass_obj
def purge_user_agent(obj):
    """Purges the metadata information locally.
    """
    
    user_agent = obj['user_agent']
    user_agent.set_default_values()
    
    console = obj['console']  
    console.print(f"\n=> [green]PURGED[/] user agent information locally.\n")

@user_agent_group.command('check')
@click.pass_obj
def check_user_agent(obj):
    """Checks the current user agent information.
    """
    
    user_agent = obj['user_agent']
    console = obj['console']
    
    if user_agent.contact != 'NoneSet':
        console.print(f"\n=> Contact information to be sent to the API as metadata: [magenta]{user_agent.contact}\n")
    else:
        console.print(f"\n=> Contact information [blue]has not been set[/]. Set it using [reverse]richwx auth set\n")
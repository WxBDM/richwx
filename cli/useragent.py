import re
import click
import os
import sys

def _get_default_ini_values():
    """Returns default ini file values.

    Returns:
        dict: Information for default user agent ini files.
    """
    return {'applicationname' : 'RichWxTerminal',
            'contactinfo' : 'NoneSet'}

def _ini_file_does_not_exist(path):
    """Determines if the ini file does NOT exist.

    Args:
        path (string): The path to the ini file.

    Returns:
        bool: True if the file does exist, false otherwise.
    """
    if os.path.isfile(path):
        return False
    return True

def _get_useragent_info(configs, path_to_ini_file, return_if_new_file_was_created = False):
    """Gets the information from the user agent ini file.

    Args:
        config (configparser.ConfigParser): Used for I/O for the ini file.
        path_to_ini_file (str): The path to the ini file.
        return_if_new_file_was_created (bool, optional): Only checks to see if a new ini file was made. Defaults to False.

    Returns:
        bool/dict: dictionary containing the user agent info, otherwise true/false.
    """

    # in case it's not created, make a file.
    created_new_ini_file = False
    if _ini_file_does_not_exist(path_to_ini_file):
        with open(path_to_ini_file, 'w') as configfile:
            configs['UserAgent'] = _get_default_ini_values()
            configs.write(configfile)
            created_new_ini_file = True
    
    # If we only want to see if we created a new file with default info or not.
    if return_if_new_file_was_created:
        return created_new_ini_file
    
    # Get the user agent information from this ini file.
    configs.read(path_to_ini_file)
    user_agent = {'app_name' : configs['UserAgent']['applicationname'], 'contact' : configs['UserAgent']['contactinfo']}
    return user_agent

def check_if_user_agent_is_set(ctx):
    """Determines if the user agent is set. If not, then it will not show anything on the console.

    Args:
        config (configparser.ConfigParser): Used for parsing the ini file.
        path (str): Path to the ini file.
        rich_console (rich.console.Console): The rich console to print an alert.
    """
    config = ctx.obj['config']
    path = ctx.obj['path_to_ini_file']
    rich_console = ctx.obj['console']
    
    user_agent_info = _get_useragent_info(config, path)
    if user_agent_info['contact'] == "NoneSet":
        rich_console.print("=> [bold red]Attention:[/bold red] User Agent is not set. Be sure to set it running [underline]`richwx set-user-agent`[/underline].")
        sys.exit()

@click.group(name = "auth")
def user_agent_info():
    """Sets metadata for NWS API maintainers.
    
    This is required by the maintainers as a form of contacting you in the event of a security event. 
    Outside of the header information that is sent to the API, this data is saved locally in a file.
    To purge this information, use `richwx auth purge`.
    
    See more details here: https://www.weather.gov/documentation/services-web-api"""
    pass


@user_agent_info.command('set')
@click.argument('contact', required = True, nargs = -1, type = str)
@click.pass_context
def set_user_agent(ctx, contact):
    """Sets metadata to be sent to the NWS API.
    """
    
    if isinstance(contact, tuple):
        contact = " ".join(contact)
    
    # extract the information from context.
    config = ctx.obj['config']
    path_to_ini = ctx.obj['path_to_ini_file']
    
    # see if the ini file exists. If not, then create it.
    created_new_ini_file = _get_useragent_info(config, path_to_ini, return_if_new_file_was_created=True)
    
    # Read the ini file and set the new contact info.
    config.read(path_to_ini)
    config['UserAgent']['ContactInfo'] = contact
    with open(path_to_ini, 'w') as configfile:
        config.write(configfile)
    
    # Do console printing.
    console = ctx.obj['console']
    if created_new_ini_file:
        console.print(f"\n[red]Had to create new ini file.[/red]\n\tLocation: [underline green]{path_to_ini}[/underline green]")
        
    console.print(f"\nUser agent contact info now set to: [blue]{contact}[/blue]")
    console.print(f"\tReminder: Only the NWS API maintainers will see this information!\n")

@user_agent_info.command(name = 'purge')
@click.pass_obj
def purge_user_agent(obj):
    """Purges the metadata information locally.
    """
    
    config = obj['config']
    path_to_ini = obj['path_to_ini_file']
    console = obj['console']
    
    config.read(path_to_ini)
    config['UserAgent'] = _get_default_ini_values()
    with open(path_to_ini, 'w') as configfile:
        config.write(configfile)
        
    console.print(f"\n[green]PURGED[/green] user agent information locally.\n")

@user_agent_info.command('check')
@click.pass_obj
def check_user_agent(obj):
    """Checks the current user agent information.
    """
    
    user_agent = obj['user_agent']
    console = obj['console']
    
    contact = user_agent['contact'] 
    
    if contact == "NoneSet":
        console.print("\n=> [magenta underline]You have not set this value.[/] Set it through [reverse]richwx set-user-agent \[contact]\n")
    else:
        console.print(f"\nContact Information for user agent: [magenta]{contact}\n")
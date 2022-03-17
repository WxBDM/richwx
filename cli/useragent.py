import click
import os
from configparser import ConfigParser

class UserAgentHandler:
    
    """Class to handle user agent data and provide an interface for 
    functionality to see what's currently set.
    """
    
    info = ConfigParser()
    PATH_TO_FILE = os.path.join(os.path.abspath("."), 'useragent.ini')
    default_values = {'applicationname' : 'RichWxTerminal', 'contactinfo' : 'NoneSet'}
    
    def __init__(self):
        # If the file doesn't exist, then create a new one.
        if not self._file_exists():
            self.set_default_values()
        
        # Security concern: don't keep these values internal to the class. Just call the
        # _read method every time. Makes things easier :^)
    
    def _read(self):
        self.info.read(self.PATH_TO_FILE)
        return (self.info['UserAgent']['applicationname'], self.info['UserAgent']['contactinfo'])
    
    def set_contact(self, contact: str):
        if not isinstance(contact, str):
            print("When setting this information, you must pass in a string. Not setting.")
            return
        
        # Reset it to the default values. This handles the odd boundary case where the
        # file does exist, but there's no information.
        self.set_default_values()
        
        with open(self.PATH_TO_FILE, 'w') as configfile:
            self.info['UserAgent']['contactinfo'] = contact
            self.info.write(configfile)
    
    def set_default_values(self):
        with open(self.PATH_TO_FILE, 'w') as configfile:
            self.info['UserAgent'] = self.default_values
            self.info.write(configfile)
    
    def _file_exists(self):
        if os.path.isfile(self.PATH_TO_FILE):
            return True
        return False
    
    @property
    def peek_contact_info(self):
        return self._read()[1]

    @property
    def peek_app_name(self):
        # not sure why this would be used, but why not include it?
        return self._read()[0]

    def export_for_api_request(self) -> tuple:
        
        # If the file doesn't exist, then create a new one.
        if not self._file_exists():
            self.set_default_values()
        
        # The configparser class guarentees the output to be a string.
        return self._read()

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
    contact = user_agent.peek_contact_info
    
    if contact != 'NoneSet':
        console.print(f"\n=> Contact information to be sent to the API as metadata: [magenta]{contact}\n")
    else:
        console.print(f"\n=> Contact information [blue]has not been set[/]. Set it using [reverse]richwx auth set\n")
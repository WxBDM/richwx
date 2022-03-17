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
    
    def _file_exists(self):
        if os.path.isfile(self.PATH_TO_FILE):
            return True
        return False
    
    @property
    def contact(self):
        return self._read()[1]

    @property
    def app_name(self):
        return self._read()[0]
    
    @property
    def error_message(self) -> str:
        return "=> [red bold]Attention[/]: you have not set the contact information for this application. "\
            "The contact information can be set using [reversed]richwx auth set[/], and will [underline bold]only[/] "\
            "be seen by the API maintainers."
    
    def contact_is_set(self) -> bool:
        if self.contact == 'NoneSet':
            return False
        return True
    
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
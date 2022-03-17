import click
from datetime import datetime

from rich.progress import Progress
from rich.table import Table

from nwsapy import api_connector
from nwsapy.services.validation import valid_areas
from nwsapy.core.mapping import full_state_to_two_letter_abbreviation as fsta
from nwsapy.core.errors import DataValidationError

from cli.utils.alert_rich_strings import get_alert_object


@click.group('alerts')
def alerts():
    """Functionality for displaying NWS alerts."""
    pass


@alerts.command('state')
@click.argument('state', nargs = 1)
@click.option("--show-id", is_flag = True)
@click.pass_obj
def get_alerts(obj, state, show_id):
    """Displays a list of NWS alerts based upon the 2 letter state abbreviation (i.e. FL)"""

    console = obj['console']
    
    n_steps = 4
    steps_taken = 0

    with Progress() as progress:
        
        # Add a new task bar.
        task = progress.add_task('Validating input...', total = n_steps)
        if len(state) != 2:
            
            try:
                # full name to state abbreviation.
                state = fsta(state)
            except DataValidationError:
                console.print(f"\n=> [red bold]Attention:[/] {state} can not be abbreviated. Check spelling or provide a 2 letter abbreviation (i.e. FL, MA).\n")
                progress.update(task, advance = steps_taken, description = f'Unsuccessful data validation. See error above.')
                return
        
        state = state.upper()
        if state not in valid_areas():
            console.print(f"\n=> [red bold]Attention:[/] {state} is not a valid state.\n")
            progress.update(task, advance = steps_taken, description = f"Unsuccessful data validation. See error above.")
            return
        
        steps_taken += 1
        
        # validation happened, checking user agent.
        progress.update(task, advance = steps_taken, description = 'Checking User Agent...')
        user_agent = obj['user_agent']
        if not user_agent.contact_is_set:
            console.print(user_agent.error_message)
        api_connector.set_user_agent(user_agent.app_name, user_agent.contact)
        
        steps_taken += 1
        
        # User agent OK and set. Fetch the data.
        progress.update(task, advance = steps_taken, description = f"Getting alerts for {state}...")
        data = api_connector.get_active_alerts(area = state).to_dict()
        steps_taken += 1
        
        progress.update(task, advance = steps_taken, description = f"Creating table...")
        table = Table(title=f"Alerts for {state}, requested: {str(datetime.utcnow())} UTC", show_lines= True)
        if show_id:
            table.add_column("Alert ID", justify = 'center', min_width = 46)
        table.add_column("Alert Type", justify="center")
        table.add_column("Location", justify = 'center', max_width = 80)
        table.add_column("Issued", justify="center")
        table.add_column("Expires", justify = 'center')
        table.add_column("Sender", justify = 'center')
                
        def format_id(id):
            return id.replace('urn:oid:2.49.0.1.840.0.', '')
        
        # populate the table.
        for key_number in data.keys():
            counties = data[key_number]['areaDesc'].replace(';', ',')
            element = data[key_number]
            
            start_time = f"[magenta]{str(element['sent'])}".replace(" ", "\n")
            end_time = f"[yellow]{str(element['expires'])}".replace(" ", "\n")
            sender = element['sender_name']
            
            style = get_alert_object(element['event']) # returns an AlertStyle object.
            style.add_newline_after_emotes()

            if show_id:
                table.add_row(format_id(element['id']), style.to_string(), counties, start_time, end_time, sender)
            else:
                table.add_row(style.to_string(), counties, start_time, end_time, sender)
                
        steps_taken += 1
        
        # update the progress bars.
        progress.update(task, advance = steps_taken, description = f"Completed process!")
    
    # need 2 additional print statements here because the bar inteferes with it.
    console.print()
    console.print()
    console.print(table)


@alerts.command('id')
@click.argument('id', nargs = 1)
@click.pass_obj
def alert_id(obj, id):
    """Displays an alert information by its ID."""

    id = f'urn:oid:2.49.0.1.840.0.{id}'

    console = obj['console']
    
    user_agent = obj['user_agent']
    if not user_agent.contact_is_set:
        console.print(user_agent.error_message)
    api_connector.set_user_agent(user_agent.app_name, user_agent.contact)
    data = api_connector.get_alert_by_id(id).to_dict()[1]
    
    style = get_alert_object(data['event'])
    
    style_table = None
    if data['severity'] == 'Extreme':
        # Bolds the entire table.
        from rich.style import Style
        style_table = Style(bold = True)
    
    table = Table(show_lines=True, title = style.event_with_emotes, padding = (0, 0), style = style.color, width = 130, border_style = style_table)
    table.add_column("Information")
    table.add_column("Details")
    
    table.add_row("Headline", data['headline'])
    table.add_row("Details", data['description'])
    table.add_row("Location", data['areaDesc'])
    table.add_row("Instruction", data['instruction'] if data['instruction'] is not None else "N/A") # sometimes this is null.
    table.add_row("Sender", data['senderName'])
    table.add_row("Severity", data['severity'])
    table.add_row("Full ID", id)
    
    console.print()
    console.print(table)
    console.print()
        
    # ['@id', '@type', 'id', 'areaDesc', 'geocode', 'affectedZones', 'references', 'sent', 'effective', 'onset', 'expires', 
    # 'ends', 'status', 'messageType', 'category', 'severity', 'certainty', 'urgency', 'event', 'sender', 'senderName', 
    # 'headline', 'description', 'instruction', 'response', 'parameters', 'points', 'polygon', 'sent_utc', 'effective_utc',  
    # 'onset_utc', 'expires_utc', 'ends_utc', 'affected_zones', 'area_desc', 'message_type', 'sender_name']
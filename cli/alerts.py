import click
import time
from rich.progress import Progress
from rich.table import Table
from nwsapy import api_connector
from nwsapy.services.validation import valid_areas
from datetime import datetime
from .useragent import check_if_user_agent_is_set
    
def make_emoji_string(nws_warning):
    d = {'Red Flag Warning' : ':triangular_flag:\n[bright_magenta]Red Flag Warning',
         'Fire Weather Watch' : ':fire: :eyes:\n[misty_rose3]Fire Weather Watch',
         'Tornado Watch' : ':eyes: :tornado:\n[red]Tornado Watch',
         'Tornado Warning' : ':exclamation_mark: :tornado:\n[red bold]Tornado Warning',
         'Severe Thunderstorm Watch' : ':eyes: :high_voltage [yellow]Severe Thunderstorm Watch',
         'Severe Thunderstorm Warning' : ':exclamation_mark: :high_voltage:\n[yellow bold]Severe Thunderstorm Warning',
         'Hurricane Watch' : ':eyes: :cyclone: :water_wave:\n[magenta]Hurricane Watch',
         'Hurricane Warning' : ':exclamation_mark: :cyclone: :water_wave:\n[red bold]Hurricane Warning',
         'Tropical Storm Watch' : ':eyes: :cyclone:\n[blue]Tropical Storm Watch',
         'Tropical Storm Warning' : ':exclamation_mark: :cyclone:\n[blue bold]Tropical Storm Warning',
         'Flash Flood Watch' : ':eyes: :water_wave:\n[green]Flash Flood Watch',
         'Flash Flood Warning' : ':exclamation_mark: :water_wave:\n[green bold]Flash Flood Warning',
         'Rip Current Statement' : ':water_wave:\n[turquoise2]Rip Current Statement',
         'Freeze Watch' : ':cold_face: :eyes:\n[cyan]Freeze Watch',
         'Freeze Warning' : ':cold_face: :exclamation_mark:\n[blue1]Freeze Warning',
         'High Wind Watch' : ':wind_blowing_face: :eyes:\n[dark_goldenrod]High Wind Watch'
         }

    if nws_warning not in d:
        return nws_warning
    
    return d[nws_warning]

@click.command('alerts')
@click.argument('state', nargs = 1)
@click.pass_context
def get_alerts(ctx, state):
    """Displays a list of NWS alerts."""

    console = ctx.obj['console']
    
    n_steps = 4
    steps_taken = 0

    with Progress() as progress:
        
        # Add a new task bar.
        task = progress.add_task('Validating input...', total = n_steps)
        if len(state) != 2:
            console.print("\n=> [red bold]Attention:[/] You must have the state in its 2 letter abbreviation (ex: FL, MA, etc).\n")
            progress.update(task, advance = steps_taken, description = f"Unsuccessful data validation. See error above.")
            return
        
        state = state.upper()
        if state not in valid_areas():
            console.print(f"\n=> [red bold]Attention:[/] {state} is not a valid state.\n")
            progress.update(task, advance = steps_taken, description = f"Unsuccessful data validation. See error above.")
            return
        
        steps_taken += 1
        
        # validation happened, checking user agent.
        progress.update(task, advance = steps_taken, description = 'Checking User Agent...')
        check_if_user_agent_is_set(ctx)
        user_agent = ctx.obj['user_agent']
        api_connector.set_user_agent(user_agent['app_name'], user_agent['contact'])
        steps_taken += 1
        
        # User agent OK and set. Fetch the data.
        progress.update(task, advance = steps_taken, description = f"Getting alerts for {state}...")
        data = api_connector.get_active_alerts(area = state).to_dict()
        steps_taken += 1
        
        progress.update(task, advance = steps_taken, description = f"Creating table...")
        table = Table(title=f"Alerts for {state}, requested: {str(datetime.utcnow())} UTC", show_lines= True)
        table.add_column("Alert Type", justify="center")
        table.add_column("Location", justify = 'center')
        table.add_column("Issued", justify="center")
        table.add_column("Expires", justify = 'center')
        table.add_column("Sender", justify = 'center')
        
        for key_number in data.keys():
            counties = data[key_number]['areaDesc'].replace(';', ',')
            table.add_row(make_emoji_string(data[key_number]['event']), counties, f"[magenta]{str(data[key_number]['sent'])}", f"[yellow]{str(data[key_number]['expires'])}", data[key_number]['sender_name'])
        steps_taken += 1
    
        progress.update(task, advance = steps_taken, description = f"Completed!")
    
    # need 2 additional print statements here because the bar inteferes with it.
    console.print()
    console.print()
    console.print(table)
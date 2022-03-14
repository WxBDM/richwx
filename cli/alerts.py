import click
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel
from nwsapy import api_connector
from nwsapy.services.validation import valid_areas
from nwsapy.core.mapping import full_state_to_two_letter_abbreviation as fsta
from nwsapy.core.errors import DataValidationError
from datetime import datetime
from .useragent import check_if_user_agent_is_set

class AlertStyling:
    """Class to style alerts, allows for modularity."""
    
    def __init__(self, event, color, emojis, bolded = False, underline = False, italics = False, newline = False):
        self.emojis = emojis
        self.event = event
        self.color = color
        self.is_bolded = bolded
        self.is_underlined = underline
        self.is_italics = italics
        self.newline = newline
        
        self.event_with_emotes = " ".join(emojis) + " " + event
    
    def to_string(self):
        
        string = ''
        
        if len(self.emojis) != 0:
            for emote in self.emojis:
                string += f"{emote} "
            
            if self.newline:
                string += "\n"
        
        # i.e. [blue bold italics underline]
        opening_style_tag = f'[{self.color}'
        if self.is_bolded:
            opening_style_tag += ' bold'
        if self.is_italics:
            opening_style_tag += ' italics'
        if self.is_underlined:
            opening_style_tag += ' underline'
        opening_style_tag += ']'
        
        string += f"{opening_style_tag}{self.event}[/]"
                
        return string
    
    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()
    
    def add_bold(self):
        self.is_bolded = True
    
    def add_underline(self):
        self.is_underlined = True
    
    def add_italics(self):
        self.is_italics = True
    
    def add_newline_after_emotes(self):
        self.newline = True

def get_rich_style_string(nws_warning, bolded = False, italics = False, underline = False, newline = False):
    d = {'911 Telephone Outage': AlertStyling("911 Telephone Outage", "grey78", [":telephone_receiver:", ":man_police_officer:"]), 
        'Administrative Message': AlertStyling("Administrative Message", "grey78", [":pen:"]), 
        'Air Quality Alert': AlertStyling("Air Quality Alert", "grey50", [":mask:"]), 
        'Air Stagnation Advisory': AlertStyling("Air Stagnation Advisory", "gre50", [":mask:"]), 
        'Arroyo and Small Stream Flood Advisory': AlertStyling("Arroyo and Small Stream Flood Advisory", "medium_spring_green", [":water_wave:"]), 
        'Ashfall Advisory': AlertStyling("Ashfall Advisory", "grey39", [":volcano:"]), 
        'Ashfall Warning': AlertStyling("Ashfall Warning", "grey66", [":volcano:", ":exclamation_mark:"]), 
        'Avalanche Advisory': AlertStyling("Avalanche Advisory", "orange3", [":snow_capped_mountain:"]), 
        'Avalanche Watch': AlertStyling("Avalanche Watch", "bright_white", [":snow_capped_mountain:", ":eyes:"]), 
        'Avalanche Warning': AlertStyling("Avalanche Warning", "dodger_blue1", [":snow_capped_mountain:", ":exclamation_mark:"]), 
        'Beach Hazards Statement': AlertStyling("Beach Hazards Statement", "bright_white", [":question:", ":question:"]), 
        'Blizzard Watch': AlertStyling("Blizzard Watch", "bright_white", [":question:", ":question:"]),
        'Blizzard Warning': AlertStyling("Blizzard Warning", "bright_white", [":question:", ":question:"]), 
        'Blowing Dust Advisory': AlertStyling("Blowing Dust Advisory", "bright_white", [":question:", ":question:"]), 
        'Blowing Dust Warning': AlertStyling("Blowing Dust Warning", "bright_white", [":question:", ":question:"]), 
        'Blue Alert': AlertStyling("Blue Alert", "bright_white", [":question:", ":question:"]), 
        'Brisk Wind Advisory': AlertStyling("Brisk Wind Advisory", "bright_white", [":question:", ":question:"]), 
        'Child Abduction Emergency': AlertStyling("Child Abduction Emergency", "bright_white", [":loudly_crying_face:", ":megaphone:"]), 
        'Civil Danger Warning': AlertStyling("Civil Danger Warning", "bright_white", [":question:", ":question:"]), 
        'Civil Emergency Message': AlertStyling("Civil Emergency Message", "bright_white", [":question:", ":question:"]), 
        'Coastal Flood Advisory': AlertStyling("Coastal Flood Advisory", "bright_white", [":question:", ":question:"]), 
        'Coastal Flood Statement': AlertStyling("Coastal Flood Statement", "bright_white", [":question:", ":question:"]), 
        'Coastal Flood Warning': AlertStyling("Coastal Flood Warning", "bright_white", [":question:", ":question:"]), 
        'Coastal Flood Watch': AlertStyling("Coastal Flood Watch", "bright_white", [":question:", ":question:"]), 
        'Dense Fog Advisory': AlertStyling("Dense Fog Advisory", "bright_white", [":question:", ":question:"]), 
        'Dense Smoke Advisory': AlertStyling("Dense Smoke Advisory", "bright_white", [":question:", ":question:"]), 
        'Dust Advisory': AlertStyling("Dust Advisory", "bright_white", [":question:", ":question:"]), 
        'Dust Storm Warning': AlertStyling("Dust Storm Warning", "bright_white", [":question:", ":question:"]), 
        'Earthquake Warning': AlertStyling("Earthquake Warning", "bright_white", [":question:", ":question:"]), 
        'Evacuation Immediate': AlertStyling("Evacuation Immediate", "bright_white", [":question:", ":question:"]), 
        'Excessive Heat Watch': AlertStyling("Excessive Heat Watch", "bright_white", [":question:", ":question:"]), 
        'Extreme Cold Warning': AlertStyling("Extreme Cold Warning", "bright_white", [":question:", ":question:"]), 
        'Extreme Cold Watch': AlertStyling("Extreme Cold Watch", "bright_white", [":question:", ":question:"]), 
        'Extreme Fire Danger': AlertStyling("Extreme Fire Danger", "bright_white", [":question:", ":question:"]), 
        'Excessive Heat Warning': AlertStyling("Excessive Heat Warning", "bright_white", [":question:", ":question:"]), 
        'Extreme Wind Warning': AlertStyling("Extreme Wind Warning", "dark_orange", [":wind_blowing_face:", ":exclamation_mark:"]), 
        'Fire Warning': AlertStyling("Fire Warning", "orange4", [":fire:", ":excelamation_mark:"]), 
        'Fire Weather Watch': AlertStyling("Fire Weather Watch", "navajo_white1", [":fire:", ":eyes:"]), 
        'Flash Flood Statement': AlertStyling("Flash Flood Statement", "bright_white", [":question:", ":question:"]), 
        'Flash Flood Watch': AlertStyling("Flash Flood Watch", "bright_white", [":eyes:", ":water_wave:"]), 
        'Flash Flood Warning': AlertStyling("Flash Flood Warning", "bright_white", [":exclamation_mark:", ":water_wave:"]),
        'Flood Advisory': AlertStyling("Flood Advisory", "bright_white", [":question:", ":question:"]), 
        'Flood Statement': AlertStyling("Flood Statement", "bright_white", [":question:", ":question:"]), 
        'Flood Warning': AlertStyling("Flood Warning", "bright_green", [":exclamation_mark:", ":water_wave:"]), 
        'Flood Watch': AlertStyling("Flood Watch", "bright_white", [":question:", ":question:"]), 
        'Freeze Warning': AlertStyling("Freeze Warning", "medium_purple4", [":cold_face:", ":exclamation_mark:"]), 
        'Freeze Watch': AlertStyling("Freeze Watch", "cyan1", [":cold_face:", ":eyes:"]), 
        'Freezing Fog Advisory': AlertStyling("Freezing Fog Advisory", "bright_white", [":question:", ":question:"]), 
        'Freezing Spray Advisory': AlertStyling("Freezing Spray Advisory", "bright_white", [":question:", ":question:"]), 
        'Frost Advisory': AlertStyling("Frost Advisory", "cornflower_blue", [":cold_face:"]), 
        'Gale Warning': AlertStyling("Gale Warning", "bright_white", [":question:", ":question:"]), 
        'Gale Watch': AlertStyling("Gale Watch", "bright_white", [":question:", ":question:"]), 
        'Hard Freeze Watch': AlertStyling("Hard Freeze Watch", "bright_white", [":question:", ":question:"]), 
        'Hard Freeze Warning': AlertStyling("Hard Freeze Warning", "bright_white", [":question:", ":question:"]), 
        'Hazardous Materials Warning': AlertStyling("Hazardous Materials Warning", "bright_white", [":question:", ":question:"]), 
        'Hazardous Seas Warning': AlertStyling("Hazardous Seas Warning", "bright_white", [":question:", ":question:"]), 
        'Hazardous Seas Watch': AlertStyling("Hazardous Seas Watch", "bright_white", [":question:", ":question:"]), 
        'Hazardous Weather Outlook': AlertStyling("Hazardous Weather Outlook", "bright_white", [":question:", ":question:"]), 
        'Heat Advisory': AlertStyling("Heat Advisory", "bright_white", [":question:", ":question:"]), 
        'Heavy Freezing Spray Watch': AlertStyling("Heavy Freezing Spray Watch", "bright_white", [":question:", ":question:"]), 
        'High Surf Warning': AlertStyling("High Surf Warning", "bright_white", [":person_surfing:", ":exclamation_mark:"]), 
        'High Surf Advisory': AlertStyling("High Surf Advisory", "medium_orchid", [":person_surfing:"]), 
        'High Wind Watch': AlertStyling("High Wind Watch", "dark_goldenrod", [":wind_blowing_face:", ":eyes:"]), 
        'High Wind Warning': AlertStyling("High Wind Warning", "bright_white", [":question:", ":question:"]), 
        'Hurricane Force Wind Watch': AlertStyling("Hurricane Force Wind Watch", "bright_white", [":question:", ":question:"]), 
        'Hurricane Force Wind Warning': AlertStyling("Hurricane Force Wind Warning", "bright_white", [":question:", ":question:"]), 
        'Hurricane Local Statement': AlertStyling("Hurricane Local Statement", "bright_white", [":question:", ":question:"]), 
        'Hurricane Watch': AlertStyling("Hurricane Watch", "magenta", [":eyes:", ":cyclone:", ":water_wave:"]), 
        'Hurricane Warning': AlertStyling("Hurricane Warning", "red", [":exclamation_mark:", ":cyclone:", ":water_wave:"]), 
        'Hydrologic Advisory': AlertStyling("Hydrologic Advisory", "bright_white", [":question:", ":question:"]), 
        'Hydrologic Outlook': AlertStyling("Hydrologic Outlook", "light_green", []), 
        'Ice Storm Warning': AlertStyling("Ice Storm Warning", "bright_white", [":question:", ":question:"]), 
        'Lake Effect Snow Watch': AlertStyling("Lake Effect Snow Watch", "bright_white", [":question:", ":question:"]), 
        'Lake Effect Snow Warning': AlertStyling("Lake Effect Snow Warning", "bright_white", [":question:", ":question:"]), 
        'Lake Wind Advisory': AlertStyling("Lake Wind Advisory", "tan", [":fish:", ":wind_blowing_face:"]), 
        'Lakeshore Flood Advisory': AlertStyling("Lakeshore Flood Advisory", "bright_white", [":question:", ":question:"]),
        'Lakeshore Flood Statement': AlertStyling("Lakeshore Flood Statement", "bright_white", [":question:", ":question:"]), 
        'Lakeshore Flood Warning': AlertStyling("Lakeshore Flood Warning", "bright_white", [":question:", ":question:"]),
        'Lakeshore Flood Watch': AlertStyling("Lakeshore Flood Watch", "bright_white", [":question:", ":question:"]),
        'Law Enforcement Warning': AlertStyling("Law Enforcement Warning", "bright_white", [":question:", ":question:"]), 
        'Local Area Emergency': AlertStyling("Local Area Emergency", "bright_white", [":question:", ":question:"]), 
        'Low Water Advisory': AlertStyling("Low Water Advisory", "bright_white", [":question:", ":question:"]), 
        'Marine Weather Statement': AlertStyling("Marine Weather Statement", "bright_white", [":question:", ":question:"]),
        'Nuclear Power Plant Warning': AlertStyling("Nuclear Power Plant Warning", "bright_white", [":question:", ":question:"]),
        'Radiological Hazard Warning': AlertStyling("Radiological Hazard Warning", "bright_white", [":question:", ":question:"]), 
        'Red Flag Warning': AlertStyling("Red Flag Warning", "bright_magenta", [":triangular_flag:"]), 
        'Rip Current Statement': AlertStyling("Rip Current Statement", "medium_turquoise", [":water_wave:"]), 
        'Severe Thunderstorm Watch': AlertStyling("Severe Thunderstorm Watch", "yellow", [":eyes:", ":zap:"]),
        'Severe Thunderstorm Warning': AlertStyling("Severe Thunderstorm Warning", "yellow", [":exclamation_mark:", ":zap:"]), 
        'Severe Weather Statement': AlertStyling("Severe Weather Statement", "bright_white", [":question:", ":question:"]), 
        'Shelter In Place Warning': AlertStyling("Shelter In Place Warning", "bright_white", [":question:", ":question:"]), 
        'Short Term Forecast': AlertStyling("Short Term Forecast", "bright_white", [":question:", ":question:"]), 
        'Small Craft Advisory': AlertStyling("Small Craft Advisory", "bright_white", [":question:", ":question:"]),
        'Small Craft Advisory For Hazardous Seas': AlertStyling("Small Craft Advisory For Hazardous Seas", "bright_white", [":question:", ":question:"]), 
        'Small Craft Advisory for Rough Bar': AlertStyling("Small Craft Advisory for Rough Bar", "bright_white", [":question:", ":question:"]), 
        'Small Craft Advisory for Winds': AlertStyling("Small Craft Advisory for Winds", "bright_white", [":question:", ":question:"]), 
        'Small Stream Flood Advisory': AlertStyling("Small Stream Flood Advisory", "bright_white", [":question:", ":question:"]), 
        'Snow Squall Warning': AlertStyling("Snow Squall Warning", "bright_white", [":question:", ":question:"]), 
        'Special Marine Warning': AlertStyling("Special Marine Warning", "bright_white", [":question:", ":question:"]), 
        'Special Weather Statement': AlertStyling("Special Weather Statement", "misty_rose1", [":double_exclamation_mark:"]), 
        'Storm Warning': AlertStyling("Storm Warning", "bright_white", [":question:", ":question:"]), 
        'Storm Surge Warning': AlertStyling("Storm Surge Warning", "bright_white", [":question:", ":question:"]), 
        'Storm Surge Watch': AlertStyling("Storm Surge Watch", "bright_white", [":question:", ":question:"]),
        'Storm Watch': AlertStyling("Storm Watch", "bright_white", [":question:", ":question:"]),
        'Test': AlertStyling("Test", "bright_white", [":question:", ":question:"]), 
        'Tornado Warning': AlertStyling("Tornado Warning", "red", [":exclamation_mark:", ":tornado:"]),
        'Tornado Watch': AlertStyling("Tornado Watch", "red", [":eyes:", ":tornado:"]), 
        'Tropical Depression Local Statement': AlertStyling("Tropical Depression Local Statement", "bright_white", [":question:", ":question:"]), 
        'Tropical Storm Local Statement': AlertStyling("Tropical Storm Local Statement", "bright_white", [":question:", ":question:"]), 
        'Tropical Storm Watch': AlertStyling("Tropical Storm Watch", "blue", [":eyes:", ":cyclone:"]), 
        'Tropical Storm Warning': AlertStyling("Tropical Storm Warning", "blue", [":exclamation_mark:", ":cyclone:"]),
        'Tsunami Advisory': AlertStyling("Tsunami Advisory", "bright_white", [":question:", ":question:"]), 
        'Tsunami Warning': AlertStyling("Tsunami Warning", "orange_red1", [":water_wave:", ":exclamation_mark:", ":exclamation_mark:"]), 
        'Tsunami Watch': AlertStyling("Tsunami Watch", "bright_white", [":question:", ":question:"]), 
        'Typhoon Local Statement': AlertStyling("Typhoon Local Statement", "bright_white", [":question:", ":question:"]), 
        'Urban and Small Stream Flood Advisory': AlertStyling("Urban and Small Stream Flood Advisory", "bright_white", [":question:", ":question:"]),
        'Volcano Warning': AlertStyling("Volcano Warning", "bright_white", [":question:", ":question:"]), 
        'Wind Advisory': AlertStyling("Wind Advisory", "bright_white", [":question:", ":question:"]), 
        'Wind Chill Advisory': AlertStyling("Wind Chill Advisory", "bright_white", [":question:", ":question:"]), 
        'Wind Chill Watch': AlertStyling("Wind Chill Watch", "bright_white", [":question:", ":question:"]),
        'Wind Chill Warning': AlertStyling("Wind Chill Warning", "bright_white", [":question:", ":question:"]),
        'Winter Weather Advisory': AlertStyling("Winter Weather Advisory", "slate_blue1", [":snowflake:"]), 
        'Winter Storm Watch': AlertStyling("Winter Storm Watch", "bright_white", [":snowflake:", ":eyes:"]),
        'Winter Storm Warning': AlertStyling("Winter Storm Warning", "hot_pink", [":cold_face:", ":snowflake:", ":exclamation_mark:"])
    }
    
    # Unlikely to happen, but just in case.
    if nws_warning not in d.keys():
        return nws_warning
    
    # extract the alert.
    alert = d[nws_warning]
    
    # Add additional styling.
    if bolded:
        alert.add_bold()
    if italics:
        alert.add_italics()
    if underline:
        alert.add_italics()
    if newline:
        alert.add_newline_after_emotes()
    
    # return the AlertStyling object.
    return alert

@click.group('alerts')
def alerts():
    """Functionality for displaying NWS alerts."""
    pass

@alerts.command('state')
@click.argument('state', nargs = 1)
@click.option("--show-id", is_flag = True)
@click.pass_context
def get_alerts(ctx, state, show_id):
    """Displays a list of NWS alerts based upon the 2 letter state abbreviation (i.e. FL)"""

    console = ctx.obj['console']
    
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
        table.add_column("Location", justify = 'center', max_width = 80)
        table.add_column("Issued", justify="center")
        table.add_column("Expires", justify = 'center')
        table.add_column("Sender", justify = 'center')
        if show_id:
            table.add_column("Alert ID", justify = 'center', min_width = 46)
        
        table_update = progress.add_task('Populating table...', total = len(data))
        
        def format_id(id):
            return id.replace('urn:oid:2.49.0.1.840.0.', '')
        
        # populate the table.
        for key_number in data.keys():
            counties = data[key_number]['areaDesc'].replace(';', ',')
            element = data[key_number]
            
            start_time = f"[magenta]{str(element['sent'])}".replace(" ", "\n")
            end_time = f"[yellow]{str(element['expires'])}".replace(" ", "\n")
            sender = element['sender_name']
            
            style = get_rich_style_string(element['event'])
            style.add_newline_after_emotes()

            if show_id:
                table.add_row(style.to_string(), counties, start_time, end_time, sender, format_id(element['id']))
            else:
                table.add_row(style.to_string(), counties, start_time, end_time, sender)
                
            progress.update(table_update, advance = 1)
        steps_taken += 1
        
        # update the progress bars.
        progress.update(table_update, description = "Table populated successfully.")
        progress.update(task, advance = steps_taken, description = f"Completed process!")
    
    # need 2 additional print statements here because the bar inteferes with it.
    console.print()
    console.print()
    console.print(table)


@alerts.command('id')
@click.argument('id', nargs = 1)
@click.pass_context
def alert_id(ctx, id):
    """Displays an alert information by its ID."""
    
    check_if_user_agent_is_set(ctx)

    id = f'urn:oid:2.49.0.1.840.0.{id}'

    user_agent = ctx.obj['user_agent']
    console = ctx.obj['console']

    api_connector.set_user_agent(user_agent['app_name'], user_agent['contact'])
    data = api_connector.get_alert_by_id(id).to_dict()[1]
    
    style = get_rich_style_string(data['event'])
    
    table = Table(show_lines=True, title = style.event_with_emotes, padding = (1, 1), style = style.color, width = 130)
    table.add_column("Information")
    table.add_column("Details")
    
    table.add_row("Sender", data['senderName'])
    table.add_row("Headline", data['headline'])
    table.add_row("Details", data['description'])
    table.add_row("Location", data['areaDesc'])
    table.add_row("Severity", data['severity'])
    table.add_row("Full ID", id)
    
    console.print()
    console.print(table)
    console.print()
        
    # ['@id', '@type', 'id', 'areaDesc', 'geocode', 'affectedZones', 'references', 'sent', 'effective', 'onset', 'expires', 
    # 'ends', 'status', 'messageType', 'category', 'severity', 'certainty', 'urgency', 'event', 'sender', 'senderName', 
    # 'headline', 'description', 'instruction', 'response', 'parameters', 'points', 'polygon', 'sent_utc', 'effective_utc', 
    # 'onset_utc', 'expires_utc', 'ends_utc', 'affected_zones', 'area_desc', 'message_type', 'sender_name']
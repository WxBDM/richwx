
def get_alert_object(alert: str):
    """Gets the AlertStyling object at the specified alert.

    Args:
        alert (str): The alert that's kicked back from the API.

    Returns:
        AlertStyling: An AlertStyling object to style the specified alert.
    """
    if alert not in ALERTS.keys():
        # return an alertstyling object to keep consistent.
        # TODO: how should this be handled in the future? only devs should see this.
        return AlertStyling('Not Found', 'red', [])
    
    return ALERTS[alert]

class AlertStyling:
    """Class to style alerts, allows for modularity."""
    
    # Default styling
    is_bolded = False
    is_underlined = False
    is_italics = False
    newline = False
    
    def __init__(self, event: str, color: str, emojis: list):
        self.emojis = emojis
        self.event = event
        self.color = color
        
        self.event_with_emotes = " ".join(emojis) + " " + event
    
    def to_string(self):
    
        string = ''
        
        # i.e. [blue bold italics underline]
        opening_style_tag = f'[{self.color}'
        if self.is_bolded: opening_style_tag += ' bold'
        if self.is_italics: opening_style_tag += ' italics'
        if self.is_underlined: opening_style_tag += ' underline'
        opening_style_tag += ']'
        
        string += f"{opening_style_tag}{self.event}[/]"
        
        # if there's no emotes, there's no need for a newline.
        if all([self.newline, len(self.emojis) != 0]): 
            string += "\n"
        
        for emote in self.emojis:
            string += f"{emote} "
                
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

# TODO: Finish this out. Lots of manual work. Huge timesink.
# Need to compare standard colors (https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors)
#   with NWS colors (https://www.weather.gov/help-map), and determine closest one.
#   Bright side: whoever does this gets to choose the emotes! :D
# It's like this for modularity purposes. The color can be re-used, and the emotes are be the same for the specific alert.
ALERTS = {'911 Telephone Outage': AlertStyling("911 Telephone Outage", "grey78", [":telephone_receiver:", ":man_police_officer:"]), 
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
    'High Wind Warning': AlertStyling("High Wind Warning", "light_goldenrod3", [":wind_blowing_face:", ":wind_blowing_face:", ":wind_blowing_face:"]), 
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
    'Severe Thunderstorm Warning': AlertStyling("Severe Thunderstorm Warning", "bright_yellow", [":exclamation_mark:", ":zap:"]), 
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
    'Wind Advisory': AlertStyling("Wind Advisory", "tan", [":wind_blowing_face:"]), 
    'Wind Chill Advisory': AlertStyling("Wind Chill Advisory", "bright_white", [":question:", ":question:"]), 
    'Wind Chill Watch': AlertStyling("Wind Chill Watch", "bright_white", [":question:", ":question:"]),
    'Wind Chill Warning': AlertStyling("Wind Chill Warning", "bright_white", [":question:", ":question:"]),
    'Winter Weather Advisory': AlertStyling("Winter Weather Advisory", "slate_blue1", [":snowflake:"]), 
    'Winter Storm Watch': AlertStyling("Winter Storm Watch", "bright_white", [":snowflake:", ":eyes:"]),
    'Winter Storm Warning': AlertStyling("Winter Storm Warning", "hot_pink", [":cold_face:", ":snowflake:", ":exclamation_mark:"])
}
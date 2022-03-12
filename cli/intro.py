from rich.table import Table
import click

@click.command()
@click.pass_context
def intro(ctx):
    """Provides an introduction to ensure that the CLI works.
    """
    console = ctx.obj['console']
    console.print()
    
    title = ':tornado: :high_voltage::snowflake: [bold italic][red]Welcome[/] [green]to[/] \
[blue]RichWx[/][/] :wind_blowing_face: :sun_behind_rain_cloud: :thermometer:'
    
    content = "\nThis package utilizes Rich, NWSAPy, and Click to provide a way to get \
National Weather Service data through the CLI!\n\nThis is designed to be a for fun project. There are no plans \
on developing this further, but if there's enough community support, it will be considered.\n"

    console.rule(title)
    console.print(content)
    console.print()

    alerts_sample_table = Table(title = '== SAMPLE ALERTS, NOT REAL ==\n', show_lines= True, show_edge=False)
    
    alerts_sample_table.add_column("Alert Type", justify="center")
    alerts_sample_table.add_column("Location", justify = 'center')
    alerts_sample_table.add_column("Issued", justify="center")
    alerts_sample_table.add_column("Expires", justify = 'center')
    alerts_sample_table.add_column("Sender", justify = 'center')

    alerts_sample_table.add_row(":water_wave:[green]Flood Warning (FAKE)[/]", "Jefferson, Cliff", "1/1/2021 11:19AM EST", "1/1/2021 5:30PM EST", "It's a mystery...")
    alerts_sample_table.add_row(":cloud_with_tornado: [red]Tornado (FAKE)[/]", "Alachua", "1/1/2021 11:19AM EST", "1/1/2021 5:30PM EST", "Another mystery.")
    alerts_sample_table.add_row(":hamburger: Intern Roy missed slider happy hour ", "Nearby Arby's", "12/16/2021 4:00PM", "When he doesn't miss slider happy hour", "NWS Podunk")
    
    console.rule("Sample Alert Table")
    console.print("\nBy running `richwx alerts`, you'll get a table with the alerts based upon the area (state) you pass in. This is what a table would look like:")
    console.print(alerts_sample_table)
    
    # put some padding at the bottom.
    console.print()
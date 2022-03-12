import click
    
@click.command('alerts')
@click.argument('state', nargs = 1)
@click.pass_context
def get_alert_by_state(ctx, state):
    """Gets the alerts by the state."""
    
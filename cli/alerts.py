import click
from .useragent import check_if_user_agent_is_set
    
@click.command('alerts')
@click.argument('state', nargs = 1)
@click.pass_context
def get_alerts(ctx, state):
    """Displays a list of NWS alerts."""
    check_if_user_agent_is_set(ctx)
    
    print(state)
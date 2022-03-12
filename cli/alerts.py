import click
from nwsapy import api_connector
# from .useragent import check_if_user_agent_is_set, _get_useragent_info
    
@click.command('alerts')
@click.argument('state', nargs = 1)
@click.pass_context
def get_alerts(ctx, state):
    """Displays a list of NWS alerts."""
    
    
    # check_if_user_agent_is_set(ctx)
    # console = ctx.obj['console']
    
    # if len(state) != 2:
    #     console.print("=> [red bold]Attention:[/] You must have the state in its 2 letter abbreviation (ex: FL, MA, etc).\n")
    #     return
    
    # user_agent = _get_useragent_info(ctx)
    # api_connector.set_user_agent(user_agent['app_name'], user_agent['contact'])
    # data = api_connector.get_active_alerts(area = state)
    # print(data)
    
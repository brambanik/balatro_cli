import click
from client import health, rpc

@click.group()
def cli():
    """Balatro CLI client."""
    pass

@cli.command()
def healthcheck():
    """Check if the BalatroBot server is alive."""
    server_health = health()
    click.echo(server_health)

@cli.command()
@click.option("--deck", required=True)
@click.option("--stake", required=True)
def start(deck, stake):
    """Start a new run with a specific deck and stake."""
    result = rpc("start", {"deck": deck.upper(), "stake": stake.upper()})
    click.echo("Run started: ")
    click.echo(result)

@cli.command()
def shop():
    rpc("shop")




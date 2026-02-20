import click
from client import health, rpc
import pretty

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
    data = rpc("start", {"deck": deck.upper(), "stake": stake.upper()})
    pretty.header("New Run")
    pretty.kv(data, ["deck", "stake"])

@cli.command()
def shop():
    data = rpc("gamestate")
    pretty.display_shop(data)

@cli.command()
@click.argument("cards", required=True)
def play(cards):
    try:
        indices = [int(x.strip()) for x in cards.split(",")]
        rpc("play", {"cards": indices}, timeout = 30.0)
    except RuntimeError as e:
        click.echo("You are currently not able to select a hand.")

@cli.command()
@click.argument("cards", required=True)
def discard(cards):
    try:
        indices = [int(x.strip()) for x in cards.split(",")]
        rpc("discard", {"cards": indices}, timeout = 30.0)
    except RuntimeError as e:
        click.echo("You are currently not able to select a hand.")

# displays the current state
@cli.command()
def state():
    data = rpc("gamestate")
    click.echo("You are currently in ", nl = False)
    click.secho(data["state"], fg="yellow")

@cli.command()
def hand():
    data = rpc("gamestate")
    pretty.display_cards(data)

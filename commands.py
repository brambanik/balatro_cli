import click
from client import health, rpc
import pretty

@click.group()
def cli():
    """Balatro CLI client."""
    pass


# ACTIONS

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
def select():
    rpc("select")

@cli.command()
def skip():
    rpc("skip")

@cli.command()
def cashout():
    rpc("cash_out")

@cli.command()
def leave():
    rpc("next_round")

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

@cli.command()
@click.argument("item_type", required=True)
@click.argument("item", required=True)
def buy(item_type, item):
    try:
        item_id = int(item)
        print(item_type.upper())
        print(item_id)
        rpc("buy", {f"{item_type}":item_id}, timeout = 30.0)
    except RuntimeError as e:
        click.echo("You can't buy that.")


@cli.command()
@click.argument("choice", required=True)
@click.argument("targets", required=False)
def pick(choice, targets):
    if choice == "skip":
        rpc("pack",{"skip":True})
    if targets is None:
        rpc("pack",{"card":int(choice)}, timeout=30.0)
    else:
        target_indices = [int(x.strip(",")) for x in targets]
        rpc("pack",{"card":int(choice), "targets":target_indices})

# DEBUG COMMANDS


# DISPLAY / VISUALS

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

@cli.command()
def shop():
    data = rpc("gamestate")
    pretty.display_shop(data)

import click
from typing import Any

# General get function
def _get(d: dict, path:str, default: Any = "") -> Any:
    cur: Any = d
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

# Display a header
def header(title: str):
    click.echo(click.style(f"\n== {title} ==", bold=True))

# Display data specified by key list
def kv(data: dict[str, Any], keys: list[str]):
    for k in keys:
        if k in data:
            click.echo(f"{click.style(k + ':', bold=True)} {data[k]}")

def display_shop(data: dict):
    click.clear()
    item_count = 0
    header("Shop")
    click.echo("Current Balance: ", nl=False)
    click.secho(f"${data.get("money")}", fg="green")
    cards = data.get("shop",[]).get("cards", [])
    packs = data.get("packs",[]).get("cards",[])
    vouchers = data.get("vouchers",[]).get("cards",[])
    click.echo(click.style("\n-> Jokers", bold=True))
    for c in cards:
        click.echo(f"{item_count} :: ${c.get("cost",[]).get("buy",[])} -- {c.get("label",[])}: {c.get("value",[]).get("effect",[])}")
        item_count += 1
    click.echo(click.style("\n-> Packs", bold=True))
    for p in packs:
        click.echo(f"{item_count} :: ${p.get("cost",[]).get("buy",[])} -- {p.get("label",[])}: {p.get("value",[]).get("effect",[])}")
        item_count += 1
    click.echo(click.style("\n-> Vouchers", bold=True))
    for v in vouchers:
        click.echo(f"{item_count} :: ${v.get("cost",[]).get("buy",[])} -- {v.get("label",[])}: {v.get("value",[]).get("effect",[])}")
        item_count += 1
# Fallback function for basic json display
def fallback(data: Any):
    import json
    click.echo(json.dumps(data, indent=2, sort_keys=True))

def display_cards(data: dict):
    header("Hand")
    cards = data.get("hand", {}).get("cards", {})
    
    count = 0
    for c in cards:
        click.secho(f"{count:02d} ", bold = True, nl = False)
        count += 1
    click.echo()
    for c in cards:
        v = c.get("value",{})
        click.echo(f"{v.get('suit')}{v.get('rank')} ", nl = False)

    click.echo()
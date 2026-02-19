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
    header("Shop")
    click.echo("Current Balance: ", nl=False)
    click.secho(f"${data.get("money")}", fg="green")
    cards = data.get("shop",[]).get("cards", [])
    packs = data.get("packs",[]).get("cards",[])
    vouchers = data.get("vouchers",[]).get("cards",[])
    click.echo(click.style("\n-> Jokers", bold=True))
    for c in cards:
        click.echo(f"${c.get("cost",[]).get("buy",[])} -- {c.get("label",[])}: {c.get("value",[]).get("effect",[])}")
    click.echo(click.style("\n-> Packs", bold=True))
    for p in packs:
        click.echo(f"${p.get("cost",[]).get("buy",[])} -- {p.get("label",[])}: {p.get("value",[]).get("effect",[])}")
    click.echo(click.style("\n-> Vouchers", bold=True))
    for v in vouchers:
        click.echo(f"${v.get("cost",[]).get("buy",[])} -- {v.get("label",[])}: {v.get("value",[]).get("effect",[])}")

# Fallback function for basic json display
def fallback(data: Any):
    import json
    click.echo(json.dumps(data, indent=2, sort_keys=True))

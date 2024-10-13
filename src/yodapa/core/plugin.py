import sqlite3

import typer
from rich import print
from rich.table import Table

from yodapa.core.util import _refresh_plugins, get_plugin_list, get_db_connection

PROTECTED_PLUGINS = ["config", "plugin"]

app = typer.Typer(help="Commands to manage plugins")


############################################
############### Commands ###################
############################################

@app.command(name="list")
def list_plugins():
    """List all available plugins"""
    rows = get_plugin_list()

    if not rows:
        print("[yellow] No plugins found.[/]")
        return

    table = Table(title="Yoda Plugins")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Enabled")

    for key, value in rows:
        table.add_row(key, "[green]Yes[/]" if value == 1 else "[red]No[/]")

    print(table)


@app.command(name="enable")
def enable_plugin(name: str):
    """Enable a plugin"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, enabled FROM plugins WHERE name = ?", (name,))
        rows = cursor.fetchone()

        if not rows:
            print(f"[red] Plugin {name} not found.[/]")
            return

        cursor.execute("UPDATE plugins SET enabled=TRUE WHERE name = ?", (name,))
        conn.commit()
        print(f"[green] Enabled plugin {name}.[/]")

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="disable")
def disable_plugin(name: str):
    """Disable a plugin"""
    if name in PROTECTED_PLUGINS:
        print(f"[italic]{name}[/] [red]is an internal plugin that cannot be disabled[/]")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, enabled FROM plugins WHERE name = ?", (name,))
        rows = cursor.fetchone()

        if not rows:
            print(f"[red] Plugin {name} not found.[/]")
            return

        cursor.execute("UPDATE plugins SET enabled=FALSE WHERE name = ?", (name,))
        conn.commit()
        print(f"[green]Disabled plugin {name}.[/]")

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="refresh")
def refresh_plugins():
    """Re-discovers all available plugins and enables them"""
    _refresh_plugins()

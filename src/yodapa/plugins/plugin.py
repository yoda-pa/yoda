import sqlite3

import typer
from rich import print
from rich.table import Table

from yodapa.plugin import discover_plugins
from yodapa.plugins.config import get_db_connection

PROTECTED_PLUGINS = ["config", "plugin"]

app = typer.Typer(help="Commands to manage plugins")


@app.command(name="list")
def list_plugins():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, enabled FROM plugins")
        rows = cursor.fetchall()

        if not rows:
            print("[yellow] No plugins found.[/]")
            return

        table = Table(title="Yoda Plugins")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Enabled")

        for key, value in rows:
            table.add_row(key, "[green]Yes[/]" if value == 1 else "[red]No[/]")

        print(table)

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="enable")
def enable_plugin(name: str):
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
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="disable")
def disable_plugin(name: str):
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
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="refresh")
def refresh_plugins():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # delete all existing plugins
        cursor.execute("DELETE FROM plugins")

        plugins = discover_plugins()
        for plugin_name, _ in plugins:
            cursor.execute("INSERT INTO plugins VALUES (?, TRUE)", (plugin_name,))

        conn.commit()
        print(f"[green] Plugins refreshed.[/]")

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

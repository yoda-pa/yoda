import sqlite3

import typer
from rich import print
from rich.table import Table

from yodapa.core.util import config_sqlite_file, _refresh_plugins, get_db_connection

app = typer.Typer(help="Config management")


@app.command(name="init")
def initialize_config():
    """Initializes a sqlite db that will store the config"""
    if config_sqlite_file.exists():
        delete_old = typer.confirm("This file already exists. Do you want to continue?")

        if not delete_old:
            return

        # delete old file
        config_sqlite_file.unlink()

    conn = get_db_connection()

    cursor = conn.cursor()
    # create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configurations (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plugins (
            name TEXT PRIMARY KEY,
            enabled BOOLEAN NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url (
            name TEXT PRIMARY KEY,
            url TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    # in addition to creating new tables, we must also load the available plugins
    _refresh_plugins()


@app.command(name="set")
def set_config_value(key: str, value: str):
    """Set a value for a key in config"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO configurations (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (key, value))
        conn.commit()
        print(f"[green]Configuration set:[/] {key} = {value}")
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="get")
def get_config_value(key: str):
    """Get value of a key set in yoda config"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM configurations WHERE key = ?", (key,))
        row = cursor.fetchone()

        if row:
            value = row[0]
            print(f"[blue]{key}[/]: {value}")
        else:
            print(f"[red]Configuration key [white]'{key}'[red] not found.[/]")
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="list")
def list_configurations():
    """List all key-value pairs in the config"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM configurations")
        rows = cursor.fetchall()

        if not rows:
            print("[yellow] No configurations found.[/]")
            return

        table = Table(title="Configurations")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for key, value in rows:
            table.add_row(key, value)

        print(table)

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

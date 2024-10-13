import sqlite3
import urllib

import typer
from rich import print

from yodapa.core.util import get_db_connection

app = typer.Typer()


@app.command(name="shorten")
def shorten_url(name: str, url: str):
    """Store URL as a short name"""

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO url VALUES (?, ?)", (name, urllib.parse.quote(url)))

        conn.commit()
        print(f"[green] URL stored.[/]")
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="expand")
def expand_short_url(name: str):
    """Get expanded URL from short name"""

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM url WHERE name = ?", (name,))
        row = cursor.fetchone()

        if row:
            value = urllib.parse.unquote(row[0])
            print(f"[blue]{name}[/]: [bold]{value}[/]")
        else:
            print(f"[red]URL shortname [white]'{name}'[red] not found.[/]")
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

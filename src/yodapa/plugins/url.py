import typer

app = typer.Typer()


@app.command()
def hello():
    typer.echo("hello")

# @app.command(name="shorten")
# def shorten_url(name: str, url: str):
#     """Store URL as a short name"""
#
#     conn = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO url VALUES (?, ?)", (name, urllib.parse.quote(url)))
#
#         conn.commit()
#         print(f"[green] URL stored.[/]")
#     except sqlite3.OperationalError as e:
#         if "no such table" in str(e):
#             print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
#         else:
#             print(f"An error occurred: {e}")
#     finally:
#         if conn:
#             conn.close()
#
#
# @app.command(name="expand")
# def expand_short_url(name: str):
#     """Get expanded URL from short name"""
#
#     conn = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT value FROM url WHERE name = ?", (name,))
#         row = cursor.fetchone()
#
#         if row:
#             value = row[0]
#             print(f"[blue]{name}[/]: [bold]{value}[/]")
#         else:
#             print(f"[red]URL shortname [white]'{name}'[red] not found.[/]")
#     except sqlite3.OperationalError as e:
#         if "no such table" in str(e):
#             print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
#         else:
#             print(f"An error occurred: {e}")
#     finally:
#         if conn:
#             conn.close()

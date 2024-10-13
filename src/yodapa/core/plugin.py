import importlib
import pkgutil
import sqlite3
from pathlib import Path
from typing import List, Tuple

import typer
from rich import print
from rich.table import Table

from yodapa.core.config import get_db_connection

PROTECTED_PLUGINS = ["config", "plugin"]

app = typer.Typer(help="Commands to manage plugins")


def _discover_yoda_modules():
    plugins = list()
    for package in ["core", "plugins"]:
        plugins_pkg = importlib.import_module(f'yodapa.{package}')
        plugins_path = plugins_pkg.__path__

        for finder, name, ispkg in pkgutil.iter_modules(plugins_path):
            # print("finder", finder, "name", name, "ispkg", ispkg)
            try:
                module = importlib.import_module(f'yodapa.{package}.{name}')
                if hasattr(module, "app") and isinstance(module.app, typer.Typer):
                    plugin_app: typer.Typer = module.app
                    plugins.append((name, plugin_app))
            except Exception as e:
                typer.echo(f"Failed to load plugin {name}: {e}", err=True)
    return plugins


def _discover_plugins_from_config_dir():
    plugins = list()
    local_plugins_dir = Path.home() / ".yoda" / "plugins"
    if local_plugins_dir.exists() and local_plugins_dir.is_dir():
        for finder, name, ispkg in pkgutil.iter_modules([str(local_plugins_dir)]):
            # print("finder", finder, "name", name, "ispkg", ispkg)
            try:
                module_path = local_plugins_dir / f"{name}.py"
                if not module_path.exists():
                    typer.echo(f"Plugin module {name} does not exist at {module_path}", err=True)
                    continue

                # Load the module from the file path
                spec = importlib.util.spec_from_file_location(name, str(module_path))
                if spec is None:
                    typer.echo(f"Could not load spec for module {name}", err=True)
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "app") and isinstance(module.app, typer.Typer):
                    plugin_app: typer.Typer = module.app
                    plugins.append((name, plugin_app))
            except Exception as e:
                typer.echo(f"Failed to load local plugin {name}: {e}", err=True)
    return plugins


def discover_plugins() -> List[Tuple[str, typer.Typer]]:
    """Discover plugins in the 'plugins' directory and the local plugins directory."""

    plugins: List[Tuple[str, typer.Typer]] = list()

    # 1. Discover plugins within the 'plugins' directory
    plugins += _discover_yoda_modules()

    # 2. Discover plugins in the local plugins directory
    plugins += _discover_plugins_from_config_dir()

    # print("Plugins discovered:", plugins)
    return plugins


def load_plugins(app: typer.Typer, plugins: List[Tuple[str, typer.Typer]]):
    """Load the plugins into the yoda typer app."""
    for name, plugin in plugins:
        try:
            app.add_typer(plugin, name=name)
            # typer.echo(f"Loaded plugin: {plugin.name}")
        except Exception as e:
            typer.echo(f"Error loading plugin {name}: {e}", err=True)


def init_plugins(app: typer.Typer):
    """Get plugins from both the disk and sqlite and only show the ones that are enabled
    TODO: Currently a very inefficient implementation, optimize in the future
    """

    plugins = discover_plugins()

    enabled_plugins = get_enabled_plugins()

    load_plugins(app,
                 [(plugin_name, typer_app) for plugin_name, typer_app in plugins if plugin_name in enabled_plugins])


def get_plugin_list():
    """Get plugin list from sqlite3"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, enabled FROM plugins")
        rows = cursor.fetchall()

        return rows

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


def get_enabled_plugins():
    """Get plugin list from sqlite3"""
    return set(name for name, enabled in get_plugin_list() if enabled)


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
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
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
            print("[red]Yoda config not initialized. Use [white]`yoda config init`[red] to initialize[/]")
        else:
            print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


@app.command(name="refresh")
def refresh_plugins():
    """Re-discovers all available plugins and enables them"""
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

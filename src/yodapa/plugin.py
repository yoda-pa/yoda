import importlib
import pkgutil
from importlib.metadata import entry_points
from typing import List

import typer

from yodapa.config import ConfigManager
from .interfaces.plugin_interface import YodaPluginInterface


class PluginManager:
    def __init__(self, app: typer.Typer, config: ConfigManager):
        self.app: typer.Typer = app
        self.config: ConfigManager = config
        self.plugins: List[YodaPluginInterface] = []

    def discover_plugins(self):
        # Discover plugins via entry points
        try:
            entry_points_obj = entry_points()
            print("Entry Points: ", entry_points_obj)
            # For Python >=3.10, entry_points() returns a dict-like object
            if hasattr(entry_points_obj, 'select'):
                plugins = entry_points_obj.select(group='yodapa.plugins')
            else:
                # For older Python versions
                plugins = entry_points_obj.get('yodapa.plugins', [])

            print("Plugins: ", plugins)
            for entry_point in plugins:
                try:
                    plugin_class = entry_point.load()
                    if issubclass(plugin_class, YodaPluginInterface):
                        plugin_instance = plugin_class()
                        self.plugins.append(plugin_instance)
                except Exception as e:
                    typer.echo(f"Failed to load plugin {entry_point.name}: {e}", err=True)
        except Exception as e:
            typer.echo(f"Error accessing entry points: {e}", err=True)

        # Discover plugins in the local plugins directory
        local_plugins_dir = self.config.get_yoda_plugins_dir()
        if local_plugins_dir.exists() and local_plugins_dir.is_dir():
            for finder, name, ispkg in pkgutil.iter_modules([str(local_plugins_dir)]):
                try:
                    module = importlib.import_module(f"yodapa.plugins.{name}")
                    plugin_class = getattr(module, "Plugin", None)
                    if plugin_class and issubclass(plugin_class, YodaPluginInterface):
                        plugin_instance = plugin_class()
                        self.plugins.append(plugin_instance)
                except Exception as e:
                    typer.echo(f"Failed to load local plugin {name}: {e}", err=True)

        typer.echo("Plugins discovered: {}".format([plugin.name for plugin in self.plugins]))

    def load_plugins(self):
        for plugin in self.plugins:
            try:
                plugin_app = plugin.get_app()
                self.app.add_typer(plugin_app, name=plugin.name(), help=f"{plugin.name()} plugin commands")
                typer.echo(f"Loaded plugin: {plugin.name()}")
            except Exception as e:
                typer.echo(f"Error loading plugin {plugin.name()}: {e}", err=True)

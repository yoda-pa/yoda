import importlib
import inspect
import pkgutil
from typing import List

import typer

from yodapa.config import ConfigManager


class PluginManager:
    def __init__(self, app: typer.Typer, config: ConfigManager):
        self.app: typer.Typer = app
        self.config: ConfigManager = config
        self.plugins: List = []

    def discover_plugins(self):
        # Discover plugins within the 'plugins' directory
        plugins_pkg = importlib.import_module('yodapa.plugins')
        plugins_path = plugins_pkg.__path__

        for finder, name, ispkg in pkgutil.iter_modules(plugins_path):
            print("finder", finder, "name", name, "ispkg", ispkg)
            try:
                module = importlib.import_module(f'yodapa.plugins.{name}')
                for attribute_name in dir(module):
                    plugin_class = getattr(module, attribute_name)
                    if inspect.isclass(plugin_class) and hasattr(plugin_class(), "typer_app"):
                        plugin_instance = plugin_class()
                        self.plugins.append(plugin_instance)
            except Exception as e:
                typer.echo(f"Failed to load plugin {name}: {e}", err=True)

        # Discover plugins in the local plugins directory
        # local_plugins_dir = self.config.get_yoda_plugins_dir()
        # if local_plugins_dir.exists() and local_plugins_dir.is_dir():
        #     for finder, name, ispkg in pkgutil.iter_modules([str(local_plugins_dir)]):
        #         try:
        #             module = importlib.import_module(f"yodapa.plugins.{name}")
        #             plugin_class = getattr(module, "Plugin", None)
        #             if plugin_class and issubclass(plugin_class, YodaPluginInterface):
        #                 plugin_instance = plugin_class()
        #                 self.plugins.append(plugin_instance)
        #         except Exception as e:
        #             typer.echo(f"Failed to load local plugin {name}: {e}", err=True)

        # uncomment to debug
        # print("Plugins discovered:", self.plugins)

    def load_plugins(self):
        for plugin in self.plugins:
            try:
                self.app.add_typer(plugin.typer_app, name=plugin.name, help=f"{plugin.name} plugin commands")
                # typer.echo(f"Loaded plugin: {plugin.name}")
            except Exception as e:
                typer.echo(f"Error loading plugin {plugin.name}: {e}", err=True)

    def enable_plugin(self, plugin_name: str):
        # TODO: implement
        pass

    def disable_plugin(self, plugin_name: str):
        # TODO: implement
        pass

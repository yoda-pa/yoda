import importlib
import inspect
import pkgutil
from typing import List

import typer

from yodapa.config import ConfigManager


class PluginManager:
    """Plugin manager class. Manages the plugins in the 'plugins' directory and the local plugins directory."""

    def __init__(self, app: typer.Typer, config: ConfigManager):
        self.app: typer.Typer = app
        self.config: ConfigManager = config
        self.plugins: List = []

    def discover_plugins(self):
        """Discover plugins in the 'plugins' directory and the local plugins directory."""

        # 1. Discover plugins within the 'plugins' directory
        plugins_pkg = importlib.import_module('yodapa.plugins')
        plugins_path = plugins_pkg.__path__

        for finder, name, ispkg in pkgutil.iter_modules(plugins_path):
            # print("finder", finder, "name", name, "ispkg", ispkg)
            try:
                module = importlib.import_module(f'yodapa.plugins.{name}')
                for attribute_name in dir(module):
                    plugin_class = getattr(module, attribute_name)
                    if inspect.isclass(plugin_class) and hasattr(plugin_class(), "typer_app"):
                        plugin_instance = plugin_class()
                        self.plugins.append(plugin_instance)
            except Exception as e:
                typer.echo(f"Failed to load plugin {name}: {e}", err=True)

        # 2. Discover plugins in the local plugins directory
        local_plugins_dir = self.config.get_yoda_plugins_dir()
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

                    # typer.echo(f"Imported module: {module.__name__}")

                    # Find the plugin class in the module (same as above)
                    for attribute_name in dir(module):
                        plugin_class = getattr(module, attribute_name)
                        if inspect.isclass(plugin_class) and hasattr(plugin_class(), "typer_app"):
                            plugin_instance = plugin_class()
                            self.plugins.append(plugin_instance)
                except Exception as e:
                    typer.echo(f"Failed to load local plugin {name}: {e}", err=True)

        # uncomment to debug
        # print("Plugins discovered:", self.plugins)

    def load_plugins(self):
        """Load the plugins into the yoda typer app."""
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

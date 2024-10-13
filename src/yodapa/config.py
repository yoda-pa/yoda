from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigManager:
    """Configuration manager class. Manages the configuration of Yoda."""

    def __init__(self):
        self.base_url = "http://localhost:1111"
        self.config_file = self.get_default_config_file()
        self.config: Dict[str, Any] = dict()
        self.load()

    def load(self):
        """Load the configuration from the configuration file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self.get_default_config()

    def save(self):
        """Save the configuration to the configuration file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            yaml.safe_dump(self.config, f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value by key."""
        self.config[key] = value
        self.save()

    def get_yoda_config_dir(self) -> Path:
        return Path.home() / ".yoda"

    def get_yoda_plugins_dir(self) -> Path:
        return self.get_yoda_config_dir() / "plugins"

    def get_default_config_file(self) -> Path:
        return self.get_yoda_config_dir() / "config.yaml"

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "user": "Skywalker",
            "plugins": {},
        }

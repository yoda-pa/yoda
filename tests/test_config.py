from pathlib import Path

from yodapa.config import ConfigManager

config = ConfigManager()


def test_default_config():
    default_config = config.get_default_config()
    assert default_config.get("user") == "Skywalker"
    assert default_config.get("plugins") == {}


def test_get_yoda_config_dir():
    yoda_config_dir = config.get_yoda_config_dir()
    assert yoda_config_dir == Path.home() / ".yoda"


def test_get_yoda_plugins_dir():
    yoda_plugins_dir = config.get_yoda_plugins_dir()
    assert yoda_plugins_dir == Path.home() / ".yoda" / "plugins"


def test_get_default_config_file():
    default_config_file = config.get_default_config_file()
    assert default_config_file == Path.home() / ".yoda" / "config.yaml"


def test_load():
    config.load()
    assert config.config.get("user") == "Skywalker"
    assert config.config.get("plugins") == {}


def test_save():
    config.set("user", "Yoda")
    config.save()
    config.load()
    assert config.get("user") == "Yoda"
    config.set("user", "Padawan")
    config.save()
    config.load()
    assert config.get("user") == "Padawan"

    # assert that the config file is created
    assert config.config_file.exists()

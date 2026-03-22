from carbon.helpers import CarbonError

from pathlib import Path

import toml
from typing import Any

class ConfigGetter:


    def __init__(self, config_path: str):
        self._config_path = Path(config_path).expanduser()
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self):

        try:
            with open(self._config_path) as file:
                self._config = toml.load(file)
        except (FileNotFoundError, toml.TomlDecodeError) as e:
            CarbonError(f"Invalid Config File! {e.__class__.__name__} ({self._config_path})").halt()

    def _save_config(self):

        with open(self._config_path, "w") as file:
            toml.dump(self._config, file)


    def get(self, path: str, default: Any = None, *, valid_types: tuple[object] | None = None, valid_values: tuple[object] | None = None) -> Any:
        "Get a variable from config."
        
        parts = path.split(".")

        sub_config = self._config

        for part in parts:
            
            if part not in sub_config:
                return default
            
            sub_config = sub_config[part]

        if not valid_types:
            return sub_config
        
        if isinstance(sub_config, valid_types):   

            if not valid_values: return sub_config

            for value in valid_values:
                if sub_config == value: return sub_config

        return default
        
    
    def set(self, path: str, val: Any) -> None:
        "Set a config variable"

        parts = path.split(".")
        sub_config = self._config

        for part in parts[:-1]:
            if part not in sub_config:
                sub_config[part] = {}
            sub_config = sub_config[part]

        sub_config[parts[-1]] = val
        self._save_config()


    @property
    def CachePath(self) -> Path:
        cache = Path("~/.carbon/cache").expanduser()
        if not cache.exists():
            cache.mkdir()
        return cache


    @property
    def ConfigPath(self) -> Path:
        return self._config_path
        

CarbonConfig = ConfigGetter("~/.carbon/config.toml")
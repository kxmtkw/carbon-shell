from pathlib import Path

import toml
from typing import Any

class CarbonConfig:

    CONFIG_PATH = Path("~/.carbon/settings/config.toml").expanduser()

    def __init__(self):
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self):

        with open(CarbonConfig.CONFIG_PATH) as file:
            self._config = toml.load(file)

    def _save_config(self):

        with open(CarbonConfig.CONFIG_PATH, "w") as file:
            toml.dump(self._config, file)

    def get(self, key: str, default: Any = None, *, valid_types: tuple[object] | None = None) -> Any:
        "Get a variable from config."
        
        if key not in self._config:
            return default
        
        val = self._config[key]

        if not valid_types:
            return val
        
        if isinstance(val, valid_types):
            return val
        else:
            return default
        
    
    def set(self, key: str, val: Any) -> Any:
        "Set a config variable"
        
        self._config[key] = val
        self._save_config()
    
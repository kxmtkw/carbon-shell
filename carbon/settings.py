from pathlib import Path
import tomllib
from typing import Any

from carbon.helpers import CarbonError

class SettingsLoader():

    def __init__(self, src: str | dict):
        
        if isinstance(src, dict):
            self.settings = src
            return
        
        self.filepath = Path(src).expanduser()
        self.settings: dict[Any, Any] = {}

        if not self.filepath.exists():
            CarbonError(f"Could not find settings file: {self.filepath}").halt()

        with open(self.filepath, "rb") as file:
            self.settings = tomllib.load(file)

    def get(self, path: str | None = None):

        if not path:
            return self.settings
        
        sections = path.split(".")

        val = self.settings
        for section in sections:
            try:
                val = val[section]
            except Exception:
                CarbonError(
                    f"Corrupted settings file or invalid key path. File:{self.filepath}; Key:{path}"
                ).halt()

        return val
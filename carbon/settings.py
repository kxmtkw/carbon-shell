from pathlib import Path
import tomllib

from carbon.helpers import CarbonError

class SettingsLoader():

    def __init__(self, filepath: str):
        
        self.filepath = Path(filepath)
        self.settings: dict[any, any] = {}

        if not self.filepath.exists():
            CarbonError(f"Could not find settings file: {self.filepath}").halt()

        with open(self.filepath) as file:
            self.settings = tomllib.load(file)

    def get(self, path: str):
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
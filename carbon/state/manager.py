from pathlib import Path
import json
from typing import Any, Callable

from carbon.utils import FileWatcher

class StateManager:

    def __init__(self, path: str):
        self._state = {}
        self._state_file = Path(path).expanduser()
        self._is_loading_needed = True

        if not self._state_file.parent.exists():
            self._state_file.parent.mkdir(511, True, True)

        if not self._state_file.exists():
            with open(self._state_file, "w") as file:
                json.dump({}, file)

    @property
    def file(self) -> Path:
        return self._state_file

    def update(self, key: str, state: dict):
        self._state[key] = state


    def get(self, key: str) -> dict[str, Any] | None:
        return self._state.setdefault(key, None)
    

    def save(self):
        
        string = json.dumps(self._state, skipkeys=True, indent=4) 
                
        with open(self._state_file, "w") as file:
            file.write(string)
           

    def load(self) -> bool:
        
        with open(self._state_file) as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return False

        self._state = data
        return True

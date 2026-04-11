from pathlib import Path
import json
from typing import Any

class StateManager:

    def __init__(self):
        self._state = {}
        self._state_file = Path("~/.carbon/user/state.json").expanduser()

        if self._state_file.exists(): return

        if not self._state_file.parent.exists():
            self._state_file.parent.mkdir(511, True, True)

        with open(self._state_file, "w") as file:
            json.dump({}, file)


    def update(self, key: str, state: dict):
        self._state[key] = state


    def get(self, key: str) -> dict[str, Any] | None:
        return self._state.setdefault(key, None)
    

    def save(self):

        string = json.dumps(self._state, skipkeys=True, indent=4) 
                
        with open(self._state_file, "w") as file:
            file.write(string)
           

    def load(self):
        with open(self._state_file) as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        self._state = data




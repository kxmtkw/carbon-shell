import json
from pathlib import Path
from typing import Any

CARBON_STATE_PATH = "~/.carbon/cache/carbon.state"

class _State():

    def __init__(self):
        self._state_file = Path(CARBON_STATE_PATH).expanduser()

        self._state: dict[str, Any] = {}

        self._load_state()

    def _load_state(self):
        "Load the current carbon state from file."

        if not self._state_file.exists():

            with open(self._state_file, "w") as file:
                json.dump({}, file)

            return
        
        try:
            with open(self._state_file) as file: 
                self._state = json.load(file)

        except json.JSONDecodeError:
            with open(self._state_file, "w") as file:
                json.dump({}, file)
        

    def _save_state(self):

        with open(self._state_file, "w") as file:
            json.dump(self._state, file)


    def get(self, key: str, default: Any = None, *, valid_types: tuple[object] | None = None) -> Any:
        "Get a variable from state."
        
        if key not in self._state:
            return default
        
        val = self._state[key]

        if not valid_types:
            return val
        
        if isinstance(val, valid_types):
            return val
        else:
            return default
        
    
    def set(self, key: str, val: Any) -> Any:
        "Set a state variable"
        
        self._state[key] = val
        self._save_state()

from threading import Lock

from carbon.managers.base import BaseManager
from carbon.managers.theme import ThemeManager
from carbon.utils import CarbonError, procrun, is_valid_hex

from .base import BaseController
from .providers import (
    Launcher,
    Power,
    Screenshot,
    Theme,
    Networker,
    Clipboard,
    Windows
)

class ControllerManager(BaseManager):

    def __init__(self, themer: ThemeManager):
        super().__init__()
        self.lock = Lock()

        self.current_controller: BaseController | None = None

        self.launcher = Launcher()
        self.power = Power()
        self.screenshot = Screenshot()
        self.theme = Theme(themer)
        self.networker = Networker()
        self.clipboard = Clipboard()
        self.windows = Windows()

        self.controllers = {
            "launcher": self.launcher,
            "power": self.power,
            "screenshot": self.screenshot,
            "theme": self.theme,
            "networker": self.networker,
            "clipboard": self.clipboard,
            "windows": self.windows
        }

        self._handlers = {
            "run": self.run,
            "close-all": self.close
        }


    def handlers(self) -> dict[str, callable]:
        return self._handlers
    

    def run(self, *, name: str) -> str:
       
        controller = self.controllers.get(name)
        print("Launched controller:", name)
        print("Current controller:", self.current_controller.__class__.__name__ if self.current_controller else None)
        
        if not controller:
            raise CarbonError(f"Controller not found: {name}")
        
        
        if self.current_controller is controller:
            self.current_controller.close()
            with self.lock: self.current_controller = None
            return
        
        if self.current_controller:
            
            self.current_controller.close()
            with self.lock: self.current_controller = None        
        
        with self.lock:
            self.current_controller = controller

            try:
                controller.launch()
            except Exception as e:
                self.current_controller = None
                raise e
            
            self.current_controller = None


    def close(self) -> str:
        if self.current_controller:
            self.current_controller.close()
            self.current_controller = None
            return "Controller closed."
        else:
            return "No controller to close."
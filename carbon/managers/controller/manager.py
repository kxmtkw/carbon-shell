
from threading import Lock

from carbon.managers.base import BaseManager
from carbon.managers.theme import ThemeManager
from carbon.utils import CarbonError, procrun, is_valid_hex, logger

from .base import BaseController
from .providers import (
    Launcher,
    Power,
    Screenshot,
    Theme,
    Networker,
    Clipboard,
    Windows,
    Runner
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
        self.runner = Runner()

        self.controllers = {
            "launcher": self.launcher,
            "power": self.power,
            "screenshot": self.screenshot,
            "theme": self.theme,
            "networker": self.networker,
            "clipboard": self.clipboard,
            "windows": self.windows,
            "runner": self.runner
        }

        self._handlers = {
            "run": self.run,
            "close-all": self.close
        }


    def handlers(self) -> dict[str, callable]:
        return self._handlers
    

    def run(self, *, name: str) -> str:
       
        controller: BaseController = self.controllers.get(name)
        
        if not controller:
            raise CarbonError(f"Controller not found: {name}")

        logger.log(
            "controller",
            f"Launching controller: {name}. Previous/Active controller: {self.current_controller.__class__.__name__}",
            logger.Level.info
        )
        
        if self.current_controller is controller:
            self.current_controller.close()
            with self.lock: self.current_controller = None
            return "Was already open, closed it."
        
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
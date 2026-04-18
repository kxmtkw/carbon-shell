
from dataclasses import dataclass
from threading import Lock

from carbon.managers.base import BaseManager
from carbon.managers.theme import ThemeManager
from carbon.utils import CarbonError, procrun, isValidHex, logger

from carbon.lib.quickshell import Quickshell

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

    @dataclass(init=True, kw_only=True)
    class State(BaseManager.State):
        pass

    def __init__(self, themer: ThemeManager):
        super().__init__()
        self.lock = Lock()
        self.qs = Quickshell()
        self.panel_should_return_normal: bool = True

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

        self.state = self.State()


    def handlers(self) -> dict[str, callable]:
        return {
            "run": self.run,
            "close": self.close
        }


    def setState(self, state):
        pass


    def getState(self):
        return self.state
    

    def run(self, *, name: str) -> str:

        # get controller
        controller: BaseController = self.controllers.get(name)
        if not controller:
            raise CarbonError(f"Controller not found: {name}")

        logger.log(
            "controller",
            f"Launching controller: {name}. Previous/Active controller: {self.current_controller.__class__.__name__}",
            logger.Level.info
        )
        
        # if active controller was launched again, we close it instead. run() is basically a toggle
        if self.current_controller is controller:
            self.current_controller.close()
            self.current_controller = None
            logger.log(
                "controller",
                f"Controller {name} was already opened, so closed it.",
                logger.Level.debug
            )
            return "Was already open, closed it."
        

        if self.current_controller:
            self.panel_should_return_normal = False
            self.current_controller.close()
            self.current_controller = None
        

        with self.lock:
            
            self.current_controller = controller

            self.qs.setPanelMode("bypass")
            self.panel_should_return_normal = True

            try:
                controller.launch()
            except Exception as e:
                self.current_controller = None
                raise e                
            
            self.current_controller = None

            if self.panel_should_return_normal:
                self.qs.setPanelMode("normal")
        
            
        logger.log(
            "controller",
            f"Controller {name} was closed.",
            logger.Level.debug
        )


    def close(self) -> str:
        if self.current_controller:
            self.current_controller.close()
            self.current_controller = None
            return "Controller closed."
        else:
            return "No controller to close."
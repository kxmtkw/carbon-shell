from dataclasses import dataclass
from threading import Lock
import time
from typing import Any, Callable, Dict

from carbon.managers.base import BaseManager
from carbon.managers.theme import ThemeManager
from carbon.managers.panel import PanelManager

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


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None]):
		super().__init__(internalDispatch)
		self.lock = Lock()
		self.qs = Quickshell()
		self.current_controller: BaseController | None = None
		self.state = self.State()

		self.panel_should_return_normal: bool = True


	def start(self):

		self.launcher = Launcher(self.internalDispatch)
		self.power = Power(self.internalDispatch)
		self.screenshot = Screenshot(self.internalDispatch)
		self.theme = Theme(self.internalDispatch)
		self.networker = Networker(self.internalDispatch)
		self.clipboard = Clipboard(self.internalDispatch)
		self.windows = Windows(self.internalDispatch)
		self.runner = Runner(self.internalDispatch)

		self.controllers: Dict[str, BaseController] = {
			"launcher": self.launcher,
			"power": self.power,
			"screenshot": self.screenshot,
			"theme": self.theme,
			"networker": self.networker,
			"clipboard": self.clipboard,
			"windows": self.windows,
			"runner": self.runner
		}


	def end(self):
		pass


	def name(self):
		return "controller"


	def handlers(self) -> dict[str, Callable]:
		return {
			"run": self.run,
			"close": self.close
		}


	def setState(self, state):
		
		for controller in self.controllers.values():
			controller.reload()


	def getState(self):
		return self.state


	def getHelp(self):
		return _help
	
	
	def setManagers(self, themer: ThemeManager):
		self.theme.themer = themer


	def run(self, *, name: str) -> str:

		# get controller
		controller: BaseController | None = self.controllers.get(name)
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
		
		with self.lock:
			
			self.current_controller = controller
			
			self.internalDispatch("panel", "toggle-bypass", {"state": "on"})
			self.panel_should_return_normal = True

			try:
				controller.launch()
			except Exception as e:
				self.current_controller = None
				raise e                
			
			self.current_controller = None

			if self.panel_should_return_normal:
				self.internalDispatch("panel", "toggle-bypass", {"state": "off"})
		
			
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


_help = """
==> controller
Open and close controllers. Controllers are basically menus.

handlers:

	> run --name [name]
		Open/Close the named controller.

	> close
		Close any active controller.
"""

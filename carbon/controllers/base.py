from typing import Any, Callable
from carbon.managers.base import BaseManager

class BaseController:

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], BaseManager.State|None]):
		self.internalDispatch = internalDispatch
		self.getManagerState: Callable[[str], BaseManager.State|None] = getManagerState
		self.config = {}
	
	def setConfig(self, config: dict[str, Any]):
		pass

	def name(self) -> str:
		raise NotImplementedError()

	def reload(self):
		pass
	
	def launch(self):
		raise NotImplementedError()
	
	def close(self):
		raise NotImplementedError()                                                                              
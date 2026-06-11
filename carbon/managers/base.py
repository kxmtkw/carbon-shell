from typing import Dict, Callable, Any
from dataclasses import dataclass

class BaseManager:

	@dataclass(init=True, kw_only=True)
	class State:
		pass

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State|None]):
		self.internalDispatch: Callable[[str, str, dict[str, Any]], None] = internalDispatch
		self.getManagerState: Callable[[str], BaseManager.State|None] = getManagerState
		self.state: BaseManager.State
	
	def start(self):
		raise NotImplementedError()

	def end(self):
		raise NotImplementedError()
	
	def name(self) -> str:
		raise NotImplementedError()
	
	def handlers(self) -> Dict[str, Callable]:
		raise NotImplementedError()
	
	def getState(self) -> State:
		raise NotImplementedError()
	
	def setState(self, state: State):
		raise NotImplementedError()
	
	def getHelp(self) -> str:
		raise NotImplementedError()

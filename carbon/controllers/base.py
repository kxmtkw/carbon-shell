from typing import Any, Callable

class BaseController:

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None]):
		self.internalDispatch = internalDispatch
	
	def reload(self):
		pass
	
	def launch(self):
		raise NotImplementedError()
	
	def close(self):
		raise NotImplementedError()                                                                              
from typing import Any, Callable

from carbon.controllers.base import BaseController
from carbon.lib.rofi import RofiShell
from carbon.managers.base import BaseManager

class Windows(BaseController):

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], BaseManager.State|None]):
		super().__init__(internalDispatch, getManagerState)
		
		self.rasi = "~/.carbon/shell/rofi/windows/main.rasi"
		self.rofi = RofiShell(self.rasi)
	
	def reload(self):
		return super().reload()
	
	def launch(self):
		self.rofi.display(
			mode=RofiShell.Mode.window
		)
		self.rofi.wait()

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

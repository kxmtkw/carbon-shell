from typing import Any, Callable

from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell

class Launcher(BaseController):

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None]):
		super().__init__(internalDispatch)
		self.rasi = "~/.carbon/shell/rofi/launcher/main.rasi"
		self.rofi = RofiShell(self.rasi)
	
	def reload(self):
		return super().reload()
	
	def launch(self):
		self.rofi.display(
			prompt="Launcher",
			mode=RofiShell.Mode.drun
		)
		self.rofi.wait()

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

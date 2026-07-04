from typing import Any, Callable

from carbon.controllers.base import BaseController
from carbon.lib.rofi import RofiShell

from carbon.managers.base import BaseManager
from carbon.utils import shellrun

class Clipboard(BaseController):

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], BaseManager.State|None]):
		super().__init__(internalDispatch, getManagerState)
		self.rasi = "~/.carbon/shell/rofi/clipboard/main.rasi"
		self.rofi = RofiShell(self.rasi)

	def name(self) -> str:
		return "clipboard"
	
	def reload(self):
		return super().reload()
	
	def launch(self):
		
		success, data = shellrun("cliphist list")

		if not success:
			return
		
		options = [data]
		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Clipboard",
			options=options
		)

		selected = self.rofi.wait()

		if not selected:
			return

		shellrun(f"echo '{selected}' | cliphist decode | wl-copy", wait=False)

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

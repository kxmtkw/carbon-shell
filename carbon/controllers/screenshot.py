from pathlib import Path
import sys, time
from typing import Any, Callable

from carbon.lib.rofi import RofiShell
from carbon.controllers.base import BaseController

from carbon.managers.base import BaseManager
from carbon.utils import shellrun

class Screenshot(BaseController):
	
	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], BaseManager.State|None]):
		super().__init__(internalDispatch, getManagerState)
		
		self.rofi = RofiShell("~/.carbon/shell/rofi/screenshot/main.rasi")

		self.save_dir = Path("~/Pictures").expanduser()

		self.options: list[str] = [
			"  Screen",
			"  Window",
			"󰿦  Region"
		]

	def name(self) -> str:
		return "screenshot"
	
	def reload(self):
		return super().reload()

	def launch(self):

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			options= self.options
		)

		selected: str = self.rofi.wait()
		if not selected: return

		self.exec(selected.strip())


	def exec(self, option: str):

		time.sleep(0.2) # rofi closes

		if option == self.options[0]:
			shellrun(f"hyprshot -m active -m output -o {self.save_dir}", wait=False)

		elif option == self.options[1]:
			shellrun(f"hyprshot -m window -o {self.save_dir}", wait=False)

		elif option == self.options[2]:
			shellrun(f"hyprshot -m region -o {self.save_dir}", wait=False)

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass
		

if __name__ == "__main__":
	c = Screenshot(lambda *_args, **_kwargs: None)
	c.launch()

from pathlib import Path
import sys, time

from carbon.lib.rofi import RofiShell
from carbon.managers.controller.base import BaseController

from carbon.utils import shellrun

class Screenshot(BaseController):
	
	def __init__(self):
		self.rofi = RofiShell("~/.carbon/shell/rofi/screenshot/main.rasi")

		self.save_dir = Path("~/Pictures").expanduser()

		self.options: list[str] = [
			"  Screen",
			"  Window",
			"󰿦  Region"
		]

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
	c = Screenshot()
	c.launch()
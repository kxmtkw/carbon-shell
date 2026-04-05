from pathlib import Path
from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell

class Launcher(BaseController):

	def __init__(self):
		super().__init__()
		self.rasi = "~/.carbon/shell/rofi/launcher/main.rasi"
		self.rofi = RofiShell(self.rasi)
	
	def launch(self):
		self.rofi.display(
			mode=RofiShell.Mode.drun
		)
		self.rofi.wait()

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

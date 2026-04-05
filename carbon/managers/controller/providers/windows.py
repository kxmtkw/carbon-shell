from pathlib import Path
from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell

class Windows(BaseController):

	def __init__(self):
		super().__init__()
		self.rasi = "~/.carbon/shell/rofi/windows/main.rasi"
		self.rofi = RofiShell(self.rasi)
	
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

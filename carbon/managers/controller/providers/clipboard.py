from pathlib import Path
from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell

from carbon.utils import shellrun

class Clipboard(BaseController):

	def __init__(self):
		super().__init__()
		self.rasi = "~/.carbon/shell/rofi/clipboard/main.rasi"
		self.rofi = RofiShell(self.rasi)
	
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

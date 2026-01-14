import subprocess
from pathlib import Path
from typing import Optional


class RofiShell:

	class Error(Exception):
		def __init__(self, *args, **kwargs):
			super().__init__(args, kwargs)

	class Mode:
		Drun       = "drun"
		Run        = "run"
		Window     = "window"
		Filebrower = "filebrowser"

	@classmethod
	def Run(cls, cmd: str) -> str:
		output = subprocess.run(f"rofi {cmd}", shell=True, capture_output=True, text=True)
		return output.stdout if (output.returncode == 0) else output.stderr


	def __init__(self, theme: str = ""):
		self.theme: Optional[Path] = Path(theme) if theme else None
		if self.theme:
			if not self.theme.exists():
				raise RofiShell.Error(f"Theme file not found: {theme}")
			

	def openMode(self, mode: str):
		cmd = f"-show {mode} -theme {self.theme.absolute() if self.theme else ""}"
		self.Run(cmd)

	




rofi = RofiShell("/home/haseeb/code/dots/Config/rofi/launcher/style.rasi")
rofi.openMode(RofiShell.Mode.Filebrower)
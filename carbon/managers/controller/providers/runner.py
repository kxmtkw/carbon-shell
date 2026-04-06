from pathlib import Path
import subprocess
from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell
from carbon.utils import logger
import os
import shlex

class Runner(BaseController):

	def __init__(self):
		super().__init__()
		self.rasi_main = "~/.carbon/shell/rofi/run/main.rasi"
		self.rasi_error = "~/.carbon/shell/rofi/run/error.rasi"

		self.rofi = RofiShell(self.rasi_main)

		self.binaries: list[str] = []

		self.load_binaries()
	

	def load_binaries(self) -> set[str]:

		path = os.environ["PATH"]
		directories = path.split(":")

		binaries = set()

		for d in directories:
			directory = Path(d)

			if not directory.exists(): continue

			for item in directory.iterdir():
				if item.is_file():
					binaries.add(item.name)

		self.binaries = list(binaries)
		self.binaries.sort()

	
	def display_error(self, msg: str):

		self.rofi.updateTheme(self.rasi_error)

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=msg
		)

		self.rofi.wait()


	def launch(self):

		self.rofi.updateTheme(self.rasi_main)

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Run ::",
			options=self.binaries
		)

		selected = self.rofi.wait()

		if not selected: return

		self.exec(selected)


	def exec(self, selected: str):

		try:
			cmd = shlex.split(selected)
		except ValueError as e:
			self.display_error(f"Syntax Error: {str(e)}")
			return
		
		try:
			subprocess.Popen(
				cmd,
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,
				stdin=subprocess.DEVNULL
			)
		except FileNotFoundError:
			self.display_error(f"File Not Found: {cmd[0]}")
		except PermissionError:
			self.display_error(f"Permission Error: {cmd[0]}")

			
	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

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

		self.loadBinaries()

		self.specials: dict[str, str] = {
			"@terminal": os.environ.get("TERMINAL", "alacritty"),
			"@editor": os.environ.get("EDITOR", "alacritty -e nano"),
			"@browser": os.environ.get("BROWSER", "firefox"),
			"@files": os.environ.get("FILES", "dolphin"),
			"@music": os.environ.get("MUSIC", "spotify"),
		}

		self.binaries.extend(self.specials.keys())
	
	
	def reload(self):
		self.loadBinaries()
		self.binaries.extend(self.specials.keys())


	def loadBinaries(self) -> set[str]:

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

	
	def displayError(self, msg: str):

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

		self.parse(selected)


	def parse(self, selected: str):
		
		modifier = selected[0]

		match modifier:
			case "$":
				self.execShell(selected.removeprefix("$"))
			case "@":
				self.execSpecial(selected)
			case _:
				self.execProc(selected)


	def execProc(self, selected: str):

		try:
			cmd = shlex.split(selected)
		except ValueError as e:
			self.displayError(f"Syntax Error: {str(e)}")
			return
		
		try:
			subprocess.Popen(
				cmd,
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,
				stdin=subprocess.DEVNULL
			)
		except FileNotFoundError:
			self.displayError(f"File Not Found: {cmd[0]}")
		except PermissionError:
			self.displayError(f"Permission Denied: {cmd[0]}")


	def execShell(self, cmd: str):
		
		subprocess.Popen(
			cmd,
			shell=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			stdin=subprocess.DEVNULL
		)
		

	def execSpecial(self, cmd: str):
		
		if cmd not in self.specials:
			self.displayError(f"Unknown Special: {cmd}")
			return
		
		target = self.specials[cmd]
		self.execProc(target)


	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass

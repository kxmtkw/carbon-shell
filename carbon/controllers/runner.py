from pathlib import Path
import subprocess, os, shlex, math
from typing import Any, Callable
from carbon.controllers.base import BaseController
from carbon.lib.rofi import RofiShell
from carbon.managers.base import BaseManager
from carbon.utils import logger
from simpleeval import simple_eval, NameNotDefined

from carbon.utils.functions import procrun, shellrun

class Runner(BaseController):

	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], BaseManager.State|None]):
		super().__init__(internalDispatch, getManagerState)
		
		self.rasi_main = "~/.carbon/shell/rofi/runner/main.rasi"
		self.rasi_error = "~/.carbon/shell/rofi/runner/error.rasi"
		self.rasi_display = "~/.carbon/shell/rofi/runner/display.rasi"

		self.is_running = True

		self.rofi = RofiShell(self.rasi_main)

		self.binaries: list[str] = []
		self.specials: dict[str, str] = {}

		self.calc_variables = {
			"pi": math.pi,
			"e": math.e,
			"_": 0
		}

		self.calc_functions = {
			"sin": math.sin,
			"cos": math.cos,
			"tan": math.tan,
			"round": round,
			"sqrt": math.sqrt,
			"radians": math.radians,
			"degrees": math.degrees,
			"log": math.log10,
			"ln": math.log1p
		}

	
	def setConfig(self, config: dict[str, Any]):
		self.loadBinaries()
		 
		for name, val in config.items():
			self.specials[f"@{name}"] = str(val)

		self.binaries.extend(self.specials.keys())


	def loadBinaries(self):

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


	def displayMesg(self, msg: str):

		self.rofi.updateTheme(self.rasi_display)

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=msg
		)

		self.rofi.wait()


	def launch(self):

		self.is_running = True

		while self.is_running:

			self.rofi.updateTheme(self.rasi_main)

			self.rofi.display(
				mode=RofiShell.Mode.dmenu,
				prompt=">>> ",
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
			case "=":
				self.execCalc(selected.removeprefix("="))
			case "?":
				self.execSearch(selected.removeprefix("?"))
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
			self.close()

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

		self.close()
		

	def execSpecial(self, cmd: str):
		
		if cmd not in self.specials:
			self.displayError(f"Unknown Special: {cmd}")
			return
		
		target = self.specials[cmd]
		self.execProc(target)

		self.close()


	def execCalc(self, expr: str):
		try:
			result = simple_eval(expr, names=self.calc_variables, functions=self.calc_functions)
		except SyntaxError:
			self.displayError(f"Invalid syntax")
			return
		except NameNotDefined as e:
			self.displayError(f"Name not defined: {e.name}")
			return
		
		self.calc_variables["_"] = result
		self.displayMesg(str(result))


	def execSearch(self, text: str):
		procrun(["xdg-open", f"https://www.google.com/search?q={text}"], wait=False)
		self.close()


	def close(self):
		try:
			self.is_running = False
			self.rofi.close()
		except RofiShell.Error:
			pass

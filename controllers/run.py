from pathlib import Path
import subprocess, shlex
import os

from lib.rofi import RofiShell
import simpleeval

class RunPrompt():
	

	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/run/main.rasi")

		self.hist_file: Path = Path("~/.carbon/cache/run_history.txt").expanduser()

		
		self.cache_file: Path = Path("~/.carbon/cache/run_cache.txt").expanduser()

		self.options: list[str] = self.load_entries()


	def load_entries(self) -> list[str]:

		print("Loading entries for run...")

		options = []

		if self.cache_file.exists():
			print("Cache found! Using it instead.")
			options.extend(self.load_cache())
		else:
			self.cache_file.touch()
			options.extend(self.rebuild_cache())

		if not self.hist_file.exists():
			self.hist_file.touch()

		options.extend(self.load_history())
		
		print("All entries loaded.")

		return options
	

	def load_cache(self) -> list[str]:

		with open(self.cache_file) as file:
			content = file.read()

		return content.splitlines()


	def rebuild_cache(self) -> list[str]:
		
		print("Rebuilding cache...")

		entries = []
		entries.extend(self.get_binaries())

		with open(self.cache_file, "w") as file:
			file.write("\n".join(entries))

		return entries
	

	def load_history(self) -> list[str]:

		with open(self.hist_file, "r") as file:
			content = file.read()

		self.history_set = set(content.splitlines())
		
		history = list(self.history_set)

		print("Loaded history.")

		return history


	def save_history(self, cmd: str):
		with open(self.hist_file, "a") as file:
			file.write(cmd+"\n")
	

	def get_binaries(self) -> list[str]:

		PATH = os.environ.get("PATH")

		if not PATH:
			self.show_error("$PATH not defined! Cannot parse system binaries.")
			exit(1)

		dirs = [Path(s) for s in PATH.split(":")]
		dirs.reverse()

		binaries = []

		for d in dirs:
			
			if not d.exists(): continue
			if not d.is_dir(): continue

			for binary in d.iterdir():
				binaries.append(binary.name)

		binaries.sort()

		print("Loaded binaries.")

		return binaries

	
	def show_error(self, msg: str):

		self.rofi.updateTheme("~/.config/rofi/run/error.rasi")

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=msg
		)

		self.rofi.wait()


	def launch(self):

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Run ::",
			options=self.options
		)
		
		selected = self.rofi.wait()

		if not selected: exit()

		print(f"Selected: {selected}")

		self.parse(selected)

	
	def parse(self, selected: str):
		
		cmd = selected.strip()

		mod = cmd[0]
		modded_cmd = cmd[1:]

		match mod:
			case "$":
				self.execute_shell(modded_cmd)
			case "%":
				self.parse(modded_cmd)
			case "=":
				self.execute_mathexpr(modded_cmd)
			case _:
				self.execute_subprocess(cmd)

		if mod != "%":
			self.save_history(f"% {selected}")


	def execute_subprocess(self, cmd: str):

		
		try:
			cmd_list = shlex.split(cmd)
			print(cmd_list)
		except ValueError as e:
			self.show_error(f"Syntax Error: {e}")
			return

		try:
			proc = subprocess.Popen(
				cmd_list,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE
			)
			proc.wait(1)
		except FileNotFoundError:
			self.show_error(f"Command not found: {cmd}")
			return
		except PermissionError:
			self.show_error("Insufficient Permissions!")
			return
		except subprocess.TimeoutExpired:
			return
		


	def execute_shell(self, cmd: str):

		subprocess.Popen(
			cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			shell=True
		)

	
	def execute_mathexpr(self, expr: str):

		result = simpleeval.simple_eval(expr)
		self.show_error(str(result))


if __name__ == "__main__":
	c = RunPrompt()
	c.launch()
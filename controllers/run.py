from pathlib import Path
import subprocess, shlex
import os

from lib.rofi import RofiShell


class RunPrompt():
	

	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/run/main.rasi")
		self.options: list[str] = self.load_entries()


	def load_entries(self) -> list[str]:

		print("Loading entries for run...")

		options = []
		options.extend(self.get_binaries())
		
		print("All entries loaded.")

		return options


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


	def get_history(self) -> list[str]:
		pass 

	
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

		mod = selected[0]
		modded_cmd = selected[1:]

		match mod:
			case "$":
				self.execute_shell(modded_cmd)
				return
			

		self.execute_subprocess(cmd)


	def execute_subprocess(self, cmd: str):

		try:
			cmd_list = shlex.split(cmd)
		except ValueError as e:
			self.show_error(f"Syntax Error: {e}")
			return

		try:
			subprocess.Popen(
				cmd_list,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE
			)
		except FileNotFoundError:
			self.show_error(f"Command not found: {cmd}")
			return
		except PermissionError:
			self.show_error("Insufficient Permissions!")
			return


	def execute_shell(self, cmd: str):

		subprocess.Popen(
			cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			shell=True
		)


if __name__ == "__main__":
	c = RunPrompt()
	c.launch()
from pathlib import Path
from rofi import RofiShell
import subprocess, shlex
import os

class RunPrompt():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/run/main.rasi")

		self.prompt = "Run"
		self.mesg = ""

		dirs = [Path("/usr/bin"), Path("~/.local/share/bin").expanduser()]


		self.options: list[str] = []

		for d in dirs:
			
			if not d.exists(): continue
			if not d.is_dir(): continue

			for binary in d.iterdir():
				self.options.append(binary.name)

		self.options.sort()


	def launch(self):

		selected: str = self.rofi.display(
			self.prompt,
			self.mesg,
			self.options
		)

		if not selected: return

		self.parse(selected)


	def parse(self, selected: str):
		
		try:
			cmd = shlex.split(selected)
		except ValueError as e:
			self.show_error(f"Invalid Syntax!\n{str(e)}.")
			exit(1)

		modifier = cmd[-1]

		if not modifier.startswith("#"):
			self.exec(cmd)
			return
		
		cmd.pop()

		match modifier:

			case "#t":
				self.execTerminal(cmd)

		
	
	def exec(self, cmd: list[str]):
		try:
			proc = subprocess.Popen(
				cmd,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				text=True
			)
		except FileNotFoundError:
			self.show_error(f"Command not found: {cmd[0]}")
		except PermissionError:
			self.show_error("Insufficient Permissions!")


	def execTerminal(self, cmd: list[str]):
		
		terminal = os.environ.get("TERM")
		term_cmd = [terminal, "-e"]
		term_cmd.extend(cmd)

		self.exec(term_cmd)

	def show_error(self, msg: str):

		self.rofi.updateTheme("~/.config/rofi/run/error.rasi")

		self.rofi.display(
			msg,
			"",
			[]
		)



if __name__ == "__main__":
	c = RunPrompt()
	c.launch()
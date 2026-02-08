from pathlib import Path
from rofi import RofiShell
import subprocess, shlex
import os, time


end = 0
start = time.perf_counter()

def timed():
	global end
	global start
	end = time.perf_counter()
	print(end - start)
	start = end 

class RunPrompt():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/run/main.rasi")

		self.prompt = "Run ::"
		self.mesg = ""
		
		PATH = os.environ.get("PATH")

		if not PATH:
			self.show_error("No $PATH env var found!")
			exit(1)
		else:
			dirs = [Path(s) for s in PATH.split(":")]
			dirs.reverse()

		self.options = []
		self.history = set(self.load_history())

		
		for d in dirs:
			
			if not d.exists(): continue
			if not d.is_dir(): continue

			for binary in d.iterdir():
				if binary.name in self.history:
					self.history.remove(binary.name)
					
				self.options.append(f"  {binary.name}")

		self.options.extend([f"  {item}" for item in self.history])


	def load_history(self) -> list[str]:

		history_file = Path("~/.carbon/cache/run_history.txt").expanduser()

		if not history_file.exists(): return []

		with open(history_file, "r") as file:
			history = file.read()

		return history.splitlines()
		 

	def add_to_history(self, cmd: str):

		if cmd in self.history:
			return
		
		history_file = Path("~/.carbon/cache/run_history.txt").expanduser()

		if not history_file.exists():
			history_file.touch()

		with open(history_file, "a") as file:
			file.write(cmd+"\n")


	def launch(self):

		selected: str = self.rofi.display(
			self.prompt,
			self.mesg,
			self.options
		)

		if not selected: return

		self.parse(selected)


	def parse(self, selected: str):
		
		selected = selected.encode("ascii", "ignore").decode()

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
			return
		except PermissionError:
			self.show_error("Insufficient Permissions!")
			return

		try:
			proc.wait(1)
		except subprocess.TimeoutExpired:
			pass

		self.add_to_history(shlex.join(cmd))


	def execTerminal(self, cmd: list[str]):
		
		terminal = os.environ.get("TERMINAL")
		
		if not terminal:
			self.show_error(
				"Set a $TERMINAL env to specify a terminal."
			)
			exit(1)

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
	timed()
	c = RunPrompt()
	timed()
	c.launch()
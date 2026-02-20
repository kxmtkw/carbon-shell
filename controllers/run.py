from pathlib import Path
import subprocess, shlex
import os, time

from lib.rofi import RofiShell


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
		
		cmd = selected.encode("ascii", "ignore").decode()
		self.exec(cmd)

		
	def exec(self, cmd: str):
		try:
			subprocess.run(
				cmd,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				shell=True
			)
		except FileNotFoundError:
			self.show_error(f"Command not found: {cmd}")
			return
		except PermissionError:
			self.show_error("Insufficient Permissions!")
			return

		self.add_to_history(cmd)

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
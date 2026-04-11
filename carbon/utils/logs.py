from enum import Enum
from pathlib import Path
from datetime import datetime
from threading import Lock

from .color_print import Color
from .locked import locked
from .functions import writefile


class _Logger():


	class Level(Enum):
		debug = 0
		info = 1
		warning = 2
		critical = 3


	def __init__(self) -> None:

		self.log_colors = {
			self.Level.debug    : Color.cyan,
			self.Level.info     : Color.green,
			self.Level.warning  : Color.yellow,
			self.Level.critical : Color.red
		}
	
		self.log_file: Path
		self.startup_error_file: Path
		self.to_terminal: bool = True

		self.setOutfile("~/.carbon/logs/carbon.log")
		self.setStartupError("/tmp/carbon_startup_error.txt")

	
	def disableStdout(self) -> None:
		self.to_terminal = False

	@locked()
	def setOutfile(self, path: str) -> None:
		self.log_file = Path(path).expanduser()
		if not self.log_file.parent.exists():
			self.log_file.parent.mkdir(parents=True, exist_ok=True)
		if not self.log_file.exists():
			self.log_file.touch()
				
	@locked()
	def setStartupError(self, path: str) -> None:
		self.startup_error_file = Path(path).expanduser()
		if not self.startup_error_file.parent.exists():
			self.startup_error_file.parent.mkdir(parents=True, exist_ok=True)
		if not self.startup_error_file.exists():
			self.startup_error_file.touch()


	def log(self, sender: str, msg: str, level: Level) -> None:
		
		if self.to_terminal:
			self._terminal_log(sender, msg, level)

		self._file_log(sender, msg, level)


	def _terminal_log(self, sender: str, msg: str, level: Level) -> None:

		timestamp = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
		level = Color.colorify(f"[{level.name.upper()}]", self.log_colors[level])
		sender = Color.colorify(f"({sender})", Color.magenta)
		message = msg

		log_str = f"{timestamp} {level} {sender} {message}"
		print(log_str)


	def _file_log(self, sender: str, msg: str, level: Level) -> None:

		log_str = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level.name.upper()}] ({sender}) {msg}\n"

		with open(self.log_file, "a+") as file:
			file.write(log_str)


	def reportStartupError(self, sender: str, msg: str) -> None:
		"Reserved for only when a startup error needs to be reported."
		error_str = f"[Error] ({sender}) {msg}\n"
		writefile(self.startup_error_file, error_str)

	def extractStartupError(self) -> str:
		
		if not self.startup_error_file.exists():
			return "No startup error file found. The error was not reported by the daemon."
		
		with open(self.startup_error_file) as file:
			string = file.read()

		return string



logger = _Logger()

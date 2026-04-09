from enum import Enum
from pathlib import Path
from datetime import datetime
from threading import Lock

from .color_print import Color
from .locked import locked


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
		self.to_terminal: bool = True

		self.setOutfile("~/.carbon/logs/carbon.log")

	
	def disableStdout(self) -> None:
		self.to_terminal = False

	@locked()
	def setOutfile(self, path: str) -> None:
		self.log_file = Path(path).expanduser()
		if not self.log_file.parent.exists():
			self.log_file.parent.mkdir(parents=True, exist_ok=True)
		if not self.log_file.exists():
			self.log_file.touch()
				

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


logger = _Logger()

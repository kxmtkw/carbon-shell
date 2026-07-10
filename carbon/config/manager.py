from pathlib import Path
import toml
from typing import Any, Callable

from carbon.utils import FileWatcher

from .vars import _ConfigVar


class ConfigManager:

	ConfigVar: _ConfigVar = None

	def __init__(self, path: Path):

		self.configdir = path.expanduser()

		ConfigManager.ConfigVar = _ConfigVar(
			self.configdir,
			self.configdir / "state.toml",
			self.configdir / "data",
		)
		self._state = {}


		if not self.configdir.exists():
			self.configdir.mkdir(511, True)
		
		if not (self.configdir / "data").exists():
			(self.configdir / "data").mkdir()

		self._state_file = self.configdir / "state.toml"

		self._is_loading_needed = True

		if not self._state_file.exists():
			self.create()
			return
		

	def create(self):
		if not self._state_file.parent.exists():
			self._state_file.parent.mkdir(511, True, True)

		with open(self._state_file, "w") as file:
			toml.dump({}, file)


	@property
	def file(self) -> Path:
		return self._state_file

	def update(self, key: str, state: dict):
		self._state[key] = state


	def get(self, key: str) -> dict[str, Any] | None:
		return self._state.setdefault(key, None)
	

	def dump(self) -> str:
		string = toml.dumps(self._state) 
		return string

	def save(self):
		
		string = self.dump()
				
		with open(self._state_file, "w") as file:
			file.write(string)
		   

	def load(self) -> bool:
		
		with open(self._state_file) as file:
			try:
				self._state = toml.load(file)
				return True
			except toml.TomlDecodeError:
				self._state = {}
				return False


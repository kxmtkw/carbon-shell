import subprocess
from pathlib import Path

class Quickshell:
	"Class for communicating with the quickshell instance for carbon"

	class Error(Exception):
		def __init__(self, msg: str):
			self.msg = msg
			super().__init__(msg)


	def __init__(self):

		self.base_cmd = [
			"quickshell",
			"--config",
			Path("~/.carbon/shell/quickshell").expanduser(),
			"ipc",
			"call"
		]

	
	def start(self):

		output = subprocess.run("pidof 'quickshell --config ~/.carbon/shell/quickshell'", shell=True, capture_output=True, text=True)

		if output.returncode == 0:
			raise Quickshell.Error(f"quickshell is already running. (code: {output.returncode})")

		try:
			self._proc = subprocess.Popen(
				[
					"quickshell",
					"--config",
					Path("~/.carbon/shell/quickshell").expanduser(),
				], 
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,
				stdin=subprocess.DEVNULL,
				start_new_session=True
			)
		except Exception as e:
			raise Quickshell.Error(f"Failed to start quickshell. Reason: {e.__class__.__name__}::{str(e)}")
		

	def _call(self, *args) -> str:
		try:
			result = subprocess.run(self.base_cmd + list(args), capture_output=True, text=True, timeout=5)
			if result.returncode != 0:
				return ""
			return result.stdout.strip()
		except Exception as e:
			return ""
		

	def updateTheme(self):
		"Ask quickshell to reread the theme json file."
		self._call(
			"theme",
			"update"
		)

	def updateFont(self, font: str):
		"Ask quickshell to update the font."
		self._call(
			"style",
			"update_font",
			font
		)


	
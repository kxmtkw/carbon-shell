import subprocess
from pathlib import Path
from typing import Literal

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
		

	def kill(self):
		self._call("kill")


	def _call(self, *args) -> str:
		try:
			cmd = self.base_cmd + [str(arg) for arg in args]
			result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
			if result.returncode != 0:
				return ""
			return result.stdout.strip()
		except Exception as e:
			return ""
		

	def updateTheme(self):
		"Ask quickshell to reread the theme json file."
		self._call(
			"ipc",
			"call",
			"theme",
			"update"
		)

	def updateFont(self, font: str):
		"Ask quickshell to update the font."
		self._call(
			"ipc",
			"call",
			"style",
			"updateFont",
			font
		)


	def sendNotification(
		self,
		id: int,
		replaces_id: int,
		app_name: str,
		app_icon: str,
		summary: str,
		body: str,
		urgency: Literal[0, 1, 2],
		image: str,
		expire_timeout: int
	):
		"Send a notification to the quickshell notifier window."
		self._call(
			"ipc",
			"call",
			"notif",
			"show_notification",
			str(id),
			str(replaces_id),
			app_name,
			app_icon,
			summary,
			body,
			urgency,
			image,
			str(expire_timeout)
		)


	

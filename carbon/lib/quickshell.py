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
				self.base_cmd, 
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,
				stdin=subprocess.DEVNULL,
				start_new_session=True
			)
		except Exception as e:
			raise Quickshell.Error(f"Failed to start quickshell. Reason: {e.__class__.__name__}::{str(e)}")
		

	def kill(self):
		self._call("kill")


	def _call(self, *args) -> None:
		cmd = self.base_cmd + [str(arg) for arg in args]
		subprocess.Popen(
			cmd,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
		

	def setPanelMode(self, mode: Literal["normal", "hidden", "bypass"] = "normal"):
		"Change Panel modes."
		self._call(
			"ipc",
			"call",
			"panel",
			mode
		)


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
			"update_font",
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


	

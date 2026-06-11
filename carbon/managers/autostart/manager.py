from dataclasses import dataclass, replace
from typing import Any, Callable, Dict, Literal

from carbon.managers.base import BaseManager

from carbon.utils import logger, CarbonError, Notify, shellrun, clamp



class AutostartManager(BaseManager):


	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		commands: list[str]


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State]):
		super().__init__(internalDispatch, getManagerState)
		
		self.state = self.State(
			commands=[]
		)

		self.core_commands = [
			"awww-daemon", # wallpaper daemon
			"wl-paste --watch cliphist store", # clipboard daemon
			"systemctl --user start hyprpolkitagent" # polkit agent
		]

		self.are_core_executed = False
		self.are_user_executed = False

	
	def start(self):
		self.execCoreCommands()


	def end(self):
		pass
	

	def name(self) -> str:
		return "autostart"
	

	def handlers(self) -> Dict[str, Callable]:
		return {
			"restart-user": self.restartUser,
			"list": self.listCommands 
		}
	

	def getState(self) -> State:
		return replace(self.state)
	

	def setState(self, state: State):
		self.state = state
		self.execUserCommands()
	

	def getHelp(self) -> str:
		return _help
	

	def restartUser(self):
		self.are_user_executed = False
		self.execUserCommands()
		return "Restarting user commands."


	def listCommands(self):
		return f"(core) {self.core_commands}\n(user) {self.state.commands}"
	

	def execCoreCommands(self):

		if self.are_core_executed: return
		
		logger.info("autostart", "Starting up core commands..")
		for cmd in self.core_commands:
			self.execCommand(cmd)

		self.are_core_executed = True


	def execUserCommands(self):
		
		if self.are_user_executed: return

		logger.info("autostart", "Starting up user commands..")
		for cmd in self.state.commands:
			self.execCommand(cmd)

		self.are_user_executed = True


	def execCommand(self, cmd: str):
		logger.debug("autostart", f"Running: {cmd}")
		shellrun(cmd, wait=False)


_help = """
==> autostart
Starts up specified commands on startup of shell.

handlers:

	> restart-user
		Restart all the user listed commands.
		Useful when updating the autostart's state.

	> list
		List all commands executed by the autostart.
"""

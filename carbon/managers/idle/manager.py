from dataclasses import dataclass, replace

from carbon.managers.base import BaseManager
from carbon.utils import ProcessManager, Notify, logger

_help = """
Help for manager: idle

	> on
		Turn on the idle manager.
	> off
		Turn off the idle manager.
	> toggle
		Toggle the idle manager.
"""

class IdleManager(BaseManager):

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		toggled: bool


	def __init__(self):
		super().__init__()

		self.state = IdleManager.State(
			toggled=True
		)

		self.hypridle = ProcessManager("hypridle", only_one=True)


	def handlers(self):
		return {
			"on": lambda: self.toggleIdle(True),
			"off": lambda: self.toggleIdle(False),
			"toggle": lambda: self.toggleIdle(not self.state.toggled),
		}


	def start(self):
		self.hypridle.start()


	def end(self):
		self.toggleIdle(False)


	def name(self):
		return "idle"


	def getState(self) -> State:
		return replace(self.state)


	def setState(self, state: State):
		self.toggleIdle(state.toggled)


	def getHelp(self):
		return _help


	def toggleIdle(self, on: bool):

		self.state.toggled = on

		if self.state.toggled:

			if not self.hypridle.poll(0.1):
				self.hypridle.start()
				logger.log("idle", "Idle manager turned on.", logger.Level.info)

			return "Idle manager turned on."
			
		else:

			if self.hypridle.poll(0.1):
				self.hypridle.kill()
				logger.log("idle", "Idle manager turned off.", logger.Level.info)
				Notify("Idle", "Idle manager turned off.")

			return "Idle manager turned off."

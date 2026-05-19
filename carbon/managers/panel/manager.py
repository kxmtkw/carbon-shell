from dataclasses import dataclass, replace
from typing import Literal
from typing import Literal

from carbon.managers.base import BaseManager

from carbon.lib.quickshell import Quickshell

from carbon.utils import logger, CarbonError, Notify, shellrun, clamp



class PanelManager(BaseManager):


	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		mode: Literal["show", "hide", "bypass"]
		position: Literal["top", "bottom"]


	def __init__(self):
		super().__init__()
		self.state = self.State(
			mode="show",
			position="bottom"
		)
		
		self.qs = Quickshell()

	
	def setState(self, state: PanelManager.State):
		self.setMode(state.mode)


	def getState(self):
		return replace(self.state)
	

	def handlers(self):
		return {
			"set-mode": self.setMode,
			"set-position": self.setPosition
		}
	

	def end(self):
		pass


	def setMode(self, mode: Literal["show", "hide", "bypass"]):
		
		if self.state.mode == mode:
			return f"Panel already in {mode} mode."
		
		if mode == "show":
			self.state.mode = mode
			self.qs.setPanelMode("normal")
			logger.log("panel", "Panel mode set to show.", logger.Level.info)
			return "Panel shown."
		
		elif mode == "hide":
			self.state.mode = mode
			self.qs.setPanelMode("hidden")
			logger.log("panel", "Panel mode set to hide.", logger.Level.info)
			return "Panel hidden."
		
		elif mode == "bypass":
			self.state.mode = mode
			self.qs.setPanelMode("bypass")
			logger.log("panel", "Panel mode set to bypass.", logger.Level.info)
			return "Panel bypassing."

		else:
			raise CarbonError("Invalid panel mode. Valid modes are: show, hide, bypass.")
		
		
	def setPosition(self, position: Literal["top", "bottom"]):
		
		if self.state.position == position:
			return f"Panel already positioned at {position}."
		
		if position == "top":
			self.state.position = "top"
			self.qs.setPanelPosition("movetotop")
			logger.log("panel", "Panel moved to top.", logger.Level.info)
			return "Panel moved to top."
		
		elif position == "bottom":
			self.state.position = "bottom"
			self.qs.setPanelPosition("movetobottom")
			logger.log("panel", "Panel moved to bottom.", logger.Level.info)
			return "Panel moved to bottom."
		
		else:
			raise CarbonError("Invalid panel position. Valid positions are: top, bottom")
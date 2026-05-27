from dataclasses import dataclass, replace
from typing import Any, Callable, Literal

from carbon.managers.base import BaseManager

from carbon.lib.quickshell import Quickshell

from carbon.utils import logger, CarbonError, Notify, shellrun, clamp



class PanelManager(BaseManager):


	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		mode: Literal["show", "hide", "bypass"]
		position: Literal["top", "bottom"]


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None]):
		super().__init__(internalDispatch)
		self.state = self.State(
			mode="show",
			position="bottom"
		)
		
		self.qs = Quickshell()
		self.last_active_mode: Literal["show", "hide"] = "show"


	def start(self):
		pass


	def end(self):
		pass


	def name(self):
		return "panel"


	def handlers(self):
		return {
			"set-mode": self.setMode,
			"toggle-bypass": self.toggleBypassView,
			"set-position": self.setPosition
		}
	

	def setState(self, state: PanelManager.State):
		self.setMode(mode=state.mode)
		self.setPosition(position=state.position)


	def getState(self):
		return replace(self.state)


	def getHelp(self):
		return _help
	

	def setMode(self, *, mode: Literal["show", "hide", "bypass"]):
		
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
		
		
	def toggleBypassView(self, *, state: Literal["on", "off"]):

		if state == "off":
			self.setMode(mode=self.last_active_mode)
			return f"Switched back to {self.state.mode} mode."
		
		elif state == "on":
			self.last_active_mode = self.state.mode if self.state.mode != "bypass" else "show"
			self.setMode(mode="bypass")

		else:
			raise CarbonError(f"Invalid state: {state}. Either 'on' or 'off'.")

		return "Switched to bypass mode."
	
		
	def setPosition(self, *, position: Literal["top", "bottom"]):
		
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
		

_help = """
==> panel
Configure the panel.

handlers:

	> set-mode --mode [show|hide|bypass]
		Set panel mode.

	> toggle-bypass --state [on|off]
		Switch between bypass mode and last active mode.

	> set-position --position [top|bottom]
		Set panel position.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, Literal

from carbon.managers.base import BaseManager

from carbon.utils import logger, CarbonError, Notify, procrun, shellrun

from .styles import writeLockStyle


class LockScreenManager(BaseManager):

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		style: Literal["screenshot", "image", "wallpaper"]
		image: str


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State]):
		super().__init__(internalDispatch, getManagerState)
		self.state: LockScreenManager.State = LockScreenManager.State(
			style="screenshot",
			image="~/.carbon/assets/default_wallpaper.jpg"
		)
		self.config_file = "~/.config/hypr/hyprlock/hyprlock-theme.conf"


	def start(self):
		pass


	def end(self):
		pass

	
	def name(self):
		return "lockscreen"


	def handlers(self) -> Dict[str, Callable]:
		return {
			"lock": self.lock,
			"set-style": self.setStyle
		}


	def getState(self) -> State:
		return replace(self.state)
	

	def setState(self, state: State):
		self.setStyle(style=state.style, img=state.image)


	def getHelp(self):
		return _help

	# handler
	def lock(self):
		logger.log("lockscreen", "Locking screen...", logger.Level.info)
		procrun(["hyprlock"], wait=False)
		return "Bye Bye!"

	# handler	
	def setStyle(self, *, style: Literal["screenshot", "image", "wallpaper"], img: str| None = None):

		match style:

			case "screenshot":
				self.state.style = "screenshot"
				writeLockStyle(self.config_file, "screenshot")

			case "image":
				self.state.style = "image"

				if img is None:
					if self.state.image is None:
						raise CarbonError(f"File not given!")
					img = self.state.image

				if not Path(img).exists():
					raise CarbonError(f"File not found: {img}")
				
				self.state.image = img
				shellrun(f"cp {img} ~/.carbon/user/lockscreen")
				writeLockStyle(self.config_file, "~/.carbon/user/lockscreen")

			case "wallpaper":
				self.state.style = "wallpaper"
				writeLockStyle(self.config_file, "~/.carbon/user/wall")

			case _:
				raise CarbonError(f"Unknown lock style: {style}")
			
		logger.log("lockscreen", f"Style set to {style}. {img if style == 'image' else ''}", logger.Level.info)

		return f"Lockscreen style set to {style}."
				


_help = """
==> lockscreen
Set lockscreen styles.

handlers:

	> lock
		Trigger the lockscreen.

	> set-style --style [screenshot|image|wallpaper] --img [path] (if style = image)
		Set the lockscreen style. --img argument only needed when --style is image
"""

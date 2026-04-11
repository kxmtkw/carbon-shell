from pathlib import Path
from typing import Any, Literal
from threading import Lock
from dataclasses import dataclass

from carbon.managers.base import BaseManager
from carbon.utils import CarbonError, procrun, isValidHex, locked, logger

from carbon.state import Defaults
from .updater import ThemeUpdater
from .material import MaterialColors


themeLock = Lock()


class ThemeManager(BaseManager):

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		mode: Literal["dark", "light"]
		source: Literal["wallpaper", "hex"]
		wallpaper: str
		hex: str
		variant: Literal["ash", "coal", "graphite", "diamond"]
		contrast: float | int
		font: str
		face: str


	def __init__(self):
		self.updater = ThemeUpdater()
		self.material = MaterialColors()

		self.dark_theme = {}
		self.light_theme = {}

		self.state = self.State(
			mode=Defaults.theme_mode,
			source=Defaults.theme_source,
			wallpaper=Defaults.theme_wallpaper,
			hex=Defaults.theme_hex,
			variant=Defaults.theme_variant,
			contrast=Defaults.theme_contrast,
			font=Defaults.theme_font,
			face=Defaults.theme_face,
		)

		self._handlers = {
			"set-wallpaper": self.setWallpaper,
			"update-theme": self.updateTheme,
			"switch-mode": self.switchMode,
			"toggle-mode": self.toggleMode,
			"change-font": self.changeFont,
			"set-face": self.setFace,
		}

		super().__init__()


	def handlers(self) -> dict[str, callable]:
		return self._handlers
	

	@locked(themeLock)
	def setWallpaper(self, *, img: str) -> str:
		return self._setWallpaper_nolock(img=img)
	

	def _setWallpaper_nolock(self, *, img: str) -> str:

		path = Path(img).expanduser()

		if not path.exists():
			raise CarbonError(f"File not found: {path}") 
		
		success, output = procrun(["swww", "img", "--transition-type", "outer", path])

		if success:
			self.state.wallpaper = img
			logger.log(
				"theme",
				f"Wallpaper updated: {img}",
				logger.Level.info
			)
			return "Wallpaper updated."
		else:
			raise CarbonError(f"Failed to change wallpaper: swww failure\n{output}")
		
	
	@locked(themeLock)
	def updateTheme(
			self, 
			*, 
			mode: Literal["dark", "light"] | None  = None,
			variant: Literal["ash", "coal", "graphite", "diamond"] | None  = None,
			contrast: float | None  = None,
			source: Literal["wallpaper", "hex"] | None  = None,
			hex: str | None = None,
			img: str| None  = None
		) -> str:
		
		if not mode: mode = self.state.mode
		if not variant: variant = self.state.variant
		if not contrast: contrast = self.state.contrast
		if not source: source = self.state.source
		if not hex: hex = self.state.hex
		if not img: img = self.state.wallpaper

		
		match variant:
			case "ash":
				variant_type = MaterialColors.Variant.ash
			case "coal":
				variant_type = MaterialColors.Variant.coal
			case "graphite":
				variant_type = MaterialColors.Variant.graphite
			case "diamond":
				variant_type = MaterialColors.Variant.diamond
			case _:
				raise CarbonError(f"Invalid variant type: {variant}")


		if source == "wallpaper":

			if not Path(img).expanduser().exists():
				raise CarbonError(f"Image not found: {img}")
			self.material.generateFromImage(Path(img).expanduser(), contrast, variant_type)

			
			self._setWallpaper_nolock(img=img)

		elif source == "hex":

			if not isValidHex(hex): 
				raise CarbonError(f"Invalid hex value: {hex}")
			self.material.generateFromColor(hex, contrast, variant_type)
			
		else:
			raise CarbonError(f"Invalid theme source: {source}")
		

		self.dark_theme = self.material.darkMapping
		self.light_theme = self.material.lightMapping

		if mode == "light":
			self.updater.updateColors(self.light_theme)
		elif mode == "dark":
			self.updater.updateColors(self.dark_theme)
		else:
			raise CarbonError(f"Invalid theme mode: {mode}")
		

		self.state.mode = mode
		self.state.variant = variant
		self.state.contrast = contrast
		self.state.source = source
		self.state.wallpaper = img
		self.state.hex = hex

		logger.log(
			"theme",
			f"Theme updated!",
			logger.Level.info
		)

		logger.log(
			"theme",
			f"Theme Desc: Mode({mode}) Variant({variant}) Source({source}) Contrast({contrast}) Hex({hex}) Wallpaper({img})",
			logger.Level.debug
		)

		return "Theme updated successfully."
	

	@locked(themeLock)
	def switchMode(
			self, 
			mode: Literal["dark", "light"]
		) -> str:

		if mode == self.state.mode:
			return f"Already in {mode} mode."
		
		if mode == "light":
			self.updater.updateColors(self.light_theme)
		elif mode == "dark":
			self.updater.updateColors(self.dark_theme)
		else:
			raise CarbonError(f"Invalid theme mode: {mode}")
		
		self.state.mode = mode

		logger.log(
			"theme",
			f"Switched to {self.state.mode} mode.",
			logger.Level.info
		)

		return f"Switched to {mode} mode successfully."
	

	@locked(themeLock)
	def toggleMode(self) -> str:

		if self.state.mode == "light":
			self.updater.updateColors(self.dark_theme)
			self.state.mode = "dark"
		else:
			self.updater.updateColors(self.light_theme)
			self.state.mode = "light"

		logger.log(
			"theme",
			f"Switched to {self.state.mode} mode.",
			logger.Level.info
		)

		return f"Switched to {self.state.mode} mode successfully."


	@locked(themeLock)
	def changeFont(self, font: str) -> str:
		self.updater.updateFont(font)
		logger.log(
			"theme",
			f"Font updated to {font}.",
			logger.Level.info
		)
		self.state.font = font
		return f"Font changed to {font} successfully."
	

	@locked(themeLock)
	def setFace(self, img: str):
		self.updater.updateFace(img)
		logger.log(
			"theme",
			f"Face updated to {img}.",
			logger.Level.info
		)
		self.state.face = img
		
		return f"Face image updated successfully."
	

	def setState(self, state: State):
		self.updateTheme(
			mode     = state.mode,
			variant  = state.variant,
			contrast = state.contrast,
			source   = state.source,
			hex      = state.hex,
			img      = state.wallpaper,
		)
		self.changeFont(font = state.font)
		self.setFace(img     = state.face)

		logger.log("theme", "Loaded theme state.", logger.Level.info)


	def getState(self) -> State:
		return self.state
from pathlib import Path
from typing import Any, Callable, Literal
from threading import Lock
from dataclasses import dataclass, replace

from carbon.managers.base import BaseManager
from carbon.utils import CarbonError, procrun, isValidHex, locked, logger

from .updater import ThemeUpdater
from .material import MaterialColors



class ThemeManager(BaseManager):

	themeLock = Lock()

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
		wallpaper_animation: Literal["wipe", "left", "right", "top", "bottom", "outer", "center", "any", "fade", "random"]


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None]):

		self.updater = ThemeUpdater()
		self.material = MaterialColors()

		self.dark_theme = {}
		self.light_theme = {}

		self.state = self.State(
			mode="dark",
			source="wallpaper",
			wallpaper="~/.carbon/assets/default_wallpaper.jpg",
			hex="#82a0c0",
			variant="graphite",
			contrast=0.5,
			font="Iosevka",
			face="~/.carbon/assets/default_face.jpg",
			wallpaper_animation="center"
		)

		super().__init__(internalDispatch)


	def start(self):
		pass


	def end(self):
		pass

	
	def name(self):
		return "theme"
	

	def handlers(self) -> dict[str, callable]:
		return {
			"set-wallpaper": self.setWallpaper,
			"update-theme": self.updateTheme,
			"switch-mode": self.switchMode,
			"toggle-mode": self.toggleMode,
			"change-font": self.changeFont,
			"set-face": self.setFace,
			"set-wallpaper-animation": self.setWallpaper_animation,
			"set-shell-style": self.setShellStyle
		}
	

	def setState(self, state: State):

		self.setWallpaper_animation(style = state.wallpaper_animation)

		self.updateTheme(
			mode     = state.mode,
			variant  = state.variant,
			contrast = state.contrast,
			source   = state.source,
			hex      = state.hex,
			img      = state.wallpaper,
		)

		if self.state.source != "wallpaper":
			self.setWallpaper(img=state.wallpaper)

		self.changeFont(font = state.font)
		self.setFace(img = state.face)
		
		logger.log("theme", "Loaded theme state.", logger.Level.info)


	def getState(self) -> State:
		return replace(self.state)
	

	def getHelp(self):
		return _help
	

	@locked(themeLock)
	def setWallpaper(self, *, img: str) -> str:
		return self._setWallpaper_nolock(img=img)
	

	def _setWallpaper_nolock(self, *, img: str) -> str:
		self.updater.updateWallpaper(img, self.state.wallpaper_animation)
		self.state.wallpaper = img
		logger.log(
				"theme",
				f"Wallpaper updated: {img}",
				logger.Level.info
			)
		return "Wallpaper updated."
	
	
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

		
		try:
			contrast = float(contrast)
		except ValueError:
			raise CarbonError("Invalid contrast value. Expected integar or decimal.")
		
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
			*,
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
	def changeFont(self, *, font: str) -> str:
		self.updater.updateFont(font)
		logger.log(
			"theme",
			f"Font updated to {font}.",
			logger.Level.info
		)
		self.state.font = font
		return f"Font changed to {font} successfully."
	

	@locked(themeLock)
	def setFace(self, *, img: str):
		self.updater.updateFace(img)
		logger.log(
			"theme",
			f"Face updated to {img}.",
			logger.Level.info
		)
		self.state.face = img
		
		return f"Face image updated successfully."
	

	@locked(themeLock)
	def setWallpaper_animation(self, *, style: str):
		
		if not hasattr(self, "wallpaper_animation_styles"):
			self.wallpaper_animation_styles = ("wipe", "left", "right", "top", "bottom", "outer", "center", "any", "fade", "random")

		if style not in self.wallpaper_animation_styles:
			raise CarbonError(f"Invalid style. Allowed styles include:\n{self.wallpaper_animation_styles}")
		
		self.state.wallpaper_animation = style

		logger.log(
			"theme",
			f"Wallpaper animation updated to {style}.",
			logger.Level.info
		)

		return "Wallpaper animation style updated."
	

	@locked(themeLock)
	def setShellStyle(
		self,
		*,
		style:  Literal["material", "modern"]
	):
		
		if not hasattr(self, "_shell_styles"):
			self._shell_styles = ("material", "modern")

		if style not in self._shell_styles:
			raise CarbonError(f"Invalid style. Allowed styles include:\n{self._shell_styles}")
		
		self.updater.setShellStyle(style)

		return f"Shell style updated to {style}"


_help = """
==> theme
Change and update the shell theme.

handlers:

	> update-theme 
	--mode [dark|light]
	--variant [ash|coal|graphite|diamond]
	--contrast [decimal]
	--source [wallpaper|hex]
	--hex [hexcode]
	--img [path]
		Generate a theme from a source.
		Not all arguments are needed. Any missing arguments will just use the previous ones.
		--mode changes the mode of the theme.
		--variant changes the theme variant.
			ash: desaturated scheme; coal: monotone scheme; 
			graphite: true-to-source scheme; diamond: true material scheme;
		--hex is considered when --source is hex. 
		--img will change the wallpaper as well.

	> set-shell-style --style [style]
		Set the style of the shell.
		Valid styles include: material, modern

	> switch-mode --mode [dark|light]
		Switch between light and dark mode.

	> toggle-mode
		Toggle light or dark mode.

	> change-font --font [name]
		Change the shell font.

	> set-face --img [path]
		Update the profile picture for the shell.

	> set-wallpaper --img [path]
		Set wallpaper.

	> set-wallpaper-animation --style [style]
		Set wallpaper animation style.
		Valid styles include: wipe, left, right, top, bottom, outer, center, any, random, fade.
"""

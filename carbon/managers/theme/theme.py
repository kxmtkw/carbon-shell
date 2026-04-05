from pathlib import Path
from typing import Any, Literal
from threading import Lock

from carbon.managers.base import BaseManager
from carbon.utils import CarbonError, procrun, is_valid_hex, locked

from carbon.state import Defaults
from .updater import ThemeUpdater
from .material import MaterialColors

themeLock = Lock()

class ThemeManager(BaseManager):


	def __init__(self):
		self.updater = ThemeUpdater()
		self.material = MaterialColors()

		self.dark_theme = {}
		self.light_theme = {}

		self.current_source = Defaults.theme_source
		self.current_wallpaper = Defaults.theme_wallpaper
		self.current_hex = Defaults.theme_hex
		self.current_mode = Defaults.theme_mode
		self.current_variant = Defaults.theme_variant
		self.current_contrast = Defaults.theme_contrast
		self.current_font = Defaults.theme_font

		self._handlers = {
			"set-wallpaper": self.setWallpaper,
			"update-theme": self.updateTheme,
			"switch-mode": self.switchMode,
			"toggle-mode": self.toggleMode,
			"change-font": self.changeFont
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
			self.current_wallpaper = img
			return "Wallpaper updated."
		else:
			raise CarbonError(f"Failed to change wallpaper: swww failure\n{output}")
		
	
	@locked(themeLock)
	def updateTheme(
			self, 
			*, 
			mode: Literal["dark", "light"] = None,
			variant: Literal["ash", "coal", "graphite", "diamond"] = None,
			contrast: float = None,
			source: Literal["wallpaper", "hex"] = None,
			hex: str = None,
			img: str = None
		) -> str:
		
		if not mode: mode = self.current_mode
		if not variant: variant = self.current_variant
		if not contrast: contrast = self.current_contrast
		if not source: source = self.current_source
		if not hex: hex = self.current_hex
		if not img: img = self.current_wallpaper

		
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
			self.material.generate_from_image(Path(img).expanduser(), contrast, variant_type)

			
			self._setWallpaper_nolock(img=img)

		elif source == "hex":

			if not is_valid_hex(hex): 
				raise CarbonError(f"Invalid hex value: {hex}")
			self.material.generate_from_color(hex, contrast, variant_type)
			
		else:
			raise CarbonError(f"Invalid theme source: {source}")
		

		self.dark_theme = self.material.darkMapping
		self.light_theme = self.material.lightMapping

		if mode == "light":
			self.updater.update_colors(self.light_theme)
		elif mode == "dark":
			self.updater.update_colors(self.dark_theme)
		else:
			raise CarbonError(f"Invalid theme mode: {mode}")
		

		self.current_mode = mode
		self.current_variant = variant
		self.current_contrast = contrast
		self.current_source = source
		self.current_wallpaper = img
		self.current_hex = hex

		return "Theme updated successfully."
	

	@locked(themeLock)
	def switchMode(
			self, 
			mode: Literal["dark", "light"]
		) -> str:

		if mode == self.current_mode:
			return f"Already in {mode} mode."
		
		if mode == "light":
			self.updater.update_colors(self.light_theme)
		elif mode == "dark":
			self.updater.update_colors(self.dark_theme)
		else:
			raise CarbonError(f"Invalid theme mode: {mode}")
		
		self.current_mode = mode
		return f"Switched to {mode} mode successfully."
	

	@locked(themeLock)
	def toggleMode(self) -> str:

		if self.current_mode == "light":
			self.updater.update_colors(self.dark_theme)
			self.current_mode = "dark"
		else:
			self.updater.update_colors(self.light_theme)
			self.current_mode = "light"

		return f"Switched to {self.current_mode} mode successfully."


	@locked(themeLock)
	def changeFont(self, font: str) -> str:
		self.updater.update_font(font)
		self.current_font = font
		return f"Font changed to {font} successfully."
	

	def loadState(self, state: dict[str, Any]):
		self.current_mode = state.get("current_mode", Defaults.theme_mode)
		self.current_variant = state.get("current_variant", Defaults.theme_variant)
		self.current_contrast = state.get("current_contrast", Defaults.theme_contrast)
		self.current_source = state.get("current_source", Defaults.theme_source)
		self.current_hex = state.get("current_hex", Defaults.theme_hex)
		self.current_wallpaper = state.get("current_wallpaper", Defaults.theme_wallpaper)
		self.current_font = state.get("current_font", Defaults.theme_font)

		self.updateTheme()
		self.setWallpaper(img=self.current_wallpaper)
		self.changeFont(font=self.current_font)

	
	def saveState(self) -> dict[str, Any]:
		return {
			"current_mode": self.current_mode,
			"current_variant": self.current_variant,
			"current_contrast": self.current_contrast,
			"current_source": self.current_source,
			"current_hex": self.current_hex,
			"current_wallpaper": self.current_wallpaper,
			"current_font": self.current_font
		}

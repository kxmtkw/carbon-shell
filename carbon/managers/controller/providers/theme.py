from pathlib import Path
import time

from carbon.lib.rofi import RofiShell
from carbon.managers.controller.base import BaseController

from carbon.utils import CarbonError, isValidHex, isValidNumber
from carbon.managers.theme import ThemeManager



class Theme(BaseController):

	def __init__(self, themer: ThemeManager):
		self.themer = themer
		self.theme_state: ThemeManager.State = themer.getState()

		self.rasi_main = "~/.carbon/shell/rofi/theme/main.rasi"
		self.rasi_entry = "~/.carbon/shell/rofi/theme/entry.rasi"
		self.rasi_mesg = "~/.carbon/shell/rofi/theme/mesg.rasi"
		self.rasi_wallpaper = "~/.carbon/shell/rofi/theme/wallpaper.rasi"
		
		self.rofi = RofiShell(self.rasi_main)

		self.wallpapers: list[str] = []

		self.main_options = [
			f"{Icons.dark}  Toggle dark mode",
			f"{Icons.wallpaper}  Select wallpaper",
			f"{Icons.color}  Select color",
			f"{Icons.variant}  Update variant",
			f"{Icons.source}  Update theme source",
			f"{Icons.contrast}  Change contrast",
			f"{Icons.face}  Change profile picture",
			f"{Icons.fonts}  Change Font"
		]


	def loadWallpapers(self):
		self.wallpapers = Utils.getWallpapers(
			["~/Pictures/Wallpapers"]
		)

	
	def launch(self):
		self.is_running = True
		self.current = self.showMainMenu

		while self.is_running:
			self.theme_state = self.themer.getState()
			self.current()


	def close(self):
		self.is_running = False
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass


	def display(self, prompt: str, mesg: str):
		self.rofi.updateTheme(self.rasi_mesg)
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=prompt,
			mesg=mesg
		)
		self.rofi.wait()


	def showMainMenu(self):

		self.rofi.updateTheme(self.rasi_main)

		self.main_options[0] = f"{Icons.light}  Toggle light mode" if self.theme_state.mode == "dark" else f"{Icons.dark}  Toggle dark mode"

		options = self.main_options.copy()
		options[0] = RofiShell.markActive(options[0])
		
		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Theme",
			options=options
		)

		selected = self.rofi.wait()

		options = self.main_options

		if not selected: self.close()

		elif selected == options[0]:
			self.themer.toggleMode()

		elif selected == options[1]:
			self.current = self.showWallpaperMenu

		elif selected == options[2]:
			self.current = self.showColorMenu

		elif selected == options[3]:
			self.current = self.showVariantMenu

		elif selected == options[4]:
			self.current = self.showSourceMenu

		elif selected == options[5]:
			self.current = self.showContrastMenu

		elif selected == options[6]:
			self.current = self.showFaceMenu

		else: 
			self.current = self.showFontMenu

		


	def showWallpaperMenu(self):
		
		self.rofi.updateTheme(self.rasi_wallpaper)

		self.loadWallpapers()

		if len(self.wallpapers) == 0:
			raise CarbonError("No wallpapers to show.") # todo: add visual error message insteads

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Set Wallpaper",
			options= self.wallpapers
		)

		selected: str = self.rofi.wait()
		self.current = self.showMainMenu 
		if not selected:
			return

		self.themer.setWallpaper(img=selected)

		if self.theme_state.source == "wallpaper":
			self.themer.updateTheme(img=selected)

		time.sleep(0.6) # animation finishes

	def showColorMenu(self):
		
		self.rofi.updateTheme(self.rasi_entry)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter a hex code (current:{self.theme_state.hex})"
		)

		entered = self.rofi.wait().strip()

		self.current = self.showMainMenu 
		if not entered: 
			return

		if entered == self.theme_state.hex: return

		if not isValidHex(entered):
			self.display(f"{Icons.error} ", f"Invalid hex value: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			return

		self.themer.updateTheme(hex=entered)


	def showSourceMenu(self):
		
		options = [
			f"{Icons.wallpaper}  From wallpaper",
			f"{Icons.color}  From color",
		]

		if self.theme_state.source == "wallpaper":
			options[0] = RofiShell.markActive(options[0])
		else:
			options[1] = RofiShell.markActive(options[1])
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Source",
			options= options
		)

		selected: str = self.rofi.wait()


		self.current = self.showMainMenu 
		if not selected:
			return

		if selected == options[0]:
			source = "wallpaper"
		else:
			source = "hex"		
			
		if source == self.theme_state.source: return

		self.themer.updateTheme(source=source)


	def showVariantMenu(self):

		options = [
			"[1] Ash",
			"[2] Coal",
			"[3] Graphite",
			"[4] Diamond"
		]

		current = self.theme_state.variant
		if current == "ash":
			options[0] = RofiShell.markActive(options[0])
		elif current == "coal":
			options[1] = RofiShell.markActive(options[1])
		elif current == "graphite":
			options[2] = RofiShell.markActive(options[2])
		else:
			options[3] = RofiShell.markActive(options[3])
			
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Variant",
			options= options
		)

		selected: str = self.rofi.wait()

		self.current = self.showMainMenu 
		if not selected: 
			return

		selected = selected.split("]")[-1].strip().lower()

		if selected == current: return

		self.themer.updateTheme(variant=selected)
		


	def showContrastMenu(self):
		
		self.rofi.updateTheme(self.rasi_entry)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter contrast value (current:{round(self.theme_state.contrast, 2)})"
		)

		entered = self.rofi.wait()

		self.current = self.showMainMenu 
		if not entered: return

		if not isValidNumber(entered):
			self.display(f"{Icons.error} ", f"Invalid number: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			return
		
		contrast = float(entered)

		self.themer.updateTheme(contrast=contrast)


	def showFaceMenu(self):

		self.rofi.updateTheme(self.rasi_entry)

		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Profile Picture",
			mesg=f"Enter a filepath\n(current:{self.theme_state.face})"
		)

		entered = self.rofi.wait().strip()

		self.current = self.showMainMenu 
		if not entered: return
		
		path = Path(entered).expanduser()

		if not path.exists():
			self.display(f"{Icons.error} ", f"File not found: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			return

		if path == self.theme_state.face: return
		
		self.themer.setFace(img=entered)


	def showFontMenu(self):
		return
	
		options = get_fonts()

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Fonts",
			options= options
		)

		selected: str = self.rofi.wait()

		self.current = self.showMainMenu 
		if not selected: self.close()

		selected = selected.split("]")[-1].strip().lower()

		font = extract_font_from_rofi(selected)
		Theme.set_font(font)

		CarbonConfig.set("theme.font", font)


class Icons:
    light = ""
    dark = ""
    wallpaper = "󰟾"
    contrast = "󰆗"
    variant = ""
    color = ""
    source = "󰜘"
    face = ""
    error = ""
    fonts = ""


class Utils:

	def getWallpapers(sources: list[str] | str) -> list[str]:

		wallpapers: list[str] = []

		# Getting Wallpaper Source dirs
		wallpaper_paths: list[Path] = []

		# Adding paths
		if isinstance(sources, str):
			wallpaper_paths.append(Path(sources).expanduser())
		else:
			for item in sources:
				if not isinstance(item, str): continue
				wallpaper_paths.append(Path(item).expanduser())

		# Checking paths
		for item in wallpaper_paths:
			if not item.exists():
				CarbonError(f"Wallpaper source directory does not exist: '{item.absolute}' ")
				continue

			if not item.is_dir():
				CarbonError(f"Wallpaper source is not a directory: '{item.absolute}' ")

			images = Utils.getImages(item)

			wallpapers.extend(images)

		wallpapers.sort()


		return wallpapers


	def getImages(directory: Path) -> list[str]:

		images = []
		
		for item in directory.iterdir():
			if item.is_file():
				absolute = item.absolute()
				option = RofiShell.markWithIcon(absolute, absolute)
				images.append(option)

		return images

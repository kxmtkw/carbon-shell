from pathlib import Path
import time

from carbon.lib.rofi import RofiShell
from carbon.managers.controller.base import BaseController

from carbon.utils import CarbonError, is_valid_hex, is_valid_number
from carbon.managers.theme import ThemeManager



class Theme(BaseController):

	def __init__(self, themer: ThemeManager):
		self.themer = themer

		self.rasi_main = "~/.carbon/shell/rofi/theme/main.rasi"
		self.rasi_entry = "~/.carbon/shell/rofi/theme/entry.rasi"
		self.rasi_mesg = "~/.carbon/shell/rofi/theme/mesg.rasi"
		self.rasi_wallpaper = "~/.carbon/shell/rofi/theme/wallpaper.rasi"
		
		self.rofi = RofiShell(self.rasi_main)

		self.wallpapers: list[str] = []


	def load_wallpapers(self):
		self.wallpapers = Utils.get_wallpapers(
			["~/Pictures/Wallpapers"]
		)

	
	def launch(self):
		self.is_running = True
		self.current = self.show_main_menu

		while self.is_running:
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


	def show_main_menu(self):

		self.rofi.updateTheme(self.rasi_main)

		options = [
			f"{Icons.light}  Toggle light mode" if self.themer.current_mode == "dark" else f"{Icons.dark}  Toggle dark mode",
			f"{Icons.wallpaper}  Select wallpaper",
			f"{Icons.color}  Select color",
			f"{Icons.variant}  Update variant",
			f"{Icons.source}  Update theme source",
			f"{Icons.contrast}  Change contrast",
			f"{Icons.face}  Change profile picture",
			f"{Icons.fonts}  Change Font"
		]

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Theme",
			options=options
		)

		selected = self.rofi.wait()
		
		if not selected: self.close()

		elif selected == options[0]:
			self.themer.toggleMode()

		elif selected == options[1]:
			self.current = self.show_wallpaper_menu

		elif selected == options[2]:
			self.current = self.show_color_menu

		elif selected == options[3]:
			self.current = self.show_variant_menu

		elif selected == options[4]:
			self.current = self.show_source_menu

		elif selected == options[5]:
			self.current = self.show_contrast_menu

		elif selected == options[6]:
			self.current = self.show_face_menu

		else: 
			self.current = self.show_font_menu


	def show_wallpaper_menu(self):
		
		self.rofi.updateTheme(self.rasi_wallpaper)

		self.load_wallpapers()

		if len(self.wallpapers) == 0:
			raise CarbonError("No wallpapers to show.") # todo: add visual error message insteads

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Set Wallpaper",
			options= self.wallpapers
		)

		selected: str = self.rofi.wait()
		self.current = self.show_main_menu 
		if not selected:
			return

		self.themer.setWallpaper(img=selected)
		self.themer.updateTheme(img=selected)


	def show_color_menu(self):
		
		self.rofi.updateTheme(self.rasi_entry)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter a hex code (current:{self.themer.current_hex})"
		)

		entered = self.rofi.wait().strip()

		self.current = self.show_main_menu 
		if not entered: 
			return

		if entered == self.themer.current_hex: return

		if not is_valid_hex(entered):
			self.display(f"{Icons.error} ", f"Invalid hex value: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			return

		self.themer.updateTheme(hex=entered)


	def show_source_menu(self):
		
		options = [
			f"{Icons.wallpaper}  From wallpaper",
			f"{Icons.color}  From color",
		]

		if self.themer.current_source == "wallpaper":
			options[0] = RofiShell.markActive(options[0])
		else:
			options[1] = RofiShell.markActive(options[1])
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Source",
			options= options
		)

		selected: str = self.rofi.wait()


		self.current = self.show_main_menu 
		if not selected:
			return

		if selected == options[0]:
			source = "wallpaper"
		else:
			source = "hex"		
			
		if source == self.themer.current_source: return

		self.themer.updateTheme(source=source)


	def show_variant_menu(self):

		options = [
			"[1] Ash",
			"[2] Coal",
			"[3] Graphite",
			"[4] Diamond"
		]

		current = self.themer.current_variant
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

		self.current = self.show_main_menu 
		if not selected: 
			return

		selected = selected.split("]")[-1].strip().lower()

		if selected == current: return

		self.themer.updateTheme(variant=selected)
		


	def show_contrast_menu(self):
		
		self.rofi.updateTheme(self.rasi_entry)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter contrast value (current:{round(self.themer.current_contrast, 2)})"
		)

		entered = self.rofi.wait()

		self.current = self.show_main_menu 
		if not entered: self.close()

		if not is_valid_number(entered):
			self.display(f"{Icons.error} ", f"Invalid number: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			return
		
		contrast = float(entered)

		self.themer.updateTheme(contrast=contrast)


	def show_face_menu(self):
		return

		self.rofi.updateTheme(self.rasi_entry)

		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Profile Picture",
			mesg=f"Enter a filepath\n(current:{current_face})"
		)

		entered = self.rofi.wait().strip()

		self.current = self.show_main_menu 
		if not entered: return
		
		path = Path(entered).expanduser()

		if not path.exists():
			self.displayer.show(f"{Icons.error} ", f"File not found: {f"{entered[:10]}..." if len(entered) > 10 else entered}")
			self.displayer.wait()
			return

		if current_face.exists() and path == current_face: return
		Theme.set_face(path)

		CarbonConfig.set("theme.face", entered)


	def show_font_menu(self):
		return
	
		options = get_fonts()

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Fonts",
			options= options
		)

		selected: str = self.rofi.wait()

		self.current = self.show_main_menu 
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

	def get_wallpapers(sources: list[str] | str) -> list[str]:

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

			images = Utils.get_images(item)

			wallpapers.extend(images)

		wallpapers.sort()


		return wallpapers


	def get_images(directory: Path) -> list[str]:

		images = []
		
		for item in directory.iterdir():
			if item.is_file():
				absolute = item.absolute()
				option = RofiShell.markWithIcon(absolute, absolute)
				images.append(option)

		return images

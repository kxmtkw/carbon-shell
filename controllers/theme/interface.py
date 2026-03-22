from carbon.rofi import RofiShell

from carbon.helpers import CarbonError
from carbon.config import CarbonConfig
from carbon.config.defaults import ConfigDefaults

from carbon.theme import Theme

from icons import Icons

from pathlib import Path
import time

from utils import get_wallpapers, is_valid_hex, is_valid_number

main_rasi = "~/.carbon/shell/rofi/theme/main.rasi"
entry_rasi = "~/.carbon/shell/rofi/theme/entry.rasi"
mesg_rasi = "~/.carbon/shell/rofi/theme/mesg.rasi"
wallpaper_rasi = "~/.carbon/shell/rofi/theme/wallpaper.rasi"

# TODO error handling and displaying what went wrong to the user, for example invalid hex value or contrast not being a number

class ThemeManager:

	def __init__(self):
		self.rofi = RofiShell(main_rasi)

		self.is_running = True
		self.current = self.show_main_menu
	
		self.wallpapers = get_wallpapers()
	

	def launch(self):

		while self.is_running:
			self.current()


	def show_main_menu(self):

		self.rofi.updateTheme(main_rasi)

		current_mode = CarbonConfig.get("theme.mode", "light", valid_types=(str))
		is_dark_mode = False if current_mode == "light" else True

		title = "Theme"
		options = [
			f"{Icons.light}  Toggle light mode" if is_dark_mode else f"{Icons.dark}  Toggle dark mode",
			f"{Icons.wallpaper}  Select wallpaper",
			f"{Icons.color}  Select color",
			f"{Icons.variant}  Update variant",
			f"{Icons.source}  Update theme source",
			f"{Icons.contrast}  Change contrast",
			f"{Icons.face}  Change profile picture",
		]

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			options=options
		)

		selected = self.rofi.wait()
		
		if not selected:
			exit()

		elif selected == options[0]:
			Theme.switch_theme_mode("light" if is_dark_mode else "dark")
			CarbonConfig.set("theme.mode", "light" if is_dark_mode else "dark")

		elif selected == options[1]:
			self.current = self.show_wallpaper_menu

		elif selected == options[2]:
			self.current = self.show_color_menu

		elif selected == options[3]:
			self.current = self.show_variant_menu

		elif selected == options[4]:
			self.current = self.show_source_menu

		elif selected == options[5]:
			self.current = self.show_source_menu

		else:
			self.current = self.show_face_menu


	def show_wallpaper_menu(self):
		
		self.rofi.updateTheme(wallpaper_rasi)

		if len(self.wallpapers) == 0:
			CarbonError("No wallpapers to show.").halt() # todo: add visual error message insteads

		self.rofi.updateTheme(wallpaper_rasi)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Set Wallpaper",
			options= self.wallpapers
		)

		selected: str = self.rofi.wait()
		self.current = self.show_main_menu 
		if not selected: return

		image = Path(selected)
		Theme.set_wallpaper(image)

		source = CarbonConfig.get("theme.source", ConfigDefaults.source, valid_types=(str))
		
		if source == "wallpaper":
			mode = CarbonConfig.get("theme.mode", ConfigDefaults.mode, valid_types=(str))
			contrast = CarbonConfig.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))
			variant = CarbonConfig.get("theme.variant", ConfigDefaults.variant, valid_types=(str))
			Theme.change_color_theme(mode, variant, img=image, contrast=contrast)

		else:
			pass # no need to update theme

		CarbonConfig.set("theme.wallpaper", str(image))



	def show_color_menu(self):

		current_color = CarbonConfig.get("theme.hex", ConfigDefaults.hex, valid_types=(str))
		
		self.rofi.updateTheme(entry_rasi)

		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter a hex code (current:{current_color})"
		)

		entered = self.rofi.wait().strip()

		self.current = self.show_main_menu 
		if not entered: return


		if entered == current_color: return

		if not is_valid_hex(entered):
			return

		source = CarbonConfig.get("theme.source", ConfigDefaults.source, valid_types=(str))
		
		if source == "wallpaper":
			pass
		else:
			mode = CarbonConfig.get("theme.mode", ConfigDefaults.mode, valid_types=(str))
			contrast = CarbonConfig.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))
			variant = CarbonConfig.get("theme.variant", ConfigDefaults.variant, valid_types=(str))

			Theme.change_color_theme(mode, variant, hex=entered, contrast=contrast)

		CarbonConfig.set("theme.hex", entered)


	def show_source_menu(self):

		current_source = CarbonConfig.get("theme.source", ConfigDefaults.source, valid_types=(str))

		options = [
			f"{Icons.wallpaper}  From wallpaper",
			f"{Icons.color}  From color",
		]

		if current_source == "wallpaper":
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
		if not selected: return

		source = selected.split(" ")[-1]
		
		if source == current_source: return

		mode = CarbonConfig.get("theme.mode", ConfigDefaults.mode, valid_types=(str))
		contrast = CarbonConfig.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))
		variant = CarbonConfig.get("theme.variant", ConfigDefaults.variant, valid_types=(str))

		if source == "wallpaper":
			image = CarbonConfig.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str))
			image_path = Path(image)
			if not image_path.exists(): return
			Theme.change_color_theme(mode, variant, img=image, contrast=contrast)

		else:
			color = CarbonConfig.get("theme.hex", ConfigDefaults.hex, valid_types=(str))
			Theme.change_color_theme(mode, variant, hex=color, contrast=contrast)

		CarbonConfig.set("theme.source", source)

	

	def show_variant_menu(self):

		variant = CarbonConfig.get("theme.variant", ConfigDefaults.variant, valid_types=(str))

		options = [
			"[1] Ash",
			"[2] Coal",
			"[3] Graphite",
			"[4] Diamond"
		]

		if variant == "ash":
			options[0] = RofiShell.markActive(options[0])
		elif variant == "coal":
			options[1] = RofiShell.markActive(options[1])
		elif variant == "graphite":
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
		if not selected: return

		selected = selected.split("]")[-1].strip().lower()

		if selected == variant: return

		source = CarbonConfig.get("theme.source", ConfigDefaults.source, valid_types=(str))

		mode = CarbonConfig.get("theme.mode", ConfigDefaults.mode, valid_types=(str))
		contrast = CarbonConfig.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))

		if source == "wallpaper":
			image = CarbonConfig.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str))
			image_path = Path(image)
			if not image_path.exists(): return
			Theme.change_color_theme(mode, selected.lower(), img=image, contrast=contrast)

		else:
			color = CarbonConfig.get("theme.hex", ConfigDefaults.hex, valid_types=(str))
			Theme.change_color_theme(mode, selected.lower(), hex=color, contrast=contrast)

		CarbonConfig.set("theme.variant", selected)



	def show_contrast_menu(self):
		
		self.rofi.updateTheme(entry_rasi)

		current_contrast = CarbonConfig.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Theme Color",
			mesg=f"Enter contrast value (current:{round(current_contrast, 2)})"
		)

		entered = self.rofi.wait()

		self.current = self.show_main_menu 
		if not entered: return

		if not is_valid_number(entered):
			self.current = self.show_main_menu 
			return
		
		contrast = float(entered)

		self.current = self.show_main_menu

		source = CarbonConfig.get("theme.source", ConfigDefaults.source, valid_types=(str))
		mode = CarbonConfig.get("theme.mode", ConfigDefaults.mode, valid_types=(str))
		variant = CarbonConfig.get("theme.variant", ConfigDefaults.variant, valid_types=(str))

		if source == "wallpaper":
			image = CarbonConfig.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str))
			image_path = Path(image)
			if not image_path.exists(): return
			Theme.change_color_theme(mode, variant, img=image, contrast=contrast)

		else:
			color = CarbonConfig.get("theme.hex", ConfigDefaults.hex, valid_types=(str))
			Theme.change_color_theme(mode, variant, hex=color, contrast=contrast)

		CarbonConfig.set("theme.contrast", contrast)




	def show_face_menu(self):

		current_face = CarbonConfig.get("theme.face", ConfigDefaults.hex, valid_types=(str))
		current_face = Path(current_face).expanduser()


		self.rofi.updateTheme(entry_rasi)

		
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
			return

		if current_face.exists() and path == current_face: return
		Theme.set_face(path)

		CarbonConfig.set("theme.face", entered)



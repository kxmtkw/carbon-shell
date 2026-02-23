from carbon.state import CarbonState
from carbon.theme import Theme

from pathlib import Path
import sys, time
from lib.rofi import RofiShell

class ThemePicker():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/screenshot.rasi")

		self.image_dir = Path("~/Images").expanduser()


	def launch(self):
		while True:
			self.open_main_options()


	def open_main_options(self):

		options: list[str] = [
			"Toggle mode",
			"Change wallpaper",
			"Update theme",
		]

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Theme",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()
		

		if selected == options[0]:
			current_mode = CarbonState.get("theme_mode", "light", valid_types=(str))
			toggled_mode = "dark" if current_mode == "light" else "light"
			Theme.switch_theme_mode(toggled_mode)

		elif selected == options[1]:
			self.open_wallpaper_options()

		elif selected == options[2]:
			self.open_update_theme_options()


	def open_wallpaper_options(self):

		options = self.get_images()

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Set Wallpaper",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		image = self.image_dir.joinpath(selected)

		mode = CarbonState.get("theme_mode", "dark", valid_types=(str))
		variant = CarbonState.get("theme_variant", "graphite", valid_types=(str))
		contrast = CarbonState.get("theme_contrast", 0.25, valid_types=(float, int))

		if image.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, variant, img=image, contrast=contrast)


	def open_update_theme_options(self):

		options = [
			"Ash",
			"Coal",
			"Graphite",
			"Diamond"
		]
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Change Theme",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		mode = CarbonState.get("theme_mode", "dark", valid_types=(str))
		variant = CarbonState.get("theme_variant", "graphite", valid_types=(str))
		contrast = CarbonState.get("theme_contrast", 0.25, valid_types=(float, int))
		image = CarbonState.get("theme_wallpaper", valid_types=(str))

		image_path = Path(image)
		if image_path.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, selected.lower(), image, contrast=contrast)


	def get_images(self) -> list[str]:

		images = []
		for item in self.image_dir.iterdir():
			if item.is_file():
				images.append(item.name)
		
		images.sort()
		return images


if __name__ == "__main__":
	c = ThemePicker()
	c.launch()
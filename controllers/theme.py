from carbon.config import CarbonConfig
from carbon.theme import Theme
from carbon.helpers import CarbonError

from pathlib import Path
import sys, time
from carbon.rofi import RofiShell


main_rasi = "~/.carbon/shell/rofi/theme/main.rasi"
wallpaper_rasi = "~/.carbon/shell/rofi/theme/wallpaper.rasi"

class ThemePicker():
	
	def __init__(self):
		self.rofi = RofiShell(main_rasi)
		self.wallpapers: list[str] = []
		self.get_wallpapers()


	def get_wallpapers(self):
		# Getting Wallpaper Source dirs
		wallpaper_paths: list[Path] = []

		default =  ["~/Pictures", "~/Images"]
		wallpaper_dirs = CarbonConfig.get("defaults.wallpaperSource", default, valid_types=(str, list))

		# Adding paths
		if isinstance(wallpaper_dirs, str):
			wallpaper_paths.append(Path(wallpaper_dirs).expanduser())
		else:
			for item in wallpaper_dirs:
				if not isinstance(item, str): continue
				wallpaper_paths.append(Path(item).expanduser())

		# Checking paths
		for item in wallpaper_paths:
			if not item.exists():
				CarbonError(f"Wallpaper source directory does not exist: '{item.absolute}' ")
				continue

			if not item.is_dir():
				CarbonError(f"Wallpaper source is not a directory: '{item.absolute}' ")

			images = self.get_images(item)

			self.wallpapers.extend(images)

		self.wallpapers.sort()


	def get_images(self, directory: Path) -> list[str]:

		images = []
		
		for item in directory.iterdir():
			if item.is_file():
				option = RofiShell.markWithIcon(item.absolute(), item.absolute())
				images.append(option)

		return images


	def launch(self):
		while True:
			self.open_main_options()


	def open_main_options(self):
		
		self.rofi.updateTheme(main_rasi)

		current_mode = CarbonConfig.get("theme.mode", "light", valid_types=(str))
		is_dark_mode = False if current_mode == "light" else True

		options: list[str] = [
			"  Toggle light mode" if is_dark_mode else "  Toggle dark mode",
			"󰟾  Change wallpaper",
			"  Update theme",
			"󰆖  Change contrast"
		]

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Theme",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()
		

		if selected == options[0]:
			Theme.switch_theme_mode("light" if is_dark_mode else "dark")
			CarbonConfig.set("theme.mode", "light" if is_dark_mode else "dark")

		elif selected == options[1]:
			self.open_wallpaper_options()

		elif selected == options[2]:
			self.open_update_theme_options()

		elif selected == options[3]:
			self.open_contrast_options()


	def open_wallpaper_options(self):

		if len(self.wallpapers) == 0:
			CarbonError("No wallpapers to show.").halt() # todo: add visual error message insteads

		self.rofi.updateTheme(wallpaper_rasi)

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt="Set Wallpaper",
			options= self.wallpapers
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		image = Path(selected)

		mode = CarbonConfig.get("theme.mode", "dark", valid_types=(str))
		variant = CarbonConfig.get("theme.variant", "graphite", valid_types=(str))
		contrast = CarbonConfig.get("theme.contrast", 0.25, valid_types=(float, int))

		if image.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, variant, img=image, contrast=contrast)
			time.sleep(2) # wait for wallpaper animation to end

		self.rofi.updateTheme(main_rasi)

		CarbonConfig.set("theme.wallpaper", str(image))


	def open_update_theme_options(self):

		variant = CarbonConfig.get("theme.variant", "graphite", valid_types=(str))

		options = [
			"[1] Ash",
			"[2] Coal",
			"[3] Graphite",
			"[4] Diamond"
		]
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Change Theme Variant ({variant.capitalize()})",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		selected = selected.split("]")[-1].strip().lower()

		mode = CarbonConfig.get("theme.mode", "dark", valid_types=(str))
		contrast = CarbonConfig.get("theme.contrast", 0.25, valid_types=(float, int))
		image = CarbonConfig.get("theme.wallpaper", valid_types=(str))

		image_path = Path(image)
		if image_path.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, selected.lower(), image, contrast=contrast)

		CarbonConfig.set("theme.variant", selected)


	def open_contrast_options(self):
		
		contrast = CarbonConfig.get("theme.contrast", 0.25, valid_types=(float, int))
		options = [str(x/4) for x in range(1, 17)]
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Change Contrast ({contrast})",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		mode = CarbonConfig.get("theme.mode", "dark", valid_types=(str))
		variant = CarbonConfig.get("theme.variant", "graphite", valid_types=(str))
		image = CarbonConfig.get("theme.wallpaper", valid_types=(str))

		image_path = Path(image)
		if image_path.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, variant, image, contrast=float(selected))

		CarbonConfig.set("theme.contrast", float(selected))



if __name__ == "__main__":
	c = ThemePicker()
	c.launch()
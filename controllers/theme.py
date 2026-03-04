from carbon.state import CarbonState
from carbon.theme import Theme

from pathlib import Path
import sys, time
from carbon.rofi import RofiShell


main_rasi = "~/.carbon/shell/rofi/themer.rasi"

class ThemePicker():
	
	def __init__(self):
		self.rofi = RofiShell(main_rasi)

		self.image_dir = Path("~/Images").expanduser()


	def launch(self):
		while True:
			self.open_main_options()


	def open_main_options(self):
		
		self.rofi.updateTheme(main_rasi)

		current_mode = CarbonState.get("theme_mode", "light", valid_types=(str))
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

		elif selected == options[1]:
			self.open_wallpaper_options()

		elif selected == options[2]:
			self.open_update_theme_options()

		elif selected == options[3]:
			self.open_contrast_options()


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

		variant = CarbonState.get("theme_variant", "graphite", valid_types=(str))

		options = [
			"[1] Ash",
			"[2] Coal",
			"[3] Graphite",
			"[4] Diamond"
		]
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Change Theme ({variant.capitalize()})",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		selected = selected.split("]")[-1].strip().lower()

		mode = CarbonState.get("theme_mode", "dark", valid_types=(str))
		contrast = CarbonState.get("theme_contrast", 0.25, valid_types=(float, int))
		image = CarbonState.get("theme_wallpaper", valid_types=(str))

		image_path = Path(image)
		if image_path.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, selected.lower(), image, contrast=contrast)


	def open_contrast_options(self):
		
		contrast = CarbonState.get("theme_contrast", 0.25, valid_types=(float, int))
		options = [str(x/4) for x in range(1, 17)]
		
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=f"Change Contrast ({contrast})",
			options= options
		)

		selected: str = self.rofi.wait()
		if not selected: exit()

		mode = CarbonState.get("theme_mode", "dark", valid_types=(str))
		variant = CarbonState.get("theme_variant", "graphite", valid_types=(str))
		image = CarbonState.get("theme_wallpaper", valid_types=(str))

		image_path = Path(image)
		if image_path.exists():
			Theme.set_wallpaper(image)
			Theme.change_color_theme(mode, variant, image, contrast=float(selected))


	def get_images(self) -> list[str]:

		images = []
		for item in self.image_dir.iterdir():
			if item.is_file():
				option = RofiShell.markWithIcon(item.name, item.absolute())
				images.append(option)
		print(images)
		return images


if __name__ == "__main__":
	c = ThemePicker()
	c.launch()
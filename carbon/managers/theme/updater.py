from pathlib import Path

from carbon.utils import shellrun, writefile, procrun, CarbonError

from .colors import *
from . import fonts

from carbon.lib.quickshell import Quickshell

class ThemeUpdater:


	def __init__(self):
		self.colorfiles = {}
		self.colorfiles["rofi"]       = "~/.carbon/shell/rofi/Config/color.rasi"
		self.colorfiles["json"]       = "~/.carbon/shell/quickshell/Config/color.json"
		self.colorfiles["hypr"]       = "~/.config/hypr/color.conf"
		self.colorfiles["kde"]        = ("~/.local/share/color-schemes/Carbon.colors", "~/.local/share/color-schemes/CarbonCopy.colors")
		self.colorfiles["alacritty"]  = "~/.config/alacritty/Carbon.toml"
		self.colorfiles["kitty"]      = "~/.config/kitty/Carbon.conf"

		self.updaters = {
			"json":      updateJson,
			"kde":       updateKde,
			"rofi":      updateRofi,
			"hypr":      updateHypr,
			"kitty":     updateKitty,
			"alacritty": updateAlacritty,
		}

		self.post_update_commands = [
			"plasma-apply-colorscheme CarbonCopy && plasma-apply-colorscheme Carbon",
			"hyprctl reload"
		]

		self.qs = Quickshell()
		self.fonts = self.loadFonts()


	def updateColors(self, colors: dict[str, str]):

		for type, paths in self.colorfiles.items():
			handler = self.updaters.get(type)
			string = handler(colors)

			for file in ([paths] if isinstance(paths, str) else paths):
				writefile(Path(file).expanduser(), string)

		self.runPostUpdate()


	def updateFont(self, font: str):

		if font not in self.fonts:
			raise CarbonError(f"Unknown font: {font}.")
		
		rofifile = Path("~/.carbon/shell/rofi/Config/fonts.rasi").expanduser()

		rofi = fonts.updateRofi(font)
		writefile(rofifile, rofi)

		self.qs.updateFont(font)


	def updateFace(self, path: str):

		if not Path(path).expanduser().exists():
			raise CarbonError(f"Face image not found: {path}")
		
		out = shellrun(f"cp {path} ~/.carbon/user/face")

		if not out[0]:
			raise CarbonError(f"Failed to update face image. Reason: {out[1]}")


	def updateWallpaper(self, img: str, animation: str):

		path = Path(img).expanduser()

		if not path.exists():
			raise CarbonError(f"File not found: {path}") 
		
		success, output = procrun(["swww", "img", "--transition-type", animation, path])

		if not success:
			raise CarbonError(f"Failed to change wallpaper: swww failure\n{output}")
			
		out = shellrun(f"cp {path} ~/.carbon/user/wall")		

		if not out[0]:
			raise CarbonError(f"Failed to update wallpaper image. Reason: {out[1]}")


	def runPostUpdate(self):
		for cmd in self.post_update_commands:
			shellrun(cmd)

		self.qs.updateTheme()


	def loadFonts(self) -> list[str]:

		success, output = shellrun("fc-list --format='%{family[0]}\n' | sort | uniq")

		if not success: return fonts

		fonts = []
		for item in output.splitlines():
			if item.startswith("Noto"): continue
			fonts.append(item)

		return fonts
	

	def getFonts(self) -> list[str]:
		return self.fonts
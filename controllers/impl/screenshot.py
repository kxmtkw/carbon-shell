from pathlib import Path
from rofi import RofiShell
import sys

class ScreenshotMenu():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/screenshot.rasi")

		self.prompt = "Screenshot"
		self.mesg = ""

		try:
			self.save_dir = Path(sys.argv[1])
		except IndexError:
			self.save_dir = Path("~/Images").expanduser()

		self.options: list[str] = [
			"  Screen",
			"  Window",
			"󰿦  Region"
		]


	def launch(self):

		selected: str = self.rofi.display(
			self.prompt,
			self.mesg,
			self.options
		)

		if not selected: return

		self.exec(selected.strip())


	def exec(self, option: str):

		if option == self.options[0]:
			self.rofi.Run(f"hyprshot -m active -m output -o {self.save_dir}")

		elif option == self.options[1]:
			self.rofi.Run(f"hyprshot -m window -o {self.save_dir}")

		elif option == self.options[2]:
			self.rofi.Run(f"hyprshot -m region -o {self.save_dir}")



if __name__ == "__main__":
	c = ScreenshotMenu()
	c.launch()
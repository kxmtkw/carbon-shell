from pathlib import Path
import sys, time

from lib.rofi import RofiShell

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

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt= self.prompt,
			mesg= self.mesg,
			options= self.options
		)

		selected: str = self.rofi.wait()
		if not selected: return

		self.exec(selected.strip())


	def exec(self, option: str):

		time.sleep(0.2) # rofi closes
		
		if option == self.options[0]:
			self.rofi.Run(f"hyprshot -m active -m output -o {self.save_dir}")

		elif option == self.options[1]:
			self.rofi.Run(f"hyprshot -m window -o {self.save_dir}")

		elif option == self.options[2]:
			self.rofi.Run(f"hyprshot -m region -o {self.save_dir}")



if __name__ == "__main__":
	c = ScreenshotMenu()
	c.launch()
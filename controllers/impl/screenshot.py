from rofi import RofiShell

class ScreenshotMenu():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/windows.rasi")

		self.prompt = "Screenshot"
		self.mesg = ""

		self.options: list[str] = [
			"Screen",
			"Window",
			"Region"
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
			self.rofi.Run("hyprshot -m output")

		elif option == self.options[1]:
			self.rofi.Run("hyprshot -m window")

		elif option == self.options[2]:
			self.rofi.Run("hyprshot -m region")



if __name__ == "__main__":
	c = ScreenshotMenu()
	c.launch()
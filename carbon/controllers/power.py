from carbon.rofi import RofiShell

class PowerMenu():
	
	def __init__(self):
		self.rofi = RofiShell("Config/rofi/power.rasi")

		self.options: list[str] = [
		"  Shutdown",
		"  Reboot",
		"  Lock",
		"  Sleep",
		"  Hibernate",
		"  BIOS" 
		]


	def run(self):
		selected: str = self.rofi.display(
			"",
			"Power",
			self.options
		)

		if not selected: return

		if not self.confirm(): return

		self.exec(selected.strip())


	def confirm(self) -> bool:
		selected = self.rofi.display(
			"",
			"Are you sure?",
			["  Yes", "  No"]
		)

		if (selected.strip() == "  Yes"): return True
		return False


	def exec(self, selected: str):
		
		options = self.options

		if selected == options[0]:
			self.rofi.Run("systemctl poweroff")
		elif selected == options[1]:
			self.rofi.Run("systemctl reboot")
		elif selected == options[2]:
			self.rofi.Run("loginctl lock")
		elif selected == options[3]:
			self.rofi.Run("systemctl suspend")
		elif selected == options[4]:
			self.rofi.Run("systemctl hibernate")
		elif selected == options[5]:
			self.rofi.Run("systemctl reboot --firmware-setup")

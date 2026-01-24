from rofi import RofiShell

class PowerMenu():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/power.rasi")
		self.confirmation = RofiShell("~/.config/rofi/confirmation.rasi")

		self.options: list[str] = [
		"  Shutdown",
		"  Reboot",
		"  Lock",
		"  Sleep",
		"  Hibernate",
		"  BIOS" 
		]


	def launch(self):
		selected: str = self.rofi.display(
			self.rofi.Run("echo Uptime: $(uptime -p | sed -e 's/up //g')").strip(),
			self.rofi.Run("echo \"$(whoami)@$(hostname)\"").strip(),
			self.options
		)

		if not selected: return

		self.exec(selected.strip())


	def confirm(self) -> bool:
		selected = self.confirmation.display(
			"",
			"Are you sure?",
			["  No", "  Yes"]
		)

		if (selected.strip() == "  Yes"): return True
		return False


	def exec(self, selected: str):
		
		options = self.options
		

		if selected == options[0]:
			cmd = "systemctl poweroff"
		elif selected == options[1]:
			cmd = "systemctl reboot"
		elif selected == options[2]:
			cmd = "loginctl lock"
			self.rofi.Run(cmd)
			return
		elif selected == options[3]:
			cmd = "systemctl suspend"
		elif selected == options[4]:
			cmd = "systemctl hibernate"
		else:
			cmd = "systemctl reboot --firmware-setup"

		if not self.confirm(): return
		self.rofi.Run(cmd)


if __name__ == "__main__":
	p = PowerMenu()
	p.launch()
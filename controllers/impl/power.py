from rofi import RofiShell
import time

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
		"󰍃  Logout",
		"  BIOS" 
		]


	def launch(self):
		selected: str = self.rofi.display(
			self.rofi.Run("echo \"$(whoami)@$(hostnamectl | awk -F': ' '/Static hostname/ {print $2}')\"").strip(),
			self.rofi.Run("uptime -p").strip().capitalize(),
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
			cmd = "hyprlock"
			time.sleep(0.25) # rofi closes
			self.rofi.Run(cmd)
			return
		elif selected == options[3]:
			cmd = "systemctl suspend"
		elif selected == options[4]:
			cmd = "systemctl hibernate"
		elif selected == options[5]:
			cmd = "hyprland dispatch exit"
		else:
			cmd = "systemctl reboot --firmware-setup"

		if not self.confirm(): return
		self.rofi.Run(cmd)


if __name__ == "__main__":
	c = PowerMenu()
	c.launch()

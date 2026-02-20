from lib.rofi import RofiShell
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
		self.rofi.display(
			mode = RofiShell.Mode.dmenu,
			prompt = self.rofi.Run("echo \"$(whoami)@$(hostnamectl | awk -F': ' '/Static hostname/ {print $2}')\"").strip(),
			mesg = self.rofi.Run("uptime -p").strip().capitalize(),
			options = self.options
		)
		selected: str = self.rofi.wait()

		if not selected: return
		self.exec(selected.strip())


	def confirm(self) -> bool:
		self.confirmation.display(
			mode = RofiShell.Mode.dmenu,
			mesg="Are you sure?",
			options=["  No", "  Yes"]
		)
		selected = self.confirmation.wait()

		if (selected.strip() == "  Yes"): return True
		return False


	def exec(self, selected: str):
		
		options = self.options

		if selected == options[0]:
			cmd = "systemctl poweroff"
		elif selected == options[1]:
			cmd = "systemctl reboot"
		elif selected == options[2]:
			time.sleep(0.25) #rofi closes
			cmd = "hyprlock"
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
		time.sleep(0.25) #rofi closes
		
		self.rofi.Run(cmd)


if __name__ == "__main__":
	c = PowerMenu()
	c.launch()

from carbon.rofi import RofiShell
import time

class PowerMenu():
	
	def __init__(self):
		self.rofi = RofiShell("~/.carbon/shell/rofi/power/main.rasi")
		self.confirmation = RofiShell("~/.carbon/shell/rofi/confirmation/main.rasi")

		self.options: list[str] = [
		"  Lock",
		"  Shutdown",
		"  Reboot",
		"  Suspend",
		"  Hibernate",
		"󰍃  Logout",
		]


	def launch(self):

		uptime_msg = self.rofi.Run("uptime -p").strip().capitalize()

		if uptime_msg.count(",") == 2:
			uptime_msg = "".join(uptime_msg.split(",")[0:2])

		self.rofi.display(
			mode = RofiShell.Mode.dmenu,
			prompt = self.rofi.Run("echo \"$(whoami)@$(hostnamectl | awk -F': ' '/Static hostname/ {print $2}')\"").strip(),
			mesg = uptime_msg,
			options = self.options
		)
		selected: str = self.rofi.wait()
		
		if not selected: return
		self.exec(selected.strip())

	def exec(self, selected: str):
		
		options = self.options

		if selected == options[0]:
			cmd = "carbon.power lock"
			time.sleep(0.25)
			return self.rofi.Run(cmd) #no need to confirm locking
		elif selected == options[1]:
			cmd = "carbon.power shutdown"
		elif selected == options[2]:
			cmd = "carbon.power reboot"
		elif selected == options[3]:
			cmd = "carbon.power suspend"
		elif selected == options[4]:
			cmd = "carbon.power hibernate"
		elif selected == options[5]:
			cmd = "carbon.power logout"
		else:
			return
		
		self.confirmation.display(
			mode = RofiShell.Mode.dmenu,
			mesg="Are you sure?",
			options=["  No", "  Yes"]
		)

		selected = self.confirmation.wait()
		if (selected.strip() != "  Yes"): return

		time.sleep(0.25) #rofi closes
		self.rofi.Run(cmd)


if __name__ == "__main__":
	c = PowerMenu()
	c.launch()

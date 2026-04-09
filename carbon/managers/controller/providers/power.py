import time

from carbon.lib.rofi import RofiShell
from carbon.managers.controller.base import BaseController

from carbon.utils import shellrun


class Power(BaseController):
	
	def __init__(self):
		super().__init__()
		self.main_rasi = "~/.carbon/shell/rofi/power/main.rasi"
		self.confirmation_rasi = "~/.carbon/shell/rofi/confirmation/main.rasi"
		
		self.rofi = RofiShell(self.main_rasi)

		self.options: list[str] = [
		"  Lock",
		"  Shutdown",
		"  Reboot",
		"  Suspend",
		"  Hibernate",
		"󰍃  Logout",
		]

		out = shellrun("echo \"$(whoami)@$(hostnamectl | awk -F': ' '/Static hostname/ {print $2}')\"")

		if out[0]:
			self.user_name = out[1].strip()
		else:
			self.user_name = "Unknown User"


	def launch(self):

		self.rofi.updateTheme(self.main_rasi)

		uptime_msg = self.getUptime()
		
		self.rofi.display(
			mode = RofiShell.Mode.dmenu,
			prompt = self.user_name,
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
			return shellrun(cmd) #no need to confirm locking
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
		
		self.rofi.updateTheme(self.confirmation_rasi)

		self.rofi.display(
			mode = RofiShell.Mode.dmenu,
			mesg="Are you sure?",
			options=["  No", "  Yes"]
		)

		selected = self.rofi.wait()
		if (selected.strip() != "  Yes"): return

		time.sleep(0.25) #rofi closes
		shellrun(cmd)
	

	def getUptime(self) -> str:
		output = shellrun("uptime -p")

		if not output[0]:
			return "???"

		uptime_msg = output[1].strip().capitalize()

		if uptime_msg.count(",") == 2:
			uptime_msg = "".join(uptime_msg.split(",")[0:2])

		return uptime_msg
	

	def close(self):
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass


if __name__ == "__main__":
	c = Power()
	c.launch()

from rofi import RofiShell

class BatteryInfo():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/battery.rasi")

		self.battery_info = self.rofi.Run("upower -b")
	

		perc = self.grab_key("percentage:")
		status = self.grab_key("state:")
		if not status:
			status = "<Error>"

		timing = self.grab_key("time to full:")
		if not timing:
			timing = self.grab_key("time to empty:")

		cycles = self.grab_key("charge-cycles:")

		health = self.grab_key("capacity:")

		self.prompt: str = "Battery Info"

		self.mesg: str = f"{status} {perc}"

		self.options: list[str] = [
			f"Time remaining:    {timing}",
			f"Charge Cycles:     {cycles}",
			f"Health:            {health}"
		]


	def grab_key(self, key: str) -> str | None:
		index = self.battery_info.find(key) 
		
		if index == -1: return

		index += len(key)
		for i in range(index, len(self.battery_info)):
			if self.battery_info[i] == '\n':
				val = self.battery_info[index:i].strip()
				return val
			

	def launch(self):

		selected: str = self.rofi.display(
			self.prompt,
			self.mesg,
			self.options
		)

		if not selected: return

	


if __name__ == "__main__":
	p = BatteryInfo()
	p.launch()
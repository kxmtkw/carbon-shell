from rofi import RofiShell
import os

class SystemInfo():
	
	def __init__(self):
		self.rofi = RofiShell("~/.config/rofi/system.rasi")	

		self.info = self.rofi.Run("hostnamectl")
		
		self.os_name = self.grab_key("Operating System:")
		self.kernel = self.grab_key("Kernel:")
		self.arch = self.grab_key("Architecture:")
		self.hardware = self.grab_key("Hardware Model:")
		self.user = self.rofi.Run("whoami").strip()
		self.hostname = self.grab_key("Static hostname:")
		self.shell = self.rofi.Run("echo $SHELL").strip()
		
		self.info = self.rofi.Run("lscpu")
		self.cpu = self.grab_key("Model name:")
		
		self.pacman_packages = self.rofi.Run("pacman -Q | wc -l").strip()
		self.pacman_packages_explicit = self.rofi.Run("pacman -Qe | wc -l").strip()
		self.pacman_packages_aur = self.rofi.Run("pacman -Qme | wc -l").strip()


		self.prompt = f"{self.os_name} {self.arch}"
		self.mesg = f"{self.user}@{self.hostname}"

		self.options: list[str] = [
			f":: OS                 {self.os_name} {self.arch}",
			f":: Kernel             {self.kernel}",
			f":: Hardware           {self.hardware}",
			f":: Processor          {self.cpu}",
			f":: Current User       {self.user}",
			f":: Hostname           {self.hostname}",
			f":: Shell              {self.shell}",
			f":: Package Manager    Pacman",
			f":: Package            {self.pacman_packages} ({self.pacman_packages_explicit} explicit, {self.pacman_packages_aur} from AUR)",
		]


	def grab_key(self, key: str) -> str | None:
		index = self.info.find(key) 
		
		if index == -1: return

		index += len(key)
		for i in range(index, len(self.info)):
			if self.info[i] == '\n':
				val = self.info[index:i].strip()
				return val
			

	def launch(self):

		selected: str = self.rofi.display(
			f"󰣇 ",
			"",
			self.options
		)

		if not selected: return

	
if __name__ == "__main__":
	c = SystemInfo()
	c.launch()
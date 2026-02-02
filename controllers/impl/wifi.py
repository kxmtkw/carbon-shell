from rofi import RofiShell
from networker.wifi import WifiManager, WifiError, WifiNetwork

class WifiMenu:

	def __init__(self) -> None:
		self.wifi = WifiManager()
		self.closed: bool = False

		self.rofi = RofiShell("~/.config/rofi/wifi/main.rasi")

		self.title = "Wifi"

		self.status = ""

		self.options = [
			">>     Toggle Wifi",
			">>     Rescan",
			">>  󰀝   Toggle Airplane Mode",
			">>  󰀝   Hotspot"
		]


	def launch(self):
		while not self.closed:
			self.show_main_menu()

	
	def make_wifi_entry(self, id: int, net: WifiNetwork) -> str:
		icon = "󰤥"
		entry = f"{icon}  [{id}] {net.ssid}{RofiShell.MarkActive if net.active else ''}"
		return entry
		

	def extract_id(self, entry: str) -> int:
		id = entry.split("]")[0].split("[")[1]
		try:
			return int(id)
		except ValueError:
			print("Error encountered when extracting id from entry. This should not happen at all.")
			exit(1)


	def show_main_menu(self):

		list_items = []
		list_items.extend(self.options)

		if self.wifi.is_radio_on():
			
			networks = self.wifi.list_networks()
			
			active = self.wifi.get_active_network()

			self.status = f"Status: ON | Connected: {active.ssid if active else 'None'}"

			list_items.extend([self.make_wifi_entry(id, wifi) for id, wifi in enumerate(networks)])

		else:
			networks = None
			self.status = f"Status: OFF"


		selected = self.rofi.display(
			self.title,
			self.status,
			list_items
		)

		if not selected:
			exit()

		if selected == self.options[0]:
			self.wifi.set_radio(not self.wifi.is_radio_on())
			return
		
		elif selected == self.options[1]:
			self.wifi.rescan()
			return
		
		elif selected == self.options[2]:
			self.wifi.set_radio(not self.wifi.is_radio_on())

		else:
			if networks:
				self.wifi.connect_network(networks[self.extract_id(selected)])
				self.wifi.rescan()


	def show_wifi_menu(self, net: WifiNetwork):
		pass
		
	
	def show_password_prompt(self, net: WifiNetwork) -> str:
		return "s"

	
	def trigger_loading_screen(self, prompt: str, msg: str):
		pass


if __name__ == "__main__":
	c = WifiMenu()
	c.launch()
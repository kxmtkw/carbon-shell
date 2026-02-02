from rofi import RofiShell
from networker.wifi import WifiManager, WifiError, WifiNetwork

class WifiMenu:

	def __init__(self) -> None:
		self.wifi = WifiManager()

		self.rofi = RofiShell("~/.config/rofi/launcher.rasi")

		self.title = "Wifi"

		self.status = ""

		self.options = [
			">>     Toggle Wifi",
			">>     Rescan",
			">>  󰀝   Toggle Airplane Mode"
		]


	def launch(self):
		self.show_main_menu()


	def show_main_menu(self):
		list_items = []
		list_items.extend(self.options)

		if self.wifi.is_radio_on():

			networks = {wifi.ssid:wifi for wifi in self.wifi.list_networks()}
			
			active = self.wifi.get_active_network()

			self.status = f"Status: ON | Connected: {active.ssid if active else 'None'}"

			list_items.extend([wifi.ssid for wifi in self.wifi.list_networks()])

		else:

			networks = {}
			self.status = f"Status: OFF"


		selected = self.rofi.display(
			self.title,
			self.status,
			list_items
		)

		if selected == self.options[0]:
			self.wifi.set_radio(not self.wifi.is_radio_on())
		elif selected == self.options[1]:
			self.launch()
			exit()
		elif selected == self.options[2]:
			self.wifi.set_radio(not self.wifi.is_radio_on())
		else:
			self.wifi.connect_network(networks[selected])

		

if __name__ == "__main__":
	c = WifiMenu()
	c.launch()
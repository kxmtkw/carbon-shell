from rofi import RofiShell
from networker.wifi import WifiManager, WifiError, WifiNetwork

main_rasi = "~/.config/rofi/wifi/main.rasi"
options_rasi = "~/.config/rofi/wifi/options.rasi"
display_rasi = "~/.config/rofi/wifi/display.rasi"
password_rasi = "~/.config/rofi/wifi/password.rasi"


class WifiMenu:

	def __init__(self) -> None:
		self.wifi = WifiManager()
		self.closed: bool = False

		self.rofi = RofiShell(main_rasi)

		self.title = "Wifi"

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
		try:
			id = entry.split("]")[0].split("[")[1]
			return int(id)
		except ValueError:
			print(f"Error encountered when extracting id from entry. This should not happen at all. {entry}")
			exit(1)


	def show_main_menu(self):
		
		self.rofi.updateTheme(main_rasi)

		list_items = []
		list_items.extend(self.options)

		if self.wifi.is_radio_on():
			
			networks = self.wifi.list_networks()
		
			status = f"Status: ON"

			list_items.extend([self.make_wifi_entry(id, wifi) for id, wifi in enumerate(networks)])

		else:
			networks = None
			status = f"Status: OFF"


		selected = self.rofi.display(
			self.title,
			status,
			list_items
		)

		print(selected)

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
			print(networks)
			if networks:
				self.show_wifi_options(networks[self.extract_id(selected)])


	def show_wifi_options(self, net: WifiNetwork):
		
		self.rofi.updateTheme(options_rasi)

		wifi_options = [
			"󱘖  Disconnect" if net.active else "󱘖  Connect",
			"  Forget"
		]

		details = f"SSID : {net.ssid}"

		selected = self.rofi.display(
			self.title,
			details,
			wifi_options
		)

		if not selected:
			exit()

		if selected == wifi_options[0]:

			if net.active:

				proc = self.trigger_displayer(
					" ",
					f"Disconnecting from {net.ssid}!"
				)
				self.wifi.disconnect_network(net)
				proc.kill()
				proc.wait()

			else:
				proc = self.trigger_displayer(
					" ",
					f"Connecting to {net.ssid}!"
				)
				try:
					self.wifi.connect_network(net)
				except WifiError:
					proc.kill()
					proc.wait()
					self.show_password_prompt(net)
				else:
					proc.kill()
					proc.wait()


		elif selected == wifi_options[1]:
			try:
				self.wifi.forget_network(net)
			except WifiError:
				proc = self.trigger_displayer(
					" ",
					f"Network {net.ssid} already unknown"
				)

				proc.wait()
				return

	
	def show_password_prompt(self, net: WifiNetwork) -> None:

		self.rofi.updateTheme(password_rasi)
		
		password = self.rofi.display(
			self.title,
			f"Enter password for {net.ssid}",
			[]
		)

		proc = self.trigger_displayer(
			" ",
			f"Connecting to {net.ssid}!"
		)
		
		try:
			self.wifi.connect_network(net, password)

		except WifiError:
			proc.kill()
			proc.wait()

			proc2 = self.trigger_displayer(
				" ",
				f"Incorrect password for {net.ssid}!"
			)

			proc2.wait()
			return
		
		else:
			proc.kill()
			proc.wait()

	
	def trigger_displayer(self, prompt: str, msg: str):

		self.rofi.updateTheme(display_rasi)

		return self.rofi.displayNoBlock(
			prompt,
			msg,
			[]
		)


if __name__ == "__main__":
	c = WifiMenu()
	c.launch()
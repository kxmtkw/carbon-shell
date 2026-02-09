import time

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
		]


	def launch(self):
		while not self.closed:
			self.show_main_menu()

	
	def make_wifi_entry(self, id: int, net: WifiNetwork) -> str:
		icon = "󰤥"
		sig = int(net.signal.strip())

		if sig > 80:
			icon = "󰤨"
		elif sig > 60:
			icon = "󰤥"
		elif sig > 40:
			icon = "󰤢"
		elif sig > 20:
			icon = "󰤟"
		else:
			icon = "󰤯"

		entry = f"{icon}   [{id}]  {net.ssid}{RofiShell.MarkActive if net.active else ''}"
		return entry
		

	def extract_id(self, entry: str) -> int:
		try:
			id = entry.split("]")[0].split("[")[1]
			return int(id)
		except ValueError, IndexError, TypeError:
			print(f"Error encountered when extracting id from entry. This should not happen at all. {entry}")
			exit(1)


	def show_main_menu(self):
		
		self.rofi.updateTheme(main_rasi)

		list_items = []
		list_items.extend(self.options)

		if self.wifi.is_radio_on():

			networks = self.wifi.list_networks()
		
			status = f"Status: ON | Connected: {'Yes' if self.wifi.get_active_network() else 'No'}"

			list_items.extend([self.make_wifi_entry(id, wifi) for id, wifi in enumerate(networks)])

		else:
			networks = None
			status = f"Status: OFF | Connected: No"


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
			try:
				self.wifi.rescan()
			except WifiError as w:
				print(w.details)
				
				if not self.wifi.is_radio_on():
					self.wifi.set_radio(True)

		else:
			print(networks)
			if networks:
				self.show_wifi_options(networks[self.extract_id(selected)])


	def show_wifi_options(self, net: WifiNetwork):
		
		self.rofi.updateTheme(options_rasi)

		wifi_options = [
			"<  Return",
			"󱘖  Disconnect" if net.active else "󱘖  Connect",
			"  Forget"
		]

		details = f"""
SSID:       {net.ssid}\n
BSSID:      {net.bssid}\n
Security:   {net.security}\n
Signal:     {net.signal}\n
Rate:       {net.rate}
"""

		selected = self.rofi.display(
			self.title,
			details,
			wifi_options
		)

		if not selected:
			exit()

		if selected == wifi_options[0]:
			return

		elif selected == wifi_options[1]:

			if net.active:
				self.disconnect_network(net)
			else:
				self.connect_network(net)


		elif selected == wifi_options[2]:
			self.forget_network(net)


	def connect_network(self, net: WifiNetwork):

		proc = self.trigger_displayer(
			" ",
			f"Connecting to network \"{net.ssid}\"..."
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


	def disconnect_network(self, net: WifiNetwork):

		proc = self.trigger_displayer(
			" ",
			f"Disconnecting from network \"{net.ssid}\"..."
		)
		self.wifi.disconnect_network(net)
		proc.kill()
		proc.wait()

	
	def forget_network(self, net: WifiNetwork):
		proc = self.trigger_displayer(
			" ",
			f"Forgetting network \"{net.ssid}\"..."
		)
		try:
			self.wifi.forget_network(net)

		except WifiError:
			proc.kill()
			proc.wait()

			proc2 = self.trigger_displayer(
				" ",
				f"Network \"{net.ssid}\" already unknown!"
			)
			proc2.wait()
		
		else:
			proc.kill()
			proc.wait()


	def show_password_prompt(self, net: WifiNetwork) -> None:

		self.rofi.updateTheme(password_rasi)
		
		password = self.rofi.display(
			self.title,
			f"Enter password for: {net.ssid}",
			[]
		)

		if not password:
			return

		proc = self.trigger_displayer(
			" ",
			f"Connecting to network \"{net.ssid}\"..."
		)
		
		try:
			self.wifi.connect_network(net, password)

		except WifiError:
			proc.kill()
			proc.wait()

			proc2 = self.trigger_displayer(
				" ",
				f"Incorrect password for \"{net.ssid}\"!"
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
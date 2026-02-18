import time

from lib.rofi import RofiShell
from lib.networker.wifi import WifiManager, WifiError, WifiNetwork

main_rasi = "~/.config/rofi/wifi/main.rasi"
options_rasi = "~/.config/rofi/wifi/options.rasi"
display_rasi = "~/.config/rofi/wifi/display.rasi"
password_rasi = "~/.config/rofi/wifi/password.rasi"


class Wifi:

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

		entry = f"{icon}   [{id}]  {RofiShell.markActive(net.ssid) if net.active else net.ssid}"
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


		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt= self.title,
			mesg= status,
			options= list_items
		)

		selected = self.rofi.wait()
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

		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt= self.title,
			mesg= details,
			options= wifi_options
		)
		selected = self.rofi.wait()

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

		self.trigger_displayer(
			" ",
			f"Connecting to network \"{net.ssid}\"..."
		)
		try:
			self.wifi.connect_network(net)
		except WifiError:
			self.rofi.close()
			self.show_password_prompt(net)
		else:
			self.rofi.close()


	def disconnect_network(self, net: WifiNetwork):

		self.trigger_displayer(
			" ",
			f"Disconnecting from network \"{net.ssid}\"..."
		)
		self.wifi.disconnect_network(net)
		self.rofi.close()

	
	def forget_network(self, net: WifiNetwork):
		proc = self.trigger_displayer(
			" ",
			f"Forgetting network \"{net.ssid}\"..."
		)
		try:
			self.wifi.forget_network(net)

		except WifiError:
			self.rofi.close()

			self.trigger_displayer(
				" ",
				f"Network \"{net.ssid}\" already unknown!"
			)
			self.rofi.wait()
		else:
			self.rofi.close()


	def show_password_prompt(self, net: WifiNetwork) -> None:

		self.rofi.updateTheme(password_rasi)
		self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt= self.title,
			mesg= f"Enter password for: {net.ssid}",
			password=True
		)
		
		password = self.rofi.wait()

		if not password:
			return

		self.trigger_displayer(
			" ",
			f"Connecting to network \"{net.ssid}\"..."
		)
		
		try:
			self.wifi.connect_network(net, password)

		except WifiError:
			self.rofi.close()

			self.trigger_displayer(
				" ",
				f"Incorrect password for \"{net.ssid}\"!"
			)

			self.rofi.wait()
			return
		
		else:
			self.rofi.close()

	
	def trigger_displayer(self, prompt: str, msg: str):

		self.rofi.updateTheme(display_rasi)

		return self.rofi.display(
			mode= RofiShell.Mode.dmenu,
			prompt=prompt,
			mesg=msg,
		)


if __name__ == "__main__":
	c = Wifi()
	c.launch()
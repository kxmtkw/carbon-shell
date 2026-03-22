from carbon.rofi import RofiShell
import backend, nmcli
from icons import Icons

normal_menu_rasi   =     "~/.carbon/shell/rofi/networker/normal_menu.rasi"
info_menu_rasi     =     "~/.carbon/shell/rofi/networker/info_menu.rasi"
display_mesg_rasi  =     "~/.carbon/shell/rofi/networker/display_mesg.rasi"
password_rasi      =     "~/.carbon/shell/rofi/networker/password.rasi"

class Displayer:

	def __init__(self):
		self.rofi = RofiShell(display_mesg_rasi)

	def show(self, icon: str, mesg: str):

		try: 
			self.rofi.close()
		except RofiShell.Error:
			pass

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=icon,
			mesg=mesg
		)

	def wait(self):
		self.rofi.wait()

	def close(self):
		self.rofi.close()


class Networker:

	def __init__(self):
		self.displayer = Displayer()
		self.rofi = RofiShell(info_menu_rasi)
		

		self.is_running: bool = True

		self.current = self.show_wifi_menu
		self.wifi_device: str | None = backend.get_default_wifi_device()
		self.selected_network: str | None = None

		backend.list_networks(None, True)

		
	def launch(self):
		while self.is_running:
			self.current()
		

	def show_main_menu(self):

		self.rofi.updateTheme(info_menu_rasi)
		
		title = "Networker"
		mesg = f"Device name:  {nmcli.general.get_hostname()}"
		options = [
			f"{Icons.devices}   List Devices",
			f"{Icons.wifi}   Configure Wifi",
			f"{Icons.hotspot}   Configure Hotspot",
			f"{Icons.airplane}   " + ("Turn on Airplane Mode" if nmcli.radio.wifi() or nmcli.radio.wwan() else "Turn off Airplane Mode"),
			f"{Icons.settings}   Advanced Settings"
		]

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			mesg=mesg,
			options=options
		)

		selected = self.rofi.wait()

		if not selected: 
			self.end()

		elif selected == options[0]:
			self.current = self.show_device_menu

		elif selected == options[1]:
			self.current = self.show_wifi_menu

		elif selected == options[2]:
			self.current = self.show_hotspot_menu

		elif selected == options[3]:
			backend.toggle_all_radio()

		elif selected == options[4]:
			backend.launch_nn_connection_editor()
			exit(0)
			

	def show_device_menu(self):
		
		self.rofi.updateTheme(normal_menu_rasi)

		title = "Network Devices"
		options = backend.list_devices()

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			options=options
		)

		selected = self.rofi.wait()

		self.current = self.show_main_menu 
		if not selected: return


	def show_hotspot_menu(self):
		# todo
		self.current = self.show_main_menu


	def show_wifi_menu(self):

		self.rofi.updateTheme(info_menu_rasi)
		
		title = "Wifi"

		radio = nmcli.radio.all()
		if radio.wifi and radio.wifi_hw:
			on_status = "on"
		elif radio.wifi and not radio.wifi_hw:
			on_status = "on (Hardware: off)"
		elif not radio.wifi and radio.wifi_hw:
			on_status = "off"
		else:
			on_status = "off (Hardware: off)"
		device = backend.get_device(self.wifi_device)

		mesg = f"""\
Radio     {on_status}
Device    {self.wifi_device}
Status    {device.state.capitalize()}"""
		
		options = [
			f">>>  {Icons.wifi}   Toggle Wifi",
			f">>>  {Icons.rescan}   Rescan",
		]

		networks = backend.list_networks(self.wifi_device)

		options.extend(
			networks
		)

		options.extend([
			f">>>  {Icons.devices}   Change Device",
			f">>>  {Icons.settings}   Networker Menu"    
		])

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			mesg=mesg,
			options=options
		)

		selected = self.rofi.wait()

		if not selected: 
			self.end()

		elif selected == options[0]:
			backend.toggle_wifi_radio()
			backend.list_networks(self.wifi_device, True)
		
		elif selected == options[1]:
			backend.list_networks(self.wifi_device, True)

		elif selected == options[-2]:
			self.current = self.show_wifi_device_options

		elif selected == options[-1]:
			self.current = self.show_main_menu

		else:
			self.selected_network = backend.get_id_from_formatted(selected)
			self.current = self.show_wifi_network_options


	def show_wifi_network_options(self):

		self.rofi.updateTheme(info_menu_rasi)
		
		network = backend.get_network(self.selected_network)

		title = "Wifi Network"
		details = f"""\
SSID       {network.ssid}
BSSID      {network.bssid}
Security   {network.security}
Signal     {network.signal}%
Rate       {network.rate}MiB/s"""
		
		options = [
			f"{Icons.return_sign}   Return",
			f"{Icons.connection}   " + ("Disconnect" if network.in_use else "Connect"),
			f"{Icons.cross}   Forget"
		]

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			mesg=details,
			options=options
		)

		selected = self.rofi.wait()


		self.current = self.show_wifi_menu
		if not selected: return

		elif selected == options[0]:
			self.current = self.show_wifi_menu
		
		elif selected == options[1]:

			if network.in_use:
				self.displayer.show(f"{Icons.wifi} ", f"Disconnecting {network.ssid}")
				backend.disconnect_network(network.bssid)
			else:
				try:
					self.displayer.show(f"{Icons.wifi} ", f"Connecting to {network.ssid}")
					backend.connect_network(self.wifi_device, network.bssid)
				except backend.Errors.ConnectionFailure:
					self.displayer.close()
					self.current = self.show_password_prompt
					return
				
			self.displayer.close()

		elif selected == options[2]:
			backend.forget_network(network.bssid)
		
		self.current = self.show_wifi_menu


	def show_wifi_device_options(self):

		self.rofi.updateTheme(normal_menu_rasi)

		title = "Wifi Devices"
		options = backend.list_wifi_devices()

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			options=options
		)

		selected = self.rofi.wait()

		self.current = self.show_wifi_menu
		if not selected: return

		else:
			self.wifi_device = backend.get_id_from_formatted(selected)
			self.current = self.show_wifi_menu


	def show_password_prompt(self):
		
		self.rofi.updateTheme(password_rasi)

		network = backend.get_network(self.selected_network)

		title = "Password Required"
		mesg = f"Enter password for '{network.ssid}'"

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=title,
			mesg=mesg,
			password=True
		)

		selected = self.rofi.wait()

		self.current = self.show_wifi_menu 
		if not selected: return

		self.displayer.show(f"{Icons.wifi} ", f"Connecting to {network.ssid}")


		try:
			backend.connect_network(self.wifi_device, self.selected_network, selected)
			self.displayer.close()
		except (backend.Errors.AuthFailure, backend.Errors.ConnectionFailure) as e:
			self.displayer.show(f"{Icons.error} ", f"Failed to connect to {network.ssid}")
			self.displayer.wait()
		
	def end(self):
		backend.dump_cache()
		exit(0)

	

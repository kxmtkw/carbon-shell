import time

import nmcli

from carbon.managers.controller.base import BaseController
from carbon.lib.rofi import RofiShell
from carbon.lib import networker as backend
from carbon.lib.networker import Icons

class Networker(BaseController):

	def __init__(self):
		self.rasi_normal = "~/.carbon/shell/rofi/networker/normal_menu.rasi"
		self.rasi_info = "~/.carbon/shell/rofi/networker/info_menu.rasi"
		self.rasi_mesg = "~/.carbon/shell/rofi/networker/display_mesg.rasi"
		self.rasi_password = "~/.carbon/shell/rofi/networker/password.rasi"

		self.rofi = RofiShell(self.rasi_info)

		self.is_running: bool = True

		self.current = self.showWifiMenu
		self.wifi_device: str = backend.getDefaultWifiDevice()
		self.selected_network: str = ""

		backend.listNetworks(None, True)

		
	def launch(self):
		self.is_running = True
		self.current = self.showWifiMenu
		while self.is_running:
			self.current()


	def close(self):
		self.is_running = False
		try:
			self.rofi.close()
		except RofiShell.Error:
			pass


	def displayMessageRofi(self, icon: str, mesg: str):
		self.rofi.updateTheme(self.rasi_mesg)
		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt=icon,
			mesg=mesg
		)
		

	def showMainMenu(self):

		self.rofi.updateTheme(self.rasi_info)
		
		mesg = f"Device name:  {nmcli.general.get_hostname()}"
		
		options = [
			f"{Icons.devices}   List Devices",
			f"{Icons.wifi}   Configure Wifi",
			f"{Icons.hotspot}   Configure Hotspot",
			f"{Icons.airplane}   Toggle Airplane Mode",
			f"{Icons.settings}   Advanced Settings"
		]

		if nmcli.radio.wifi() or nmcli.radio.wwan():
			RofiShell.markActive(options[3])

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Networker",
			mesg=mesg,
			options=options
		)

		selected = self.rofi.wait()

		if not selected: 
			self.close()

		elif selected == options[0]:
			self.current = self.showDeviceMenu

		elif selected == options[1]:
			self.current = self.showWifiMenu

		elif selected == options[2]:
			self.current = self.showHotspotMenu

		elif selected == options[3]:
			backend.toggleAllRadio()

		elif selected == options[4]:
			backend.launchNnConnectionEditor()
			exit(0)
			

	def showDeviceMenu(self):
		
		self.rofi.updateTheme(self.rasi_normal)

		options = backend.listDevices()

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Network Devices",
			options=options
		)

		selected = self.rofi.wait()

		self.current = self.showMainMenu 
		if not selected: return


	def showHotspotMenu(self):
		# todo
		self.current = self.showMainMenu


	def showWifiMenu(self):

		self.rofi.updateTheme(self.rasi_info)
		
		radio = nmcli.radio.all()
		if radio.wifi and radio.wifi_hw:
			on_status = "on"
		elif radio.wifi and not radio.wifi_hw:
			on_status = "on (Hardware: off)"
		elif not radio.wifi and radio.wifi_hw:
			on_status = "off"
		else:
			on_status = "off (Hardware: off)"
		device = backend.getDevice(self.wifi_device)

		mesg = f"""\
Radio     {on_status}
Device    {self.wifi_device}
Status    {device.state.capitalize()}"""
		
		options = [
			f">>>  {Icons.wifi}   Toggle Wifi",
			f">>>  {Icons.rescan}   Rescan",
		]

		networks = backend.listNetworks(self.wifi_device)

		options.extend(
			networks
		)

		options.extend([
			f">>>  {Icons.devices}   Change Device",
			f">>>  {Icons.settings}   Networker Menu"    
		])

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Wifi",
			mesg=mesg,
			options=options
		)

		selected = self.rofi.wait()

		if not selected: 
			self.close()

		elif selected == options[0]:
			backend.toggleWifiRadio()
			backend.listNetworks(self.wifi_device, True)
		
		elif selected == options[1]:
			backend.listNetworks(self.wifi_device, True)

		elif selected == options[-2]:
			self.current = self.showWifiDeviceOptions

		elif selected == options[-1]:
			self.current = self.showMainMenu

		else:
			self.selected_network = backend.getIdFromFormatted(selected)
			self.current = self.showWifiNetworkOptions


	def showWifiNetworkOptions(self):

		self.rofi.updateTheme(self.rasi_info)
		
		network = backend.getNetwork(self.selected_network)

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
			prompt="Wifi Network",
			mesg=details,
			options=options
		)

		selected = self.rofi.wait()


		self.current = self.showWifiMenu
		if not selected: return

		elif selected == options[0]:
			self.current = self.showWifiMenu
		
		elif selected == options[1]:

			if network.in_use:
				self.displayMessageRofi(f"{Icons.wifi} ", f"Disconnecting {network.ssid}")
				backend.disconnectNetwork(network.bssid)
				self.rofi.close()
			else:
				try:
					self.displayMessageRofi(f"{Icons.wifi} ", f"Connecting to {network.ssid}")
					backend.connectNetwork(self.wifi_device, network.bssid)
					self.rofi.close()
				except backend.Errors.ConnectionFailure:
					self.rofi.close()
					self.current = self.showPasswordPrompt
					return

		elif selected == options[2]:
			backend.forgetNetwork(network.bssid)
		
		backend.listNetworks(self.wifi_device, True)

		self.current = self.showWifiMenu


	def showWifiDeviceOptions(self):

		self.rofi.updateTheme(self.rasi_normal)

		options = backend.listWifiDevices()

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Wifi Devices",
			options=options
		)

		selected = self.rofi.wait()

		self.current = self.showWifiMenu
		if not selected: return

		else:
			self.wifi_device = backend.getIdFromFormatted(selected)
			self.current = self.showWifiMenu


	def showPasswordPrompt(self):
		
		self.rofi.updateTheme(self.rasi_password)

		network = backend.getNetwork(self.selected_network)

		mesg = f"Enter password for '{network.ssid}'"

		self.rofi.display(
			mode=RofiShell.Mode.dmenu,
			prompt="Password Required",
			mesg=mesg,
			password=True
		)

		selected = self.rofi.wait()

		self.current = self.showWifiMenu 
		if not selected: return

		self.displayMessageRofi(f"{Icons.wifi} ", f"Connecting to {network.ssid}")
		try:
			backend.connectNetwork(self.wifi_device, self.selected_network, selected)
			backend.listNetworks(self.wifi_device, True)
			self.rofi.close()
		except (backend.Errors.AuthFailure, backend.Errors.ConnectionFailure) as e:
			self.rofi.close()
			self.displayMessageRofi(f"{Icons.error} ", f"Failed to connect to {network.ssid}")
			time.sleep(3)
			self.rofi.close()


from carbon.rofi import RofiShell
import backend, nmcli

class Networker:

    def __init__(self):
        self.rofi = RofiShell("~/.carbon/shell/rofi/wifi/main.rasi")
        
        self.is_running: bool = True

        self.current = self.show_wifi_menu

        self.wifi_device: str | None = backend.get_default_wifi_device()
        self.selected_network: str | None = None


    def launch(self):
        while self.is_running:
            self.current()
        

    def show_main_menu(self):
        
        title = "Networker"
        mesg = f"Device Name: {nmcli.general.get_hostname()}"
        options = [
            "List Devices",
            "Configure Wifi",
            "Configure Hotspot",
            "Airplane Mode",
            "Advanced Settings"
        ]

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=mesg,
            options=options
        )

        selected = self.rofi.wait()

        if not selected: 
            exit()

        elif selected == options[0]:
            self.current = self.show_device_menu

        elif selected == options[1]:
            self.current = self.show_wifi_menu

        elif selected == options[2]:
            self.current = self.show_hotspot_menu

        elif selected == options[3]:
            backend.toggle_all_radio()

        elif selected == options[4]:
            self.current = self.show_device_menu
            

    def show_device_menu(self):
        
        title = "Network Devices"
        mesg = ""
        options = backend.list_devices()

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=mesg,
            options=options
        )

        selected = self.rofi.wait()

        if not selected: 
            exit()

        else:
            self.current = self.show_main_menu


    def show_hotspot_menu(self):
        # todo
        self.current = self.show_main_menu


    def show_wifi_menu(self):

        self.rofi.updateTheme("~/.carbon/shell/rofi/wifi/main.rasi")
        
        title = "Wifi"

        radio = nmcli.radio.all()
        on_status = "On" if radio.wifi and radio.wifi_hw else "On (Hardware: Off)" if radio.wifi else "Off (Hardware: Off)"
        device = backend.get_device(self.wifi_device)

        mesg = f"Toggled: {on_status}\nStatus: {device.state.capitalize()}\nDevice:{self.wifi_device} "
        options = [
            ">> Toggle Wifi",
            ">> Rescan",
        ]

        networks = backend.list_networks(self.wifi_device, True)

        options.extend(
            networks
        )

        options.extend([
            ">> Change Device",
            ">> Networker Menu"    
        ])

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=mesg,
            options=options
        )

        selected = self.rofi.wait()

        if not selected: 
            exit()

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
        
        network = backend.get_network(self.selected_network)

        title = "Wifi Network"
        details = f"""
SSID:       {network.ssid}\n
BSSID:      {network.bssid}\n
Security:   {network.security}\n
Signal:     {network.signal}%\n
Rate:       {network.rate}MiB/s
"""
        options = [
            "Return",
            "Disconnect" if network.in_use else "Connect",
            "Forget"
        ]

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=details,
            options=options
        )

        selected = self.rofi.wait()

        if not selected: 
            exit()

        elif selected == options[0]:
            self.current = self.show_wifi_menu
        
        elif selected == options[1]:
            if network.in_use:
                backend.disconnect_network(network.bssid)
            else:
                try:
                    backend.connect_network(self.wifi_device, network.bssid)
                except backend.Errors.ConnectionFailure:
                    self.current = self.show_password_prompt
                    return

        elif selected == options[2]:
            backend.forget_network(network.bssid)

        self.current = self.show_wifi_menu


    def show_wifi_device_options(self):
        title = "Wifi Devices"
        mesg = ""
        options = backend.list_wifi_devices()

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=mesg,
            options=options
        )

        selected = self.rofi.wait()

        if not selected: 
            exit()

        else:
            self.wifi_device = backend.get_id_from_formatted(selected)
            self.current = self.show_wifi_menu


    def show_password_prompt(self):
        self.rofi.updateTheme("~/.carbon/shell/rofi/wifi/password.rasi")
        title = "Password Required"
        mesg = ""

        self.rofi.display(
            mode=RofiShell.Mode.dmenu,
            prompt=title,
            mesg=mesg,
        )

        selected = self.rofi.wait()

        if not selected:
            exit()

        try:
            backend.connect_network(self.wifi_device, self.selected_network, selected)
        except backend.Errors.AuthFailure as e:
            raise e
        
        self.current = self.show_wifi_menu
        

    def show_error_mesg(self):
        pass

    

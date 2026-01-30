from rofi import RofiShell
import subprocess
from dataclasses import dataclass

@dataclass(init=True)
class WifiNetwork:
    ssid: str
    bssid: str
    bars: str
    signal: int 
    security: str
    connected: bool = False
    icon: str = ""

class NetworkControl:

    def __init__(self):
        pass

    def run(self, cmd) -> str:
        output = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if (output.returncode == 0): return output.stdout
        return output.stderr


    def is_wifi_on(self) -> bool:
        output = self.run("nmcli radio wifi").strip()

        if output == "enabled":
            return True
        
        return False


    def set_wifi_radio(self, on: bool):
        self.run(f"nmcli radio wifi {'on' if on else 'off'}")


    def list_networks(self) -> list[WifiNetwork]:

        output = self.run("nmcli -f SSID,BSSID,SECURITY,SIGNAL,BARS,ACTIVE device wifi list")

        networks = []

        for line in output.splitlines()[1:]:

            items = [item for item in line.split(" ") if item != " "]

            ssid = items[0]
            bssid = items[1]
            security = items[2]
            signal = items[3]
            bars = items[4]
            active = True if items[5] == "yes" else False 

            networks.append(WifiNetwork(ssid, bssid, bars, signal, security, active))

        return networks


class WifiMenu:

    def __init__(self):
        self.rofi = RofiShell("~/.config/rofi/launcher.rasi")

        self.networks = NetworkControl()

        nets = self.networks.list_networks()

        names = [net.ssid for net in nets]
        print(names)
        while True:
            print(self.rofi.display(" ", " ", names))
        

w = WifiMenu()

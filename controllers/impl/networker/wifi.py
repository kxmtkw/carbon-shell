from dataclasses import dataclass

from .helpers import shellRun, processRun, ShellOutput


@dataclass
class WifiNetwork:
    ssid: str
    bssid: str
    security: str
    signal: str
    rate: str
    active: bool


class WifiError(Exception):
    def __init__(self, msg: str, details: str) -> None:
        self.msg = msg
        self.details = details
        super().__init__(msg)


class WifiManager:

    def __init__(self) -> None:
        self._scanned_networks: list[WifiNetwork] = []
        self._active_network: WifiNetwork | None = None


    def is_radio_on(self) -> bool:

        output = shellRun("nmcli radio wifi")

        if output.success:

            if output.stdout == "enabled":
                return True
            
            return False
        
        raise WifiError(f"Could check wifi radio.", f"Error:\n{output.stdout}")

        
    def set_radio(self, on: bool):
        
        output = shellRun(f"nmcli radio wifi {'on' if on else 'off'}")

        if not output.success:
            raise WifiError(f"Could set wifi radio", f"Error:\n{output.stdout}")


    def rescan(self):
        
        output = shellRun(f"nmcli device wifi rescan")

        if not output.success:
            raise WifiError(f"Could rescan wifi radio.", f"Error:\n{output.stdout}")




    def list_networks(self) -> list[WifiNetwork]:

        networks = []

        output = shellRun("nmcli -t -f SSID,BSSID,RATE,SIGNAL,SECURITY,ACTIVE device wifi list")

        if not output.success:
            raise WifiError(f"Could get wifi networks.", f"Error:\n{output.stdout}")
        
        for line in output.stdout.splitlines():

            fragments = line.split(":")

            ssid = fragments[0]
            bssid = ":".join([f for f in fragments[1:7]]).replace("\\", "") 
            rate = fragments[7]
            signal = fragments[8]
            security = fragments[9]
            active = fragments[10]

            net = WifiNetwork(ssid, bssid, security, signal, rate, True if active == "yes" else False)

            if net.active:
                networks.insert(0, net)
                self._active_network = net
            else:
                networks.append(net)

        self._scanned_networks = networks

        return networks


    def get_active_network(self) -> WifiNetwork | None:
        return self._active_network


    def connect_network(self, network: WifiNetwork, passwd: str | None = None):

        if passwd:
            output = shellRun(f"nmcli device wifi connect {network.bssid} password {passwd}")
        else: 
            output = shellRun(f"nmcli device wifi connect {network.bssid}")

        if output.success:
            return
        
        processRun(["nmcli", "connection", "delete", network.ssid])

        raise WifiError(f"Could not connect to {network.ssid}.", f"Error:\n{output.stdout}")


    def disconnect_network(self, network: WifiNetwork):
        output = processRun(["nmcli", "connection", "down", network.ssid])

        if not output.success:
            raise WifiError(f"Could not disconnect from {network.ssid}.", f"Error:\n{output.stdout}")

    def forget_network(self, network: WifiNetwork):
        output = processRun(["nmcli", "connection", "delete", network.ssid])

        if not output.success:
            raise WifiError(f"Could not forget {network.ssid}:", f"Error:\n{output.stdout}")
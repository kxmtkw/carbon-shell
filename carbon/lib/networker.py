from carbon.lib.rofi import RofiShell
import nmcli, subprocess, json

class Icons:

    devices = "󰭰"
    hotspot = "󰠿"
    wifi = ""
    airplane = ""
    settings = ""

    rescan = ""
    return_sign = ""
    connection = "󱘖"
    cross = ""

    error = ""

nmcli.disable_use_sudo()

cache = {}

class Errors:

    class InternalError(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class ConnectionFailure(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class AuthFailure(Exception):
        def __init__(self, *args):
            super().__init__(*args)



def listDevices() -> list[str]:

    if "listDevices" in cache:
        return cache["listDevices"]
    
    formatted_devices = []

    devices = nmcli.device()
    max_name_len = max(len(d.device) for d in devices)
    max_type_len = max(len(d.device_type) for d in devices)

    for device in devices:
        formatted = f"{Icons.devices}   <b>{device.device:<{max_name_len}}</b>  :: {device.device_type:<{max_type_len}}  {device.state}"
        formatted_devices.append(formatted)

    cache["listDevices"] = formatted_devices


    return formatted_devices


def listWifiDevices() -> list[str]:

    if "listWifiDevices" in cache:
        return cache["listWifiDevices"]
    
    formatted_devices = []

    devices = nmcli.device()
    max_name_len = max(len(d.device) for d in devices)
    max_type_len = max(len(d.device_type) for d in devices)

    for device in devices:
        if device.device_type != "wifi": continue
        formatted = f"{Icons.devices}   <b>{device.device:<{max_name_len}}</b>  :: {device.device_type:<{max_type_len}}  {device.state}<span alpha='1'>|{device.device}|</span>"
        formatted_devices.append(formatted)

    cache["listWifiDevices"] = formatted_devices

    return formatted_devices


def getDevice(name: str) -> nmcli.data.device.Device:

    devices =  nmcli.device()

    for dev in devices:
        if dev.device == name:
            return dev


def getDefaultWifiDevice() -> str:
    devices = nmcli.device()

    for d in devices:
        if d.device_type == "wifi" and d.state == "connected":
            return d.device

    for d in devices:
        if d.device_type == "wifi" and d.state == "disconnected":
            return d.device

    for d in devices:
        if d.device_type == "wifi":
            return d.device
        
    return None


def listNetworks(device: str | None = None, rescan: bool = False) -> list[str]:

    if device is None:
        device = getDefaultWifiDevice()

    if f"list_networks_{device}" in cache and not rescan:
        return cache[f"list_networks_{device}"]
    
    if rescan:
        rescanWifi()

    formatted_networks = []
    networks = nmcli.device.wifi(device)

    for net in networks:
        
        icon = "󰤥"

        if net.signal > 80:
            icon = "󰤨"
        elif net.signal > 60:
            icon = "󰤥"
        elif net.signal > 40:
            icon = "󰤢"
        elif net.signal > 20:
            icon = "󰤟"
        else:
            icon = "󰤯"

        formatted = f"{icon}   <i>{net.ssid}</i><span alpha='1'>|{net.bssid}|</span>"

        if net.in_use:
            formatted_networks.insert(0, RofiShell.markActive(formatted))
        else:
            formatted_networks.append(formatted)

    cache[f"list_networks_{device}"] = formatted_networks

    return formatted_networks


def rescanWifi(device: str | None = None):

    if device is None:
        device = getDefaultWifiDevice()

    try:
        nmcli.device.wifi_rescan(device)
    except nmcli._exception.ScanningNotAllowedException:
        pass


def toggleAllRadio():
    radio = nmcli.radio()

    if radio.wifi or radio.wwan:
        nmcli.radio.all_off()
    else:
        nmcli.radio.all_on()


def toggleWifiRadio():
    radio = nmcli.radio.wifi()

    if radio:
        nmcli.radio.wifi_off()
    else:
        nmcli.radio.wifi_on()


def getNetwork(bssid: str) -> nmcli.data.device.DeviceWifi:

    networks: list[nmcli.data.device.DeviceWifi] = nmcli.device.wifi()

    for net in networks:
        if net.bssid == bssid:
            return net

    
def connectNetwork(device: str, bssid: str, passwd: str | None = None):
    network = getNetwork(bssid)

    if passwd:
        output = subprocess.run(f"nmcli device wifi connect {network.bssid} password {passwd} ifname {device}", shell=True, capture_output=True, text=True)
    else: 
        output = subprocess.run(f"nmcli device wifi connect {network.bssid} ifname {device}", shell=True, capture_output=True, text=True)

    if output.returncode == 0:
        return
    
    subprocess.run(["nmcli", "connection", "delete", network.ssid], capture_output=True, text=True)

    raise Errors.ConnectionFailure(f"Could not connect to {network.ssid}.", output.stdout)


def disconnectNetwork(bssid: str):
    network = getNetwork(bssid)

    try:
        nmcli.connection.down(network.ssid)
    except nmcli._exception.NotExistException:
        pass


def forgetNetwork(bssid: str):
    network = getNetwork(bssid)

    try:
        nmcli.connection.delete(network.ssid)
    except nmcli._exception.NotExistException:
        pass 


def getIdFromFormatted(formatted: str) -> str:
    "Get id from formatted text from backend"
    parts = formatted.split("|")

    if len(parts) < 2:
        raise Errors.InternalError("Not Formatted by backend")
    
    return parts[-2]


def launchNnConnectionEditor():
    subprocess.Popen(["nm-connection-editor"])

import sys
from carbon.controllers.rofi import RofiShell
from .power import PowerMenu
from .battery import BatteryInfo
from .system import SystemInfo

from carbon.helpers import CarbonError

def launch_controller(controller: str):
    match controller:
        case "power":
            PowerMenu().launch()
        case "battery":
            BatteryInfo().launch()
        case "system":
            SystemInfo().launch()
        case "windows":
            RofiShell.Run("rofi -show window -theme ~/.config/rofi/windows.rasi")
        case "launcher":
            RofiShell.Run("rofi -show drun -theme ~/.config/rofi/launcher.rasi")
        case "launcher-run":
            RofiShell.Run("rofi -show run -theme ~/.config/rofi/launcher.rasi")
        case "launcher-files":
            RofiShell.Run("rofi -show filebrowser -theme ~/.config/rofi/launcher.rasi")
        case _:
            CarbonError(f"Unknown controller :: {controller}").halt()   
    

if __name__ == "__main__":
    try:
        launch_controller(sys.argv[1])
    except IndexError:
        CarbonError("Insufficient or Multiple controller specified. Only specify one controller").halt()
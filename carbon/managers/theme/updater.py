from pathlib import Path

from carbon.utils import shellrun, writefile, procrun, CarbonError

from .colors import *
from . import fonts

from carbon.lib.quickshell import Quickshell

class ThemeUpdater:


    def __init__(self):
        self.colorfiles = {}
        self.colorfiles["rofi"]  = "~/.carbon/shell/rofi/Config/color.rasi"
        self.colorfiles["json"]  = "~/.carbon/shell/quickshell/Config/color.json"
        self.colorfiles["kde"]   = "~/.local/share/color-schemes/Carbon.colors"
        self.colorfiles["hypr"]  = "~/.carbon/hypr/color.conf"

        self.qs = Quickshell()

        self.post_update_commands = [
            "plasma-apply-colorscheme BreezeDark && plasma-apply-colorscheme Carbon",
            "hyprctl reload"
        ]


    def updateColors(self, colors: dict[str, str]):

        for type, filepath in self.colorfiles.items():

            filepath = Path(filepath).expanduser()

            match type:

                case "json":
                    string = updateJson(colors)
                    writefile(filepath, string)

                case "kde":
                    string = updateKde(colors)
                    writefile(filepath, string)

                case "rofi":
                    string = updateRofi(colors)
                    writefile(filepath, string)

                case "hypr":
                    string = updateHypr(colors)
                    writefile(filepath, string)

                case "kitty":
                    continue
                    string = color.update_kitty(colors)
                    writefile(filepath, string)

                case "alacritty":
                    continue
                    string = color.update_alacritty(colors)
                    writefile(filepath, string)
                
                case _:
                    print(f"Error :: {type}")
                    continue
        
        self.runPostUpdate()


    def updateFont(self, font: str):

        rofifile = Path("~/.carbon/shell/rofi/Config/fonts.rasi").expanduser()

        rofi = fonts.updateRofi(font)
        writefile(rofifile, rofi)

        self.qs.updateFont(font)


    def updateFace(self, path: str):

        if not Path(path).expanduser().exists():
            raise CarbonError(f"Face image not found: {path}")
        
        out = shellrun(f"cp {path} ~/.carbon/user/face")

        if not out[0]:
            raise CarbonError(f"Failed to update face image. Reason: {out[1]}")


    def runPostUpdate(self):
        for cmd in self.post_update_commands:
            shellrun(cmd)

        self.qs.updateTheme()
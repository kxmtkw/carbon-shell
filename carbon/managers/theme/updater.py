from pathlib import Path

from carbon.utils import shellrun, writefile, procrun

from .colors import *
from . import fonts

from carbon.lib.quickshell import Quickshell

class ThemeUpdater:


    def __init__(self):
        self.colorfiles = {}
        self.colorfiles["rofi"] = "~/.carbon/shell/rofi/Config/color.rasi"
        self.colorfiles["json"] = "~/.carbon/shell/quickshell/Config/color.json"
        self.colorfiles["kde"]  = "~/.local/share/color-schemes/Carbon.colors"

        self.qs = Quickshell()

        self.post_update_commands = [
            "plasma-apply-colorscheme BreezeDark && plasma-apply-colorscheme Carbon",
            "hyprctl reload"
        ]


    def update_colors(self, colors: dict[str, str]):

        for type, filepath in self.colorfiles.items():

            filepath = Path(filepath).expanduser()

            match type:

                case "json":
                    string = update_json(colors)
                    writefile(filepath, string)

                case "kde":
                    string = update_kde(colors)
                    writefile(filepath, string)

                case "rofi":
                    string = update_rofi(colors)
                    writefile(filepath, string)

                case "hypr":
                    continue
                    string = update_hypr(colors)
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
        
        self.run_post_update()


    def update_font(self, font: str):

        rofifile = Path("~/.carbon/shell/rofi/Config/fonts.rasi").expanduser()

        rofi = fonts.update_rofi(font)
        writefile(rofifile, rofi)

        self.qs.updateFont(font)


    def run_post_update(self):
        for cmd in self.post_update_commands:
            shellrun(cmd)

        self.qs.updateTheme()